import logging
import os
import re
import time
import datetime
from .helper import SqliteHelper
from .script import *
from conf.admin import ConfigManager
from core.face.helper import FaceHelper
from core.image.helper import ImageHelper


class Student(object):

    __db = SqliteHelper()
    __config = ConfigManager()
    __face = FaceHelper()
    __image = ImageHelper()

    __fail_list = []
    __success_list = []

    def __get_students(self) -> list:

        try:

            sql = StudentScript.get_all.format(0)
            students = self.__db.execute(sql, result_dict=True)

        except Exception as error:
            logging.error(error)

        return students

    def __get_student_by_no(self, student_no) -> list:

        try:

            sql = StudentScript.get_student_by_no.format(student_no)
            student = self.__db.execute(sql, result_dict=True)

        except Exception as error:
            logging.error(error)

        return student

    def get_name_feature_and_nos(self, students) -> list:
        # student_name = []
        student_feature = []
        student_no = []

        try:

            for s in students:
                # student_name.append(s["Name"])
                student_feature.append(s["Feature"])
                student_no.append(s["StudentNo"])

        except Exception as error:
            logging.error(error)

        return student_feature, student_no

    def init_feature(self) -> bool:
        result = True

        try:

            students = self.__get_students()
            picture_path = self.__config.get_path_value("picture")

            for s in students:
                if s["PictureName"]:
                    picture = os.path.join(picture_path, s["PictureName"])
                    feature = self.__face.get_feature(picture)

                    if len(feature) == 0:
                        self.__fail_list.append({"StudentID": s["StudentID"], "Name": s["Name"],
                                                 "StudentNo": s["StudentNo"], "Picture": s["PictureName"]})
                    else:
                        self.__success_list.append({"StudentID": s["StudentID"], "FeatureID": s["FeatureID"],
                                                    "Feature": feature})
                        self.__image.resize(s["PictureName"])

            if len(self.__success_list) > 0:
                StudentFeatures().update_feature(self.__success_list)

            if len(self.__fail_list) > 0:
                StudentFeatures().update_error_feature(self.__fail_list)

        except Exception as error:
            result = False
            logging.error(error)

        return result

    def get_error_feature(self) -> list:
        try:

            sql = ErrorScript.get_all
            students = self.__db.execute(sql, result_dict=True)

        except Exception as error:
            logging.error(error)

        return students

    def get_students(self):
        try:

            sql = StudentScript.get_all.format(1)
            students = self.__db.execute(sql, result_dict=True)

        except Exception as error:
            logging.error(error)

        return students

    def get_student_by_picture(self, picture, image=None, locations=None):
        result = []

        try:

            # get students
            students = self.get_students()
            student_feature, student_nos = self.get_name_feature_and_nos(students)

            # find student no
            student_no = self.__face.compare(picture, student_feature, student_nos, image, locations)

            # get student
            if len(student_no) > 0:
                result = self.__get_student_by_no(student_no)
            else:
                result = []

        except Exception as error:
            logging.error("Get student by picture error - {}".format(error))

        return result


class StudentFeatures(object):
    __db = SqliteHelper()

    def update_feature(self, success_list):

        try:

            for s in success_list:

                feature_id = s["FeatureID"]
                feature = s["Feature"]

                # update feature
                feature = re.sub(' +', ',', str(feature)).replace("\n", "").replace("[", "").replace("]", "")
                sql = StudentFeaturesScript.update.format(feature, feature_id)
                self.__db.execute(sql)

                # update student
                student_id = s["StudentID"]
                sql = StudentScript.update.format(1, student_id)
                self.__db.execute(sql)

        except Exception as error:
            logging.error("update feature - {}".format(error))

    def update_error_feature(self, error_list):

        try:

            if len(error_list) > 0:
                sql = ErrorScript.delete
                self.__db.execute(sql)

            for s in error_list:
                student_id = s["StudentID"]
                sql = ErrorScript.update.format(student_id)
                self.__db.execute(sql)
        except Exception as error:
            logging.error("update error - {}".format(error))


class Log(object):

    __db = SqliteHelper(db_name="log.db")
    __config = ConfigManager()

    def get_all(self) -> list:

        try:

            sql = LogScript.get_all
            logs = self.__db.execute(sql, result_dict=True)

        except Exception as error:
            logging.error("log get all - {}".format(error))

        return logs

    def insert(self, student_id, student_no, student_name, temperature, status, is_sent_sms, mobile) -> bool:

        result = True

        try:

            log_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            sql = LogScript.insert.format(student_id, student_no, student_name, temperature, log_time, status,
                                          is_sent_sms, mobile)
            self.__db.execute(sql)

        except Exception as error:
            result = False
            logging.error("log insert - {}".format(error))

        return result

    def delete(self) -> bool:

        result = True

        try:

            sql = LogScript.delete
            self.__db.execute(sql)

        except Exception as error:
            result = False
            logging.error("log delete - {}".format(error))

        return result

    def total_record_by_minutes(self, student_id):
        result = []
        try:
            minutes = int(self.__config.get_sms_value("expire"))
            start_time = (datetime.datetime.now()-datetime.timedelta(minutes=minutes)).strftime("%Y-%m-%d %H:%M:%S")
            end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            sql = LogScript.total_record_by_minutes.format(start_time, end_time, student_id)
            result = self.__db.execute(sql)
        except Exception as error:
            logging.error("total record by minutes - {}".format(error))

        return result


