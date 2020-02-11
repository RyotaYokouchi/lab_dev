import cv2
import numpy
from asn1crypto._ffi import null
from scipy import ndimage

# カスケードの初期設定
def index_cascade():
    cascade_face_file = '/usr/local/opt/opencv/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml'
    cascade_eye_file = '/usr/local/opt/opencv/share/OpenCV/haarcascades/haarcascade_eye.xml'
    cascade_mouth_file = '/usr/local/opt/opencv/share/OpenCV/haarcascades/haarcascade_mcs_mouth.xml'
    cascade_nose_file = '/usr/local/opt/opencv/share/OpenCV/haarcascades/haarcascade_mcs_nose.xml'
    face_cascade = cv2.CascadeClassifier(cascade_face_file)
    eye_cascade = cv2.CascadeClassifier(cascade_eye_file)
    mouth_cascade = cv2.CascadeClassifier(cascade_mouth_file)
    nose_cascade = cv2.CascadeClassifier(cascade_nose_file)
    return face_cascade, eye_cascade, mouth_cascade, nose_cascade

# 引数のカスケードに相当する顔のパーツを検出する
def find_face_parts(img_gray, face_cascade = None, eye_cascade = None, mouth_cascade = None, nose_cascade = None):
    # 2019/12/14 修正内容
    # 顔のパーツを検出する際に、顔が斜めになるなどの影響で正常に検出できなかった時のために
    # rotate関数を用いて顔画像を回転させ、顔検出しやすくする仕組みを作る

    # -15 ~ 15のリスト
    rotate_list = list(range(-15, 15))

    # 画像を少しずつ回転させ、その画像に対し顔検出を行う。
    # 全てのパーツが検出できたら、その画像で変顔度を測る。
    for rotate_value in rotate_list:
        # 回転させる
        rotate_img = ndimage.rotate(img_gray, rotate_value)

        # 顔検出する
        if face_cascade:
            face_list = face_cascade.detectMultiScale(img_gray, minNeighbors=10, minSize=(100, 100))
        if eye_cascade:
            eye_list = eye_cascade.detectMultiScale(img_gray, minNeighbors=10, minSize=(70, 70))
        if mouth_cascade:
            mouth_list = mouth_cascade.detectMultiScale(img_gray, minNeighbors=10, minSize=(70, 70))
        if nose_cascade:
            nose_list = nose_cascade.detectMultiScale(img_gray, minNeighbors=10, minSize=(70, 70))

        if len(face_list) == 1 and len(eye_list) == 2 and len(mouth_list) == 1 and len(nose_list) == 1:
            return face_list, eye_list, mouth_list, nose_list, True
        else:
            continue
    return face_list, eye_list, mouth_list, nose_list, False

# 顔のパーツを四角でトラッキング
def tracking_face_parts(img, face_list = None, eye_list = None, mouth_list = None, nose_list = None):
    if face_list is not None:
        tracking(img, face_list, color = (0, 0, 225))
    if eye_list is not None:
        tracking(img, eye_list, color = (0, 255, 0))
    if mouth_list is not None:
        tracking(img, mouth_list, color = (225, 0, 0))
    if nose_list is not None:
        tracking(img, nose_list, color = (225, 225, 225))

# 顔のパーツを四角でトラッキング
def tracking(img, face_part_list, color):
    for (x, y, w, h) in face_part_list:
            pen_w = 3
            cv2.rectangle(img, (x, y), (x+w, y+h), color, thickness = pen_w)

# 輪郭外の顔パーツを削除
def delete(face_list, face_part_list):
    new_face_part_list = []
    for (x, y, w, h) in face_list:
        face_part_list_count = 0
        for (x_, y_, w_, h_) in face_part_list:
            if (x <= x_ and x_ <= x+w) and (x <= x_+w_ and x_+w_ <= x+w) and (y <= y_ and y_ <= y+h) and (y <= y_+h_ and y_+h_ <= y+h):
                new_face_part_list.append(face_part_list[face_part_list_count])
            face_part_list_count += 1
    return new_face_part_list

# 輪郭外の顔パーツを削除
def delete_face_parts(face_list, eye_list = None, mouth_list = None, nose_list = None):
    if eye_list is not None:
        eye_list = delete(face_list, eye_list)
    if mouth_list is not None:
        mouth_list = delete(face_list, mouth_list)
    if nose_list is not None:
        nose_list = delete(face_list, nose_list)
    return eye_list, mouth_list, nose_list

# 右目と左目を分ける
def separateEye(eye_list):
    # 左目と右目の判別
    big_x = -9999
    right_eye = []
    left_eye = []
    count = 0
    for (x, y, w, h) in eye_list:
        if big_x < x:
            left_eye.append(eye_list[count])
            big_x = x
        else:
            right_eye.append(eye_list[count])
        count += 1
    return right_eye, left_eye

# 顔の輪郭とパーツから顔の対称性を確認
def calSymmetry(face_list = None, eye_list = None, mouth_list = None, nose_list = None):
    # 条件１：顔のパーツと輪郭が全て認識できていること
    # 条件２：目が二つのみ認識されていること
    # 条件３：鼻と口および輪郭の領域が一つのみ認識されていること
    # 手順：
    # ① 輪郭の中央線(縦線)で左右を分ける
    # ② 左右の目領域の四隅の座標を左右で比較
    # ③ 鼻領域の四隅の座標を比較
    # ④ 口領域の四隅の座標を比較
    # ⑤ 比較した値から左右の対称性を比較

    # 顔のパーツがあるか判定
    if face_list is None or eye_list is None or mouth_list is None or nose_list is None:
        print("顔のパーツが不揃いのため計測することができません！")
        return

    # 顔領域の中央のx座標
    for (x, y, w, h) in face_list:
        center_line = x + (w / 2)

    # 右目と左目を分ける
    right_eye, left_eye = separateEye(eye_list)

    # 右目と中央の差
    for (x, y, w, h) in right_eye:
        wide_diff_right_eye = abs(x - center_line)
        high_diff_right_eye = y
    # 左目と中央の差
    for (x, y, w, h) in left_eye:
        wide_diff_left_eye = abs((x + w) - center_line)
        high_diff_left_eye = y

    # 目の対称性
    eyes_symmetry = abs(wide_diff_right_eye - wide_diff_left_eye + abs(high_diff_right_eye - high_diff_left_eye))

    # 鼻
    for (x, y, w, h) in nose_list:
        # 鼻領域の右端と中央の差
        diff_right_nose = abs((x + w) - center_line)
        # 鼻領域の左端と中央の差
        diff_left_nose = abs(x - center_line)
        # 鼻の対称性
        nose_symmetry = abs(diff_right_nose - diff_left_nose)

    # 口
    for (x, y, w, h) in mouth_list:
        # 口領域の右端と中央の差
        diff_right_mouth = abs((x + w) - center_line)
        # 口領域の左端と中央の差
        diff_left_mouth = abs(x - center_line)
        # 口の対称性
        mouth_symmetry = abs(diff_right_mouth - diff_left_mouth)

    # 対称性値の合計
    total_balance = eyes_symmetry + nose_symmetry + mouth_symmetry

    return total_balance

# 顔のバランスを計算する
def calcBalance(face_list = None, eye_list = None, mouth_list = None, nose_list = None):
    # 条件１：顔のパーツと輪郭が全て認識できていること
    # 条件２：目が二つのみ認識されていること
    # 条件３：鼻と口および輪郭の領域が一つのみ認識されていること
    # 手順：
    # ① 各パーツの領域の中心の座標をとり、各パーツごとの距離で比較する

    # 顔のパーツがあるか判定
    if face_list is None or eye_list is None or mouth_list is None or nose_list is None:
        print("顔のパーツが不揃いのため計測することができません！")
        return

    # 右目と左目を分ける
    right_eye, left_eye = separateEye(eye_list)

    # 右目の中心座標
    for (x, y, w, h) in right_eye:
        right_eye_center = numpy.array([x + (w/2), y + (h/2)])
    # 左目の中心座標
    for (x, y, w, h) in left_eye:
        left_eye_center = numpy.array([x + (w/2), y + (h/2)])
    # 鼻の中心座標
    for (x, y, w, h) in nose_list:
        nose_center = numpy.array([x + (w/2), y + (h/2)])
    # 口の中心座標
    for (x, y, w, h) in mouth_list:
        mouth_center = numpy.array([x + (w/2), y + (h/2)])

    # 目と目の距離
    dis_eye_to_eye = numpy.linalg.norm(right_eye_center - left_eye_center)
    # 右目と鼻の距離
    dis_right_eye_to_nose = numpy.linalg.norm(right_eye_center - nose_center)
    # 左目と鼻の距離
    dis_left_eye_to_nose =  numpy.linalg.norm(left_eye_center - nose_center)
    # 右目と口の距離
    dis_right_eye_to_mouth = numpy.linalg.norm(right_eye_center - mouth_center)
    # 左目と口の距離
    dis_left_eye_to_mouth = numpy.linalg.norm(left_eye_center - mouth_center)
    # 鼻と口の距離
    dis_nose_to_mouth = numpy.linalg.norm(nose_center - mouth_center)

    # 各パーツの値を入れたやつ
    part_list = [dis_eye_to_eye, dis_right_eye_to_nose, dis_left_eye_to_nose, dis_right_eye_to_mouth, dis_left_eye_to_mouth, dis_nose_to_mouth]

    # 合計のバランスを入れるやつ
    total_balance = 0

    # 各パーツの値の合計
    for part in part_list:
        total_balance = part

    # 各パーツの距離/各パールの数
    return total_balance / len(part_list)

def calcSize(face_list1 = None, eye_list1 = None, mouth_list1 = None, nose_list1 = None, face_list2 = None, eye_list2 = None, mouth_list2 = None, nose_list2 = None):
    # 条件１：顔のパーツと輪郭が全て認識できていること
    # 条件２：目が二つのみ認識されていること
    # 条件３：鼻と口および輪郭の領域が一つのみ認識されていること
    # 手順：
    # ① 各パーツのの大きさの変化を計算

    # 顔のパーツがあるか判定
    if face_list1 is None or eye_list1 is None or mouth_list1 is None or nose_list1 is None:
        print("顔のパーツが不揃いのため計測することができません！")
        return

    # 顔のパーツがあるか判定
    if face_list2 is None or eye_list2 is None or mouth_list2 is None or nose_list2 is None:
        print("顔のパーツが不揃いのため計測することができません！")
        return

    # 右目と左目を分ける
    right_eye1, left_eye1 = separateEye(eye_list1)

    # 右目と左目を分ける
    right_eye2, left_eye2 = separateEye(eye_list2)

    # 右目の大きさの変化値
    for (x1, y1, w1, h1), (x2, y2, w2, h2) in zip(right_eye1, right_eye2):
        diff_right_eye = abs((w1 * h1) - (w2 * h2))

    # 左目の大きさの変化値
    for (x1, y1, w1, h1), (x2, y2, w2, h2) in zip(left_eye1, left_eye2):
        diff_left_eye = abs((w1 * h1) - (w2 * h2))

    # 鼻の大きさの変化値
    for (x1, y1, w1, h1), (x2, y2, w2, h2) in zip(nose_list1, nose_list2):
        diff_left_nose = abs((w1 * h1) - (w2 * h2))

    # 口の大きさの変化値
    for (x1, y1, w1, h1), (x2, y2, w2, h2) in zip(mouth_list1, mouth_list2):
        diff_left_nose = abs((w1 * h1) - (w2 * h2))

    return diff_right_eye + diff_left_eye + diff_left_nose + diff_left_nose



class PrintMng:
    # Handles the printing windows
    def __init__(self):
        # Windows list
        self.windows = []