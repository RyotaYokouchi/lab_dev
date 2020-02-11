import cv2
import os
import time
from datetime import datetime as dt

NAME = "hogehoge"
print(NAME + "さんの顔データを取得します。")

# カスケードパス
cascade_path = '/usr/local/opt/opencv/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml'
# カスケードを実行するためのパーツ
faceCascade = cv2.CascadeClassifier(cascade_path)

# 取得する顔の総数
cnt_max = 10
# 顔データのカウント
cnt_face = 0
# 顔データを格納する配列
faces = []

# カメラ取り込み開始
cap = cv2.VideoCapture(0)

while True:
    # 初期フレームの取得
    time.sleep(1)
    end_flag, c_frame = cap.read()
    
    # 画像取得
    img = c_frame
    # グレースケールに変換して格納
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 画像上の顔領域を見つける
    face_list = faceCascade.detectMultiScale(img_gray, minSize=(100, 100))
    # 画像上に複数の顔領域がある場合ループの最初へ
    if len(face_list) > 1:
            continue;
        
    # 顔領域を切り取って収集
    for (pos_x, pos_y, w, h) in face_list:
        # 顔の切出
        img_face = img[pos_y:pos_y+h, pos_x:pos_x+w]
        # 画像サイズ変更
        img_face = cv2.resize(img_face, (100, 100))
        # facesに顔画像を格納
        faces.append(img_face)
        # 顔データのカウントを進める
        cnt_face+=1
    
    print(cnt_face)
    # 指定した数分のデータを収集したら終了
    if cnt_max == cnt_face:
        break;

# カメラの領域を開放
cap.release()

print("顔データの収集が終わりました。")
print("顔データを名前ごとに振り分けます。")

# 学習データの数
num = 0
# 画像データの名前の最初に付ける日付
tdatetime = dt.now()
tstr = tdatetime.strftime("%Y%m%d%H%M")

# 学習用データを入れるディレクトリを作成
path = os.getcwd() + '/faces/train/' + NAME
os.makedirs(path)
print("学習用データ格納用のディレクトリを作成", path)

# trainディレクトリに学習用データを格納
for face in faces[:-1]:
    # "ファイル名"-"データ数カウント".jpg と言う名前のファイル名
    filename = tstr + '-' + str(num) + '.jpg'
    print("\t", filename)
    # path/filename で顔画像データを書き込む
    cv2.imwrite(path + '/' + filename, face)
    # カウントを進める
    num += 1

# テスト用データを入れるディレクトリを作成
path = os.getcwd() + '/faces/test/' + NAME
print("テストデータ", path)
os.makedirs(path)

# testディレクトリに学習用データを格納
face = faces[-1]
# "ファイル名"-"データ数カウント".jpg と言う名前のファイル名
filename = tstr + '-' + str(num) + '.jpg'
print("\t", filename)
# path/filename で顔画像データを書き込む
cv2.imwrite(path + '/' + filename, face)


