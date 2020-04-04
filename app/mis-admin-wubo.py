import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import cv2 as cv
from core.db.business import Student, Log
from core.face.helper import FaceHelper
from conf.admin import ConfigManager
from PIL import Image,ImageQt
from multiprocessing import Queue, Process
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class MainWindow(QMainWindow):

    __logs = Queue()
    __student = Student()
    __face = FaceHelper()
    __log = Log()
    __config = ConfigManager()
    __config = ConfigManager()
    __thumbnail_path = __config.get_path_value("thumbnail")
    __current_student_no = ""

    def __init__(self):
        QMainWindow.__init__(self)
        self.cap = cv.VideoCapture(0)
        width = 1024  # 定义摄像头获取图像宽度
        height = 768  # 定义摄像头获取图像长度
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, height)
        print(self.cap.get(3))
        print(self.cap.get(4))
        self.setGeometry(QtCore.QRect(0,0,800,480))
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.displayLabel = QLabel(self)
        self.displayLabel.setGeometry(QtCore.QRect(0,0,800,480))
        self.displayLabel.setFixedSize(800,480)
        self.shade = Shadewidget()
        self.shade.setParent(self,Qt.FramelessWindowHint|Qt.Window)
        self.shade.hide()
        self.show()
        self.timer = QTimer()
        self.timer.start()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.start_camera)
        self.shadeTimer = QTimer()
        self.shadeTimer.setInterval(10000)
        self.shadeTimer.timeout.connect(self.hideShade)

    def quit(self):
        try:
            self.cap.release()
            self.close()
        except KeyboardInterrupt:
            self.close()
    def hideShade(self):

        self.shade.hide()
        self.shadeTimer.stop()

    def insert_log_and_sent_sms(self, info):

        temperature = {"temperature": 36.1}
        info.update(temperature)

        self.__logs.put(info)
        task = LogProcess(self.__logs)
        task.daemon = True
        task.start()
        task.join()

    def find_student(self, image, locations):

        if len(locations) > 0:
            info = self.__student.get_student_by_picture(None, image, locations)
            if len(info) and len(info["PictureName"]) > 0:
                if self.__current_student_no != info["StudentNo"]:
                    # self.insert_log_and_sent_sms(info)
                    self.__current_student_no = info["StudentNo"]
                self.bind_result(info)
                self.shadeTimer.start()


    def find_face_location(self,image,small_image):
        locations = self.__face.get_face_locations(small_image, number_of_times_to_upsample=0, model="hog")
        if len(locations) > 0:
            for (top, right, bottom, left) in locations:
                cv.rectangle(image, (left*4, top*4), (right*4, bottom*4), (0, 255, 0), 2)
            self.bind_player(image)
            self.find_student(small_image, locations)
    def bind_result(self, info):
        self.shadeTimer.start()
        image = Image.open(os.path.join(self.__thumbnail_path, info["PictureName"]))
        img = ImageQt.ImageQt(image)
        self.shade.photoLabel.setPixmap(QPixmap.fromImage(img).scaled(self.shade.photoLabel.width(), self.shade.photoLabel.height()))
        self.shade.studentNameLabel.setText("姓名："+info["Name"])
        self.shade.studentNoLabel.setText("学号："+info["StudentNo"])
        self.shade.show()
    def bind_player(self, image):
        image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
        img = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
        self.displayLabel.setPixmap(QPixmap.fromImage(img).scaled(self.displayLabel.width(),self.displayLabel.height()))

    def start_camera(self):
        success, image = self.cap.read()
        if success:
            imageRGB = cv.cvtColor(image, cv.COLOR_BGR2RGB)
            small_image = cv.resize(imageRGB, (0, 0), fx=0.25, fy=0.25)
            small_image = small_image[:, :, ::-1]
            self.bind_player(image)
            self.find_face_location(image,small_image)


class Shadewidget(QWidget):

    def __init__(self,parent=None):
        super(Shadewidget,self).__init__(parent)

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


class LogProcess(Process):

    __log = Log()

    def __init__(self, logs):
        Process.__init__(self)
        self.logs = logs

    def run(self):

        if not bool(self.logs.empty()):

            self.check_is_sent_sms(self.logs.get())

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
    app=QApplication([])
    w = MainWindow()
    w.show()
    app.exec_()
