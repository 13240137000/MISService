import os
import cv2 as cv
import face_recognition as fr
from tkinter import *
from core.db.business import Student
from conf.admin import ConfigManager
from PIL import Image, ImageTk
import asyncio

__student = Student()
__config = ConfigManager()

# dim main window
main_window = Tk()
main_window.title('MIS Service')
main_window.geometry("800x480")

# dim control
frm_camera = Frame(main_window, width=480, height=480, bg="green")
frm_info = Frame(main_window, width=320, height=480, bg="yellow")

player = Label(frm_camera, bg='gray')

pnl_photo = Canvas(frm_info, width=300, height=300, bg="blue").pack(anchor="center", padx=10, side=TOP)
lbl_student_name = Label(frm_info, text="姓名：").pack(side=LEFT, padx=10, pady=10)
lbl_student_no = Label(frm_info, text="学号：").pack(side=RIGHT, padx=10, pady=10)

frm_camera.pack(side=LEFT)
frm_info.pack(side=RIGHT)

# open capture

cap = cv.VideoCapture(0)
cap.set(3, 480)
cap.set(4, 480)


def loop():

    success, frame = cap.read()

    if success:

        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

        face_locations = fr.face_locations(frame)

        if len(face_locations) > 0:

            ret = __student.get_student_by_picture(None, frame, face_locations)

            if len(ret) > 0:
                picture_path = os.path.join(__config.get_path_value("picture"), ret[0]["PictureName"])
                print(picture_path)

        for (top, right, bottom, left) in face_locations:
            cv.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        image = Image.fromarray(frame)
        image_tk = ImageTk.PhotoImage(image=image)
        player.imgtk = image_tk
        player.config(image=image_tk)
        player.pack()
        main_window.after(1, loop)


loop()
main_window.mainloop()

cap.release()
cv.destroyAllWindows()



