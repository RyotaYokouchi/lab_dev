from helpers import * #@UnresolvedImport
import cv2
import dlib#@UnresolvedImport
import time
import sys

class tracking:
    # 定数定義
    ESC_KEY = 27     # Escキー
    INTERVAL= 33     # 待ち時間
    FRAME_RATE = 30  # fps

    DEVICE_ID = 0

    # 分類器の初期設定
    face_cascade, eye_cascade, mouth_cascade, nose_cascade = index_cascade()

    # ウィンドウの準備
    cv2.namedWindow("tracking")


    # 画像の取得と顔の検出
    img = cv2.imread("/Users/yokouchiryouta/Desktop/顔データ/検証用画像データ/顔領域/Tsuboi_1.jpg")
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 輪郭、目、鼻、口を画像上から探す
    face_list, eye_list, mouth_list, nose_list, recognition_flag = find_face_parts(img_gray, face_cascade, eye_cascade, mouth_cascade, nose_cascade)
    if not recognition_flag:
        print("顔検出に失敗しました。画像を撮りなおしてください。")
        sys.exit()

    # 検出した顔に印を付ける
    tracking(img, face_list, color = (0, 0, 225))

    # 検出した目に印を付ける
    tracking(img, eye_list, color = (0, 225, 0))

    # 検出した口に印を付ける
    tracking(img, mouth_list, color = (255, 0, 0))

    # 検出した鼻に印を付ける
    tracking(img, nose_list, color = (255, 255, 255))

    # フレーム表示
    cv2.imshow("tracking", img)

    cv2.waitKey(0)

    # 終了処理
    cv2.destroyAllWindows()

