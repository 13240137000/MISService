from multiprocessing import Process
from tkinter import *


def job():

    for i in range(1):
        print("job started.")


if __name__ == '__main__':

    t = Tk()

    p = Process(target=job)
    p.start()
    p.join()

    m = Process(target=t.mainloop)
    m.start()
    m.join()


