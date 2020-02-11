import cv2
import dlib

# 各種定義
IMG = "IMG"

# ウィンドウの準備
cv2.namedWindow(IMG)

# 画像読み込み＆グレースケール化
img = cv2.imread("../faces/ryoutako_0527_1.jpg")
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# dlib分類機
face_detector = dlib.get_frontal_face_detector()
detected_faces = face_detector(img, 1)

# 顔の見つけて四角で囲む(トラッキング)
for i, face_rect in enumerate(detected_faces):
    #ここが処理部分
    cv2.rectangle(img, tuple([face_rect.left(),face_rect.top()]), tuple([face_rect.right(),face_rect.bottom()]), (0, 0,255), thickness=2)

# トラッキングされた画像を表示
cv2.imshow(IMG, img)
cv2.waitKey(0)

# 終了処理
cv2.destroyAllWindows()

