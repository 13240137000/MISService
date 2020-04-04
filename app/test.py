from tkinter import *
import multiprocessing as mp
import time
import os


class EndUser(object):

    def __init__(self, log):

        self.root = Tk()
        self.log = log

    def start(self):

        print("The end user has been started, pid is {}, process name is {}, current process is {}".format(
            mp.Process.pid, mp.Process.name, mp.current_process()))
        self.log.start()
        self.root.mainloop()


class LogService(mp.Process):

    def __init__(self, tasks):
        super(LogService, self).__init__()
        self.tasks = tasks

    def run(self):
        print("The log service has been started, pid is {}, process name is {}, current process is {}".format(mp.Process.pid, mp.Process.name, mp.current_process()))

        while 1:
            time.sleep(10)


if __name__ == '__main__':

    q = mp.Queue()
    service = LogService(q)

    EndUser(service).start()
