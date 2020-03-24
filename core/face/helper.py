import logging
import numpy as np
import face_recognition as fr


class FaceHelper(object):

    def __get_face_locations(self, picture):
        return fr.face_locations(picture)

    def __get_face_encodings(self, picture, locations):
        return fr.face_encodings(picture, locations)

    def __load_picture(self, picture):
        return fr.load_image_file(picture)

    def get_feature(self, picture):
        result = ""
        try:

            if not len(fr.face_encodings(fr.load_image_file(picture))) == 0:
                result = fr.face_encodings(fr.load_image_file(picture))[0]

        except Exception as error:
            logging.error(error)

        return result

    def compare(self, picture, student_feature, student_nos) ->list:
        try:

            # get features
            features = []
            for feature in student_feature:
                feature = str(feature).split(",")
                features.append(np.array(feature, dtype=np.float).reshape((128,)))

            # get locations and encodings
            picture = self.__load_picture(picture)
            locations = self.__get_face_locations(picture)
            encodings = self.__get_face_encodings(picture, locations)

            # compare
            for encoding in encodings:

                match = fr.compare_faces(features, encoding, tolerance=0.4)

                if match.count(True) > 0:
                    student_no = student_nos[match.index(True)]
                else:
                    student_no = ""

        except Exception as error:
            logging.error(error)

        return student_no

