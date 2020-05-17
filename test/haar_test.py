import cv2

path = r"/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/cv2/data/haarcascade_frontalface_default.xml"
image_path = r"/Users/jack/Desktop/MISService/Picture/20200003.jpg"

img = cv2.imread(image_path, 1)

face_engine = cv2.CascadeClassifier(path)

faces = face_engine.detectMultiScale(img,scaleFactor=1.3, minNeighbors=5)

for (x,y,w,h) in faces:
    img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

cv2.imshow('img', img)
cv2.waitKey(0)
cv2.destroyAllWindows()