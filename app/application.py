import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import cv2 as cv
from core.db.business import Student, Log
from core.face.helper import FaceHelper
from conf.admin import ConfigManager
from PIL import Image,ImageQt
import multiprocessing as mp
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import time
import setproctitle


class MainWindow(QMainWindow):

    __student = Student()
    __face = FaceHelper()
    __config = ConfigManager()
    __thumbnail_path = __config.get_path_value("thumbnail")
    __model = __config.get_model_value("name")
    __current_student_no = ""

    def __init__(self, log, queue):

        QMainWindow.__init__(self)
        self.log = log
        self.log.start()
        self.queue = queue
        self.cap = cv.VideoCapture(0)
        width = int(self.__config.get_capture_value("width"))
        height = int(self.__config.get_capture_value("height"))
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, height)
        self.setGeometry(QtCore.QRect(0,0,800,480))
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.displayLabel = QLabel(self)
        self.displayLabel.setGeometry(QtCore.QRect(0,0,800,480))
        self.displayLabel.setFixedSize(800, 480)
        self.shadow = ShadowWidget()
        self.shadow.setParent(self, Qt.FramelessWindowHint|Qt.Window)
        self.shadow.hide()
        self.show()
        self.timer = QTimer()
        self.timer.start()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.start_camera)
        self.shadowTimer = QTimer()
        self.shadowTimer.setInterval(10000)
        self.shadowTimer.timeout.connect(self.hide_shadow)

    def quit(self):
        try:
            self.log.terminate()
            self.cap.release()
            self.close()
        except KeyboardInterrupt:
            self.log.terminate()
            self.close()

    def hide_shadow(self):

        self.shadow.hide()
        self.shadowTimer.stop()

    def insert_log_and_sent_sms(self, info):

        if self.__current_student_no != info["StudentNo"]:
            self.__current_student_no = info["StudentNo"]
            temperature = {"temperature": 36.1}
            info.update(temperature)
            self.queue.put(info)

    def find_student(self, image, locations):

        if len(locations) > 0:
            info = self.__student.get_student_by_picture(None, image, locations)
            if len(info) and len(info["PictureName"]) > 0:
                self.bind_result(info)
                self.insert_log_and_sent_sms(info)
                self.shadowTimer.start()

    def find_face_location(self, image, small_image):

        locations = self.__face.get_face_locations(small_image, number_of_times_to_upsample=0, model=self.__model)
        if len(locations) > 0:
            for (top, right, bottom, left) in locations:
                cv.rectangle(image, (left*4, top*4), (right*4, bottom*4), (0, 255, 0), 2)
            self.bind_player(image)
            self.find_student(small_image, locations)
        else:
            self.bind_player(image)

    def bind_result(self, info):
        self.shadowTimer.start()
        image = Image.open(os.path.join(self.__thumbnail_path, info["PictureName"]))
        img = ImageQt.ImageQt(image)
        self.shadow.photoLabel.setPixmap(
            QPixmap.fromImage(img).scaled(self.shadow.photoLabel.width(), self.shadow.photoLabel.height()))
        self.shadow.studentNameLabel.setText("姓名：" + info["Name"])
        self.shadow.studentNoLabel.setText("学号：" + info["StudentNo"])
        self.shadow.show()

    def bind_player(self, image):
        image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
        img = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
        self.displayLabel.setPixmap(
            QPixmap.fromImage(img).scaled(self.displayLabel.width(), self.displayLabel.height()))

    def start_camera(self):

        try:

            success, image = self.cap.read()

            if success:
                picture = cv.cvtColor(image, cv.COLOR_BGR2RGB)
                small_image = cv.resize(picture, (0, 0), fx=0.25, fy=0.25)
                small_image = small_image[:, :, ::-1]
                self.find_face_location(image, small_image)

        except KeyboardInterrupt:
            pass


class ShadowWidget(QWidget):

    def __init__(self, parent=None):
        super(ShadowWidget,self).__init__(parent)

        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setGeometry(QtCore.QRect(640, 0, 160, 480))
        vLayout = QVBoxLayout(self)
        self.photoLabel = QLabel(self)
        self.photoLabel.setFixedSize(90,120)
        self.photoLabel.setAlignment(Qt.AlignLeft)
        self.studentNoLabel = QLabel(self)
        self.studentNoLabel.setAlignment(Qt.AlignLeft)
        self.studentNameLabel = QLabel(self)
        self.studentNameLabel.setAlignment(Qt.AlignLeft)
        vLayout.addStretch(1)
        vLayout.addWidget(self.photoLabel)
        vLayout.addWidget(self.studentNoLabel)
        vLayout.addWidget(self.studentNameLabel)
        vLayout.addStretch(1)
        self.setLayout(vLayout)


class LogService(mp.Process):

    __log = Log()

    def __init__(self, tasks):
        super(LogService, self).__init__()
        self.__tasks = tasks
        print("{} - The log service has been init...".format(mp.current_process()))

    def run(self):
        print("The log service has been started... pid is {}, process name is {}, current process is {}".format(
            mp.Process.pid, mp.Process.name, mp.current_process()))
        try:
            while True:
                info = self.__tasks.get(True)
                self.check_is_sent_sms(info)
                time.sleep(1)
        except KeyboardInterrupt:
            pass

    def check_is_sent_sms(self, info):
        sms = 0
        if len(self.__log.total_record_by_minutes(int(info["ID"]))) <= 0:
            self.sms()
            sms = 1
        self.insert(info, sms)

    def insert(self, info, sms):
        self.__log.insert(int(info["ID"]), info["StudentNo"], info["Name"], info["temperature"],
                          0, sms, info["ParentMobile"])

    def sms(self):
        pass


if __name__ == '__main__':

    setproctitle.setproctitle("MISApplication")
    q = mp.Queue()
    scheduler = LogService(q)
    app = QApplication([])
    w = MainWindow(scheduler, q)
    w.show()
    app.exec_()
