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


    face_detector = dlib.get_frontal_face_detector()
    detected_faces = face_detector(c_frame, 1)

    # ウィンドウの準備
    cv2.namedWindow("tracking")

    # 変換処理ループ
    while end_flag == True:

        # 画像の取得と顔の検出
        img = c_frame

        detected_faces = face_detector(img, 1)
        for i, face_rect in enumerate(detected_faces):
            #ここが処理部分
            cv2.rectangle(img, tuple([face_rect.left(),face_rect.top()]), tuple([face_rect.right(),face_rect.bottom()]), (0, 0,255), thickness=2)

        # フレーム表示
        cv2.imshow("tracking", img)

        # Escキーで終了
        key = cv2.waitKey(INTERVAL)
        if key == ESC_KEY:
            break

        # 次のフレーム読み込み
        end_flag, c_frame = cap.read()

    # 終了処理
    cv2.destroyAllWindows()
    cap.release()

