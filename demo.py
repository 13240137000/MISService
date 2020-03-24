import face_recognition
import cv2
import numpy as np


# This is a demo of running face recognition on a video file and saving the results to a new video file.
#
# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Open the input movie file
from core.db.business import Student

input_movie = cv2.VideoCapture(r"images/jw.mp4")
# length = int(input_movie.get(cv2.CAP_PROP_FRAME_COUNT))

# Create an output movie file (make sure resolution/frame rate matches input video!)
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# output_movie = cv2.VideoWriter('output.avi', fourcc, 29.97, (640, 360))

# Load some sample pictures and learn how to recognize them.
# jack_face_encoding = face_recognition.face_encodings(face_recognition.load_image_file(r"images/jack.jpg"))[0]
#
# wubo_face_encoding = face_recognition.face_encodings(face_recognition.load_image_file(r"images/wubo.png"))[0]

s = Student()
students = s.get_students()
student_name, student_feature, student_no = s.get_name_feature_and_nos(students)

# known_faces = [
#     face_recognition.face_encodings(face_recognition.load_image_file(r"images/jack.jpg"))[0],
#     face_recognition.face_encodings(face_recognition.load_image_file(r"images/wubo.png"))[0]
# ]

# names = [
#     'Jack',
#     'Wu Bo'
# ]

features = []

for feature in student_feature:
    feature = str(feature).split(",")
    features.append(np.array(feature, dtype=np.float).reshape((128,)))



# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
frame_number = 0

while True:
    # Grab a single frame of video
    ret, frame = input_movie.read()
    frame_number += 1

    # Quit when the input video file ends
    if not ret:
        break

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_frame = frame[:, :, ::-1]

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_frame)

    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    face_names = []

    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)

        match = face_recognition.compare_faces(features, face_encoding, tolerance=0.4)

        # If you had more than 2 faces, you could make this logic a lot prettier
        # but I kept it simple for the demo

        # name = None
        # if match[0]:
        #     name = "Jack"
        # elif match[1]:
        #     name = "Wu bo"

        if match.count(True) > 0:
            name = student_no[match.index(True)]
        else:
            name = ""

        face_names.append(name)

    # Label the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):

        if not name:
            continue

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 25), (right, bottom), (0, 255, 0), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 0, 0), 1)

    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Write the resulting image to the output video file
    # print("Writing frame {} / {}".format(frame_number, length))
    # output_movie.write(frame)

# All done!
input_movie.release()
cv2.destroyAllWindows()