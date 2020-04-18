import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import cv2 as cv
from core.db.business import Student, Log
from core.face.helper import FaceHelper
from conf.admin import ConfigManager
from PIL import Image,ImageQt
import multiprocessing as mp
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import time
import qdarkstyle
import setproctitle
import logging
import subprocess as sp
import shutil


class MainWindow(QWidget):

    __student = Student()
    __face = FaceHelper()
    __config = ConfigManager()
    __thumbnail_path = __config.get_path_value("thumbnail")
    __model = __config.get_model_value("name")
    __current_student_no = ""

    def __init__(self, log, queue, parent=None):
        super().__init__(parent)
        self.log = log
        self.log.start()
        self.queue = queue
        self.cap = cv.VideoCapture(0)
        width = int(self.__config.get_capture_value("width"))
        height = int(self.__config.get_capture_value("height"))
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, height)
        self.mlayout = QHBoxLayout(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setGeometry(0,0,800,480)
        self.displayLabel = QLabel(self)
        self.displayLabel.setFixedSize(640, 480)
        self.DateLabel = QLabel(self)
        self.DateLabel.setAlignment(Qt.AlignCenter)
        self.DateLabel.setStyleSheet('border:none;font-size:14px;')
        self.TimeLabel = QLabel(self)
        self.TimeLabel.setAlignment(Qt.AlignCenter)
        self.TimeLabel.setStyleSheet('border:none; border-bottom:1px solid white;font-size:22px;')
        self.DateLabel.setText(QDate.currentDate().toString())
        self.TimeLabel.setText(QTime.currentTime().toString())
        self.photoLabel = QLabel(self)
        self.photoLabel.setFixedSize(int(self.__config.get_picture_value("weight")),
                                     int(self.__config.get_picture_value("height")))
        self.photoLabel.setAlignment(Qt.AlignCenter)
        self.photoLabel.setStyleSheet('border:1px solid darkGray; ')
        hLayout = QHBoxLayout(self)
        hLayout.addSpacing(5)
        hLayout.addWidget(self.photoLabel)
        self.studentNoLabel = QLineEdit(self)
        self.studentNoLabel.setAlignment(Qt.AlignLeft)
        self.studentNoLabel.setFocusPolicy(Qt.NoFocus)
        self.studentNoLabel.setText("学号：")
        self.studentNoLabel.setStyleSheet('font-size:14px;')
        self.studentNameLabel = QLineEdit(self)
        self.studentNameLabel.setAlignment(Qt.AlignLeft)
        self.studentNameLabel.setFocusPolicy(Qt.NoFocus)
        self.studentNameLabel.setText("姓名：")
        self.studentNameLabel.setStyleSheet('font-size:14px;')
        self.tempLabel = QLineEdit(self)
        self.tempLabel.setAlignment(Qt.AlignLeft)
        self.tempLabel.setFocusPolicy(Qt.NoFocus)
        self.tempLabel.setText("体温：")
        self.tempLabel.setStyleSheet('font-size:14px;')
        vLayout = QVBoxLayout(self)
        vLayout.addSpacing(20)
        vLayout.addWidget(self.TimeLabel)
        vLayout.addWidget(self.DateLabel)
        vLayout.addStretch(1)
        vLayout.addLayout(hLayout)
        vLayout.addSpacing(55)
        vLayout.addWidget(self.studentNameLabel)
        vLayout.addWidget(self.studentNoLabel)
        vLayout.addWidget(self.tempLabel)
        vLayout.addStretch(1)
        self.mlayout.addWidget(self.displayLabel)
        self.mlayout.addLayout(vLayout)
        self.mlayout.setSpacing(10)
        self.mlayout.setContentsMargins(0,0,10,0)
        self.setLayout(self.mlayout)
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.timer = QTimer()
        self.timer.start()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.start_camera)
        self.oneSectimer = QTimer()
        self.oneSectimer.setInterval(1000)
        self.oneSectimer.timeout.connect(self.refresh_time)
        self.oneSectimer.start()
        self.timecount=0

    def quit(self):
        try:
            self.log.terminate()
            self.cap.release()
            self.close()
        except KeyboardInterrupt:
            self.log.terminate()
            self.close()

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
            self.timecount = 0

    def find_face_location(self, image, small_image):
        locations = self.__face.get_face_locations(small_image, number_of_times_to_upsample=0, model=self.__model)
        if len(locations) > 0:
            for (top, right, bottom, left) in locations:
                cv.rectangle(image, (left*2, top*2), (right*2, bottom*2), (0, 255, 0), 2)
            self.bind_player(image)
            self.find_student(small_image, locations)
        else:
            self.bind_player(image)

    def bind_result(self, info):
        image = Image.open(os.path.join(self.__thumbnail_path, info["PictureName"]))
        img = ImageQt.ImageQt(image)
        self.photoLabel.setPixmap(
            QPixmap.fromImage(img).scaled(self.photoLabel.width(), self.photoLabel.height()))
        self.studentNameLabel.setText("姓名：" + info["Name"])
        self.studentNoLabel.setText("学号：" + info["StudentNo"])
        self.tempLabel.setText("体温： 36.1")

    def refresh_time(self):
        self.DateLabel.setText(QDate.currentDate().toString())
        self.TimeLabel.setText(QTime.currentTime().toString())
        if self.timecount < 5:
            self.timecount +=1

    def bind_player(self, image):
        image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
        img = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
        self.displayLabel.setPixmap(
            QPixmap.fromImage(img))
        if self.timecount >= 5:
            self.photoLabel.clear()
            self.studentNoLabel.setText("学号：" )
            self.studentNameLabel.setText("姓名：")
            self.tempLabel.setText("体温：")

    def start_camera(self):
        try:
            success, image = self.cap.read()
            if success:
                # image = cv.flip(image, -1)
                picture = cv.cvtColor(image, cv.COLOR_BGR2RGB)
                small_image = cv.resize(picture, (0, 0), fx=0.5, fy=0.5)
                small_image = small_image[:, :, ::-1]
                self.find_face_location(image, small_image)
        except KeyboardInterrupt:
            pass


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


def upgrade_system():

    try:

        # init path

        db_folder_name = ConfigManager().get_app_value("db_folder_name")
        picture_folder_name = ConfigManager().get_app_value("picture_folder_name")
        db_path = ConfigManager().get_path_value("db")
        picture_path = ConfigManager().get_path_value("picture")

        # get directory
        device = sp.getoutput("df -h | grep '/media/' | awk -F '/media/' '{print $2}'")

        if len(device) > 0:
            directory = sp.getoutput("find /media -maxdepth 2 -type d -name '{}'".format(device))

            if len(directory) > 0:
                db_path_new = os.path.join(directory, db_folder_name)
                picture_path_new = os.path.join(directory, picture_folder_name)

                if os.path.exists(db_path_new) and os.path.exists(picture_path_new):
                    shutil.rmtree(db_path, ignore_errors=False)
                    shutil.rmtree(picture_path, ignore_errors=False)
                    shutil.move(db_path_new, db_path)
                    shutil.move(picture_path_new, picture_path)

    except Exception as error:
        print("replace db and picture error - {}".format(error))


def init_feature():

    try:

        if Student().init_feature():
            print('Feature initialization completed!')
        else:
            print('Feature initialization failed!')
    except Exception as error:
        logging.error(error)


if __name__ == '__main__':

    setproctitle.setproctitle("MISApplication")

    app = QApplication(sys.argv)
    splash_pix = QPixmap('./source/loading.jpeg')
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
    splash.show()

    splash.showMessage("<h1><font color='#ffffff'>Loading Feature</font></h1>", Qt.AlignBottom | Qt.AlignLeft, Qt.black)
    init_feature()

    splash.showMessage("<h1><font color='#ffffff'>Loading System</font></h1>", Qt.AlignBottom | Qt.AlignLeft, Qt.black)
    app.processEvents()

    q = mp.Queue()
    splash.showMessage("<h1><font color='#ffffff'>Loading Service</font></h1>", Qt.AlignBottom | Qt.AlignLeft, Qt.black)
    scheduler = LogService(q)

    app.setOverrideCursor(Qt.BlankCursor)
    splash.showMessage("<h1><font color='#ffffff'>Loading Application</font></h1>",
                       Qt.AlignBottom | Qt.AlignLeft, Qt.black)
    w = MainWindow(scheduler, q)
    w.show()
    time.sleep(1)
    splash.finish(w)
    splash.deleteLater()
    app.exec_()
