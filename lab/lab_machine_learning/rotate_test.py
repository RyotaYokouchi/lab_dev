import cv2
import dlib#@UnresolvedImport
import time
from scipy import ndimage

# 画像の取得と顔の検出
img = cv2.imread("/Users/yokouchiryouta/Desktop/顔データ/検証用画像データ/オリジナル/Ryota_test.jpg")
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cascade_face_file = '/usr/local/opt/opencv/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml'
cascade_eye_file = '/usr/local/opt/opencv/share/OpenCV/haarcascades/haarcascade_eye.xml'
cascade_mouth_file = '/usr/local/opt/opencv/share/OpenCV/haarcascades/haarcascade_mcs_mouth.xml'
cascade_nose_file = '/usr/local/opt/opencv/share/OpenCV/haarcascades/haarcascade_mcs_nose.xml'
face_cascade = cv2.CascadeClassifier(cascade_face_file)
eye_cascade = cv2.CascadeClassifier(cascade_eye_file)
mouth_cascade = cv2.CascadeClassifier(cascade_mouth_file)
nose_cascade = cv2.CascadeClassifier(cascade_nose_file)

# 顔検出する
if face_cascade:
    face_list = face_cascade.detectMultiScale(img_gray, minNeighbors=10, minSize=(100, 100))
if eye_cascade:
    eye_list = eye_cascade.detectMultiScale(img_gray, minNeighbors=10, minSize=(70, 70))
if mouth_cascade:
    mouth_list = mouth_cascade.detectMultiScale(img_gray, minNeighbors=10, minSize=(70, 70))
if nose_cascade:
    nose_list = nose_cascade.detectMultiScale(img_gray, minNeighbors=10, minSize=(70, 70))

# -15 ~ 15のリスト
rotate_list = list(range(-15, 15))
img_list = []

for rotate_value in rotate_list:
    rotate_img = ndimage.rotate(img, rotate_value)
    rotate_img_gray = cv2.cvtColor(rotate_img, cv2.COLOR_BGR2GRAY)
    face_list = face_cascade.detectMultiScale(rotate_img_gray, minNeighbors=10, minSize=(100, 100))
    if face_list is not None:
        for (x, y, w, h) in face_list:
            pen_w = 3
            cv2.rectangle(rotate_img, (x, y), (x+w, y+h), (255, 255, 255), thickness = pen_w)

    # フレーム表示
    cv2.imshow("rotate_" + str(rotate_value), rotate_img)

cv2.waitKey(0)
# 終了処理
cv2.destroyAllWindows()
