import logging
import numpy as np
import face_recognition as fr
import cache.vars as gv

class FaceHelper(object):

    def get_face_locations(self, picture, number_of_times_to_upsample=1, model="hog"):
        return fr.face_locations(picture, number_of_times_to_upsample=1, model="hog")

    def get_face_encodings(self, picture, locations):
        return fr.face_encodings(picture, locations)

    def load_picture(self, picture):
        return fr.load_image_file(picture)

    def get_feature(self, picture):
        result = ""
        try:

            if not len(fr.face_encodings(fr.load_image_file(picture))) == 0:
                result = fr.face_encodings(fr.load_image_file(picture))[0]

        except Exception as error:
            logging.error(error)

        return result

    def compare(self, picture, student_feature, student_nos, image=None, locations=None) ->list:
        student_no = ""
        try:

            # get features
            features = []

            if gv.get_value("features_list") is None:
                for feature in student_feature:
                    feature = str(feature).split(",")
                    features.append(np.array(feature, dtype=np.float).reshape((128,)))
                gv.set_value("features_list", features)
            else:
                features = list(gv.get_value("features_list"))

            # get locations and encodings
            if image is None and locations is None:
                picture = self.load_picture(picture)
                locations = self.get_face_locations(picture)
            else:
                picture = image
                locations = locations

            if len(locations) == 0:
                return student_no

            encodings = self.get_face_encodings(picture, locations)

            # compare
            for encoding in encodings:

                match = fr.compare_faces(features, encoding, tolerance=0.37)

                if match.count(True) > 0:
                    student_no = student_nos[match.index(True)]
                else:
                    student_no = ""

        except Exception as error:
            logging.error(error)

        return student_no

