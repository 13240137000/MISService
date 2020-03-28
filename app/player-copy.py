import asyncio
import functools
from tkinter import *
import cv2 as cv
from core.db.business import Student, Log
from core.face.helper import FaceHelper
from PIL import Image, ImageTk


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
main_window.geometry("800x480")

# load frame and control
frm_camera = Frame(main_window, width=480, height=480, bg="green")
frm_info = Frame(main_window, width=320, height=480, bg="yellow")

lbl_player = Label(frm_camera, bg='gray')

pnl_photo = Canvas(frm_info, width=300, height=300, bg="blue").pack(anchor="center", padx=10, side=TOP)
lbl_student_name = Label(frm_info, text="姓名：").pack(side=LEFT, padx=10, pady=10)
lbl_student_no = Label(frm_info, text="学号：").pack(side=RIGHT, padx=10, pady=10)

frm_camera.pack(side=LEFT)
frm_info.pack(side=RIGHT)


def callback(info, image, task):

    print("1"*10)
    # if len(info) > 0:
    #
    #     image = Image.fromarray(image)
    #     image_tk = ImageTk.PhotoImage(image=image)
    #     lbl_player.imgtk = image_tk
    #     lbl_player.config(image=image_tk)
    #     lbl_player.pack()
    #     lbl_player.update()


def insert_log(student_id, temperature, status):
    __log.insert(student_id, temperature, status)


def __find_face(image):
    return __face.get_face_locations(image)


async def find_student(image):

    print("find_student")

    # locations = __find_face(image)
    #
    # if len(locations) > 0:
    #
    #     info = __student.get_student_by_picture(None, image, locations)
    #
    #     for (top, right, bottom, left) in locations:
    #         cv.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
    # else:
    #     info = []
    #
    # return info, image


async def start_camera():
    print("c")
    while True:
        success, img = cap.read()

        if success:
            job = find_student(cv.cvtColor(img, cv.COLOR_BGR2RGB))
            task = asyncio.create_task(job)
            task.add_done_callback(functools.partial(callback))
            await asyncio.sleep(0.05)


async def start_ui():
    print("b")
    main_window.mainloop()
    print("a")


async def tasks():
    jobs = [start_ui(), start_camera()]
    await asyncio.gather(*jobs, return_exceptions=True)

asyncio.get_event_loop().run_until_complete(tasks())

# release all
cap.release()
cv.destroyAllWindows()
