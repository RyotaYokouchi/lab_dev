from helpers import * #@UnresolvedImport
import cv2
import dlib#@UnresolvedImport

class tracking:
    # 定数定義
    ESC_KEY = 27     # Escキー
    INTERVAL= 33     # 待ち時間
    FRAME_RATE = 30  # fps

    DEVICE_ID = 0

    # 分類器の初期設定
    face_cascade, eye_cascade, mouth_cascade, nose_cascade = index_cascade()

    # カメラ映像取得
    cap = cv2.VideoCapture(DEVICE_ID)

    # 初期フレームの読込
    end_flag, c_frame = cap.read()
    height, width, channels = c_frame.shape

    # ウィンドウの準備
    cv2.namedWindow("tracking")

    # 変換処理ループ
    while end_flag == True:

        # 画像の取得と顔の検出
        img = c_frame
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 輪郭、目、鼻、口を画像上から探す
        face_list, eye_list, mouth_list, nose_list = find_face_parts(img_gray, face_cascade, eye_cascade, mouth_cascade, nose_cascade)

        # 検出した顔に印を付ける
        tracking(img, face_list, color = (0, 0, 225))

        # 検出した目に印を付ける
        tracking(img, eye_list, color = (0, 225, 0))

        # 検出した口に印を付ける
        tracking(img, mouth_list, color = (255, 0, 0))

        # 検出した鼻に印を付ける
        tracking(img, nose_list, color = (255, 255, 255))

        # フレーム表示
        cv2.imshow("tracking", c_frame)

        # Escキーで終了
        key = cv2.waitKey(INTERVAL)
        if key == ESC_KEY:
            break

        # 次のフレーム読み込み
        end_flag, c_frame = cap.read()

    # 終了処理
    cv2.destroyAllWindows()
    cap.release()

