import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tkinter import *
import cv2 as cv
from core.db.business import Student, Log
from core.face.helper import FaceHelper
from conf.admin import ConfigManager
from PIL import Image, ImageTk
from multiprocessing import Queue, Process


class UserInterface(object):

    __logs = Queue()
    __student = Student()
    __face = FaceHelper()
    __log = Log()
    __config = ConfigManager()
    __thumbnail_path = __config.get_path_value("thumbnail")
    __current_student_no = ""

    def __init__(self):

        self.cap = cv.VideoCapture(r'/Users/jack/Desktop/MISService/MISService/images/jw.mp4')
        # self.cap = cv.VideoCapture(0)
        self.cap.set(3, int(self.__config.get_capture_value("width")))
        self.cap.set(4, int(self.__config.get_capture_value("height")))

        self.main_window = Tk()
        self.main_window.title('MIS Service')
        self.frm_camera = Frame(self.main_window, width=480, height=480, bg="green")
        self.frm_info = Frame(self.main_window, width=320, height=480, bg="yellow")
        self.lbl_player = Label(self.frm_camera, bg='gray')
        self.pnl_photo = Label(self.frm_info, bg="blue")
        self.frm_camera.pack(side=LEFT)
        self.frm_info.pack(side=RIGHT)
        self.btn_start = Button(self.frm_info, text="启动", command=self.start_camera).pack()
        self.btn_quit = Button(self.frm_info, text="退出", command=self.quit).pack()

    def start(self):
        self.main_window.mainloop()

    def quit(self):
        try:
            self.cap.release()
            self.main_window.quit()
        except KeyboardInterrupt:
            self.main_window.quit()

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
                    self.bind_result(info)
                    self.__current_student_no = info["StudentNo"]
                    self.insert_log_and_sent_sms(info)

    def find_face_location(self, image, small_image):

        locations = self.__face.get_face_locations(small_image, number_of_times_to_upsample=0, model="hog")
        if len(locations) > 0:
            for (top, right, bottom, left) in locations:
                cv.rectangle(image, (left*4, top*4), (right*4, bottom*4), (0, 255, 0), 2)
            self.bind_player(image)
            self.find_student(small_image, locations)

        else:

            self.bind_player(image)

    def bind_result(self, info):

        image = Image.open(os.path.join(self.__thumbnail_path, info["PictureName"]))
        image_tk = ImageTk.PhotoImage(image=image)
        self.pnl_photo.imgtk = image_tk
        self.pnl_photo.config(image=image_tk)
        self.pnl_photo.pack()
        self.pnl_photo.update()
        self.pnl_photo.update_idletasks()

    def bind_player(self, image):

        image = Image.fromarray(image)
        image_tk = ImageTk.PhotoImage(image=image)
        self.lbl_player.imgtk = image_tk
        self.lbl_player.config(image=image_tk)
        self.lbl_player.pack()
        self.lbl_player.update()

    def start_camera(self):
        loop = 0
        try:
            while True:
                success, image = self.cap.read()
                if success:
                    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
                    small_image = cv.resize(image, (0, 0), fx=0.25, fy=0.25)
                    small_image = small_image[:, :, ::-1]
                    if loop % 3 == 0:
                        self.find_face_location(image, small_image)
                    else:
                        self.bind_player(image)
                    loop += 1
                    if loop >= 999:
                        loop = 0
        except KeyboardInterrupt:
            pass


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

    UserInterface().start()
