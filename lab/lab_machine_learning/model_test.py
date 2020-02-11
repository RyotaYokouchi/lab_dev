'''
LOAD MODEL AND PREDICT
'''
from __future__ import print_function
import tensorflow.keras
from tensorflow.keras.models import load_model
import numpy as np
import cv2
import os
from natsort import natsorted

model = load_model('MyModel.h5')
dir_path = "/Users/yokouchiryouta/Desktop/顔データ/検証用画像データ/顔領域/"

face_img_names = os.listdir(dir_path)

for file_name in natsorted(face_img_names):
    face_img = cv2.imread(dir_path + file_name)
    #face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
    face_img = np.array(face_img)
    face_img = np.resize(face_img, (250, 250, 3))
    #face_img = np.reshape(face_img, (250, 250, 3, 1))
    face_img = face_img.astype("float32")
    face_img /= 255

    ret = model.predict([[face_img]], batch_size=5)   # OK
    print(file_name + "：真顔度 " + str(ret[0][0]) + "; 変顔度 " + str(ret[0][1]))