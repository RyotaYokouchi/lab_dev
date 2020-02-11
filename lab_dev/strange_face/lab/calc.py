from helpers import * #@UnresolvedImport
import cv2

def calcFunnyFace():
    IMG1 = "img1"
    IMG2 = "img2"
    DEVICE_ID = 0

    # 分類器の初期設定
    face_cascade, eye_cascade, mouth_cascade, nose_cascade = index_cascade()

    # パスの設定
    cul_dir = "/Users/yokouchiryouta/Desktop/"
    img1_name = "test1.jpg"
    img2_name = "test2.jpg"

    # 画像読み込み＆グレースケール化
    img1 = cv2.imread(cul_dir + img1_name)
    img2 = cv2.imread(cul_dir + img2_name)
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # ウィンドウの準備
    cv2.namedWindow(IMG1)
    cv2.namedWindow(IMG2)

    # 顔のパーツ検出
    face_list1, eye_list1, mouth_list1, nose_list1 = find_face_parts(img1_gray, face_cascade, eye_cascade, mouth_cascade, nose_cascade)
    face_list2, eye_list2, mouth_list2, nose_list2 = find_face_parts(img2_gray, face_cascade, eye_cascade, mouth_cascade, nose_cascade)

    # 輪郭外の顔パーツを削除
    eye_list1, mouth_list1, nose_list1 = delete_face_parts(face_list1, eye_list1, mouth_list1, nose_list1)
    eye_list2, mouth_list2, nose_list2 = delete_face_parts(face_list2, eye_list2, mouth_list2, nose_list2)

    # 顔のパーツを四角で囲む
    tracking_face_parts(img1, face_list1, eye_list1, mouth_list1, nose_list1)
    tracking_face_parts(img2, face_list2, eye_list2, mouth_list2, nose_list2)

    # トラッキングされた画像を表示
    cv2.imshow(IMG1, img1)
    cv2.imshow(IMG2, img2)

    # 結果を保存
    cv2.imwrite(cul_dir + "answer1.jpg", img1)
    cv2.imwrite(cul_dir + "answer2.jpg", img2)

    print("IMG1の顔の対称性：" + str(calSymmetry(face_list1, eye_list1, mouth_list1, nose_list1)))
    print("IMG2の顔の対称性：" + str(calSymmetry(face_list2, eye_list2, mouth_list2, nose_list2)))

    print("IMG1の顔のバランス：" + str(calcBalance(face_list1, eye_list1, mouth_list1, nose_list1)))
    print("IMG2の顔のバランス：" + str(calcBalance(face_list2, eye_list2, mouth_list2, nose_list2)))

    print("大きさの変化の値：" + str(calcSize(face_list1, eye_list1, mouth_list1, nose_list1, face_list2, eye_list2, mouth_list2, nose_list2)))
