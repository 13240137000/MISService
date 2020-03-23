import logging
from .helper import SqliteHelper
from .script import *


class Student(object):

    __db = SqliteHelper()

    def __get_students(self) -> list:

        try:
            sql = StudentScript.get_all
            students = self.__db.execute(sql, result_dict=True)
        except Exception as error:
            logging.error(error)

        return students

    def __update_feature(self):
        pass

    def init_feature(self):

        students = self.__get_students()

        for s in students:
            print(s)




class Class(object):
    pass


class StudentFeatures(object):
    pass


class ClassStudent(object):
    pass

