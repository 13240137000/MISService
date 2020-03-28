from tkinter import *
import cv2 as cv
from core.db.business import Student, Log
from core.face.helper import FaceHelper
from PIL import Image, ImageTk
import threading
import time

# init business objects
__student = Student()
__face = FaceHelper()
__log = Log()

# connection to camera and set size
cap = cv.VideoCapture(0)
cap.set(3, 480)
cap.set(4, 480)

# load main window
main_window = Tk()
main_window.title('MIS Service')
# main_window.geometry("800x480")

# load frame and control
frm_camera = Frame(main_window, width=480, height=480, bg="green")
frm_info = Frame(main_window, width=320, height=480, bg="yellow")
lbl_player = Label(frm_camera, bg='gray')
pnl_photo = Label(frm_info, bg="blue")
lbl_student_name = Label(frm_info, text="姓名：").pack(side=LEFT, padx=10, pady=10)
lbl_student_no = Label(frm_info, text="学号：").pack(side=RIGHT, padx=10, pady=10)

frm_camera.pack(side=LEFT)
frm_info.pack(side=RIGHT)

lock = threading.Lock()


def insert_log(student_id, temperature, status):
    __log.insert(student_id, temperature, status)


def __find_face(image):
    return __face.get_face_locations(image)


def find_face_location(image):

    origin_image = image

    locations = __find_face(image)

    if len(locations) > 0:

        for (top, right, bottom, left) in locations:
            cv.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)

        bind_player(image)

        threading.Thread(target=find_student, args=(origin_image, locations)).start()


def find_student(image, locations):

    if len(locations) > 0:

        info = __student.get_student_by_picture(None, image, locations)

        if len(info) > 0:
            bind_result()


def bind_result():

    image = Image.open(r"/Users/jack/Desktop/MISService/Picture/success.png")
    image_tk = ImageTk.PhotoImage(image=image)
    pnl_photo.imgtk = image_tk
    pnl_photo.config(image=image_tk)
    pnl_photo.pack()
    pnl_photo.update()
    pnl_photo.update_idletasks()


def bind_player(image):

    image = Image.fromarray(image)
    image_tk = ImageTk.PhotoImage(image=image)
    lock.acquire()
    lbl_player.imgtk = image_tk
    lbl_player.config(image=image_tk)
    lbl_player.pack()
    lbl_player.update_idletasks
    lbl_player.update()
    lock.release()


def start_camera():

    while True:

        success, image = cap.read()

        if success:
            image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
            threading.Thread(target=bind_player, args=(image,)).start()
            threading.Thread(target=find_face_location, args=(image,)).start()
        time.sleep(0.1)


if __name__ == "__main__":

    threading.Thread(target=start_camera).start()

    try:
        main_window.mainloop()
        cap.release()
        cv.destroyAllWindows()
    except KeyboardInterrupt as error:
        main_window.quit()
