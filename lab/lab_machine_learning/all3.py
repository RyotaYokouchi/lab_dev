from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.layers import Activation, Conv2D, Dense, Flatten, MaxPooling2D
from tensorflow.keras.models import Sequential
# 顔認識する対象を決定（検索ワードを入力）
SearchName = ["真顔","変顔"]#,"西野七瀬","優月心菜"]
# 画像の取得枚数の上限
ImgNumber = 10
# CNNで学習するときの画像のサイズを設定（サイズが大きいと学習に時間がかかる）
ImgSize=(250,250)
input_shape=(250,250,3)

import os
# オリジナル画像用のフォルダ
os.makedirs("./Original", exist_ok=True)
# 顔の画像用のフォルダ
os.makedirs("./Face", exist_ok=True)
# ImgSizeで設定したサイズに編集された顔画像用のフォルダ
os.makedirs("./FaceEdited", exist_ok=True)
# テストデータを入れる用のフォルダ
os.makedirs("./test", exist_ok=True)

# -*- coding:utf-8 -*-
import cv2
import numpy as np

# OpenCVのデフォルトの分類器のpath。(https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xmlのファイルを使う)
cascade_path = '/usr/local/opt/opencv/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml'
# 例
#cascade_path = './opencv-master/data/haarcascades/haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascade_path)

for name in SearchName:
    # 画像データのあるディレクトリ
    input_data_path = "./Original/"+str(name)
    # 切り抜いた画像の保存先ディレクトリを作成
    os.makedirs("./Face/"+str(name)+"_face", exist_ok=True)
    save_path = "./Face/"+str(name)+"_face/"
    # 収集した画像の枚数(任意で変更)
    image_count = ImgNumber
    # 顔検知に成功した数(デフォルトで0を指定)
    face_detect_count = 0

    print("{}の顔を検出し切り取りを開始します。".format(name))
    # 集めた画像データから顔が検知されたら、切り取り、保存する。
    for i in range(image_count):
        img = cv2.imread(input_data_path + '/'+ str(i) + '.jpg', cv2.IMREAD_COLOR)
        if img is None:
             print('image' + str(i) + ':NoFace')
        else:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            face = faceCascade.detectMultiScale(gray, 1.1, 3)
            if len(face) > 0:
                for rect in face:
                    # 顔認識部分を赤線で囲み保存(今はこの部分は必要ない)
                    # cv2.rectangle(img, tuple(rect[0:2]), tuple(rect[0:2]+rect[2:4]), (0, 0,255), thickness=1)
                    # cv2.imwrite('detected.jpg', img)
                    x = rect[0]
                    y = rect[1]
                    w = rect[2]
                    h = rect[3]
                    cv2.imwrite(save_path + 'cutted' + str(face_detect_count) + '.jpg',img[y:y+h,  x:x+w])
                    face_detect_count = face_detect_count + 1
            else:
                print('image' + str(i) + ':NoFace')

print("顔画像の切り取り作業、正常に動作しました。")
