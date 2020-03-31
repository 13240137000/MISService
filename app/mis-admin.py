from tkinter import *
import cv2 as cv
from core.db.business import Student, Log
from core.face.helper import FaceHelper
from PIL import Image, ImageTk


class UserInterface(object):

    __student = Student()
    __face = FaceHelper()
    __log = Log()

    def __init__(self):

        # connection to camera and set size
        self.cap = cv.VideoCapture(0)
        self.cap.set(3, 480)
        self.cap.set(4, 480)
        self.cap.set(5, 200)

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
        self.cap.release()
        self.main_window.quit()

    def find_student(self, image, locations):

        if len(locations) > 0:

            info = self.__student.get_student_by_picture(None, image, locations)

            if len(info) > 0:
                print(info)
                self.bind_result(info)

    def find_face_location(self, image, small_image):

        locations = self.__face.get_face_locations(small_image, number_of_times_to_upsample=0, model="hog")

        if len(locations) > 0:

            for (top, right, bottom, left) in locations:
                cv.rectangle(image, (left*4, top*4), (right*4, bottom*4), (0, 255, 0), 2)

            self.bind_player(image)

            self.find_student(small_image, locations)
            # Process(target=find_student, args=(origin_image, locations)).start()
        else:
            self.bind_player(image)

    def bind_result(self, info):

        image = Image.open(r"/Users/jack/Desktop/MISService/Thumbnail/" + info[0]["PictureName"])
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

        while True:

            success, image = self.cap.read()

            if success:
                image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
                small_image = cv.resize(image, (0, 0), fx=0.25, fy=0.25)
                small_image = small_image[:, :, ::-1]

                # self.bind_player(image)
                self.find_face_location(image, small_image)


if __name__ == '__main__':

    UserInterface().start()
