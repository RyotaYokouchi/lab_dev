import cv2

# 定数定義
ESC_KEY = 27     # Escキー
INTERVAL= 33     # 待ち時間
FRAME_RATE = 30  # fps

DEVICE_ID = 0

face_path = "/Users/yokouchiryouta/Desktop/顔データ/検証用画像データ/顔領域/Yokouchi_1.jpg"

face1 = cv2.imread(face_path)
face2 = cv2.imread(face_path)

cv2.imshow("a", face1)

face2 = cv2.threshold(face2, 100, 255, cv2.THRESH_TOZERO)[1]
cv2.imshow("b", face2)

# Escキーで終了
key = cv2.waitKey(0)

# 終了処理
cv2.destroyAllWindows()
