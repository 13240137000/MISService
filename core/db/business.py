import face_recognition as fr
import logging
import os
from .helper import SqliteHelper
from .script import *
from conf.admin import ConfigManager


class Student(object):

    __db = SqliteHelper()
    __config = ConfigManager()

    __fail_list = []
    __success_list = []

    def __get_students(self) -> list:

        try:

            sql = StudentScript.get_all
            students = self.__db.execute(sql, result_dict=True)

        except Exception as error:
            logging.error(error)

        return students

    def __update_feature(self):

        try:

            for s in self.__success_list:
                feature_id = s["FeatureID"]
                feature = s["Feature"]
                # update feature
                sql = StudentFeaturesScript.update.format(feature, feature_id)
                self.__db.execute(sql)
                # update student
                student_id = s["StudentID"]
                sql = StudentScript.update.format(1, student_id)
                self.__db.execute(sql)

        except Exception as error:
            logging.error(error)

    def __get_feature(self, picture):

        result = ""

        try:

            if not len(fr.face_encodings(fr.load_image_file(picture))) == 0:
                result = fr.face_encodings(fr.load_image_file(picture))[0]

        except Exception as error:
            logging.error(error)

        return result

    def init_feature(self) -> bool:

        result = True

        try:

            students = self.__get_students()
            picture_path = self.__config.get_path_value("picture")

            # get picture code.
            for s in students:

                if s["PictureName"]:

                    picture = os.path.join(picture_path, s["PictureName"])
                    feature = self.__get_feature(picture)

                    if len(feature) == 0:
                        self.__fail_list.append({"StudentID": s["StudentID"], "Name": s["Name"],
                                                 "StudentNo": s["StudentNo"], "Picture": s["PictureName"]})
                    else:
                        self.__success_list.append({"StudentID": s["StudentID"], "FeatureID": s["FeatureID"],
                                                    "Feature": feature})

            if len(self.__success_list) > 0:
                self.__update_feature()

        except Exception as error:
            result = False
            logging.error(error)

        return result


class Class(object):
    pass


class StudentFeatures(object):
    pass


class ClassStudent(object):
    pass

