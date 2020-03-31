from tkinter import *
import cv2 as cv
from core.db.business import Student, Log
from core.face.helper import FaceHelper
from PIL import Image, ImageTk
import time
from multiprocessing import Process, Pool, Queue, JoinableQueue
import threading

# init business objects
__student = Student()
__face = FaceHelper()
__log = Log()

# connection to camera and set size
cap = cv.VideoCapture(r"/Users/jack/Desktop/MISService/MISService/images/jw.mp4")
cap.set(3, 480)
cap.set(4, 480)
cap.set(5, 200)

# load main window
main_window = Tk()
main_window.title('MIS Service')
# main_window.geometry("800x480")


# load frame and control
frm_camera = Frame(main_window, width=480, height=480, bg="green")
frm_info = Frame(main_window, width=320, height=480, bg="yellow")
lbl_player = Label(frm_camera, bg='gray')
pnl_photo = Label(frm_info, bg="blue")


frm_camera.pack(side=LEFT)
frm_info.pack(side=RIGHT)


def insert_log(student_id, temperature, status):
    __log.insert(student_id, temperature, status)


def __find_face(image):

    return __face.get_face_locations(image, number_of_times_to_upsample=0, model="hog")


def find_face_location(image):

    origin_image = image

    locations = __find_face(image)

    if len(locations) > 0:

        for (top, right, bottom, left) in locations:
            cv.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)

        bind_player(image)
        find_student(origin_image, locations)
        # Process(target=find_student, args=(origin_image, locations)).start()


def find_student(image, locations):

    if len(locations) > 0:

        info = __student.get_student_by_picture(None, image, locations)

        if len(info) > 0:
            print(info)
            bind_result(info)


def bind_result(info):

    image = Image.open(r"/Users/jack/Desktop/MISService/Thumbnail/" + info[0]["PictureName"])
    image_tk = ImageTk.PhotoImage(image=image)
    pnl_photo.imgtk = image_tk
    pnl_photo.config(image=image_tk)
    pnl_photo.pack()
    pnl_photo.update()
    pnl_photo.update_idletasks()


def bind_player(image):

    image = Image.fromarray(image)
    image_tk = ImageTk.PhotoImage(image=image)
    lbl_player.imgtk = image_tk
    lbl_player.config(image=image_tk)
    lbl_player.pack()
    # lbl_player.update_idletasks
    lbl_player.update()


def start_camera():
    l = 1
    while True:
        success, image = cap.read()

        if success:
            image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
            bind_player(image)

            if l % 50 == 0:
                find_face_location(image)
            # Process(target=find_face_location, args=(image,)).start()
        time.sleep(0.1)
        l = l + 1


def quit_camera():
    main_window.quit()


btn_start = Button(frm_info, text="启动", command=start_camera).pack()
btn_start = Button(frm_info, text="退出", command=quit_camera).pack()

if __name__ == "__main__":

    # pool = Pool(processes=4)

    # mp = Process(target=start_camera, name="MainProcess")
    # mp.daemon = True
    # mp.start()
    # mp.join()

    # threading.Thread(target=start_camera, name="MainThread").start()

    try:
        main_window.mainloop()
        cap.release()
        cv.destroyAllWindows()
    except KeyboardInterrupt as error:
        main_window.quit()
