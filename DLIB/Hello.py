import cv2
import numpy as np

# ルックアップテーブルの生成
min_table = 50
max_table = 205
diff_table = max_table - min_table

LUT_HC = np.arange(256, dtype = 'uint8' )
LUT_LC = np.arange(256, dtype = 'uint8' )

# ハイコントラストLUT作成
for i in range(0, min_table):
    LUT_HC[i] = 0
for i in range(min_table, max_table):
    LUT_HC[i] = 255 * (i - min_table) / diff_table
for i in range(max_table, 255):
    LUT_HC[i] = 255

# 輝度
# for i in range(256):
#     LUT_LC[i] = min_table + i * (diff_table) / 255

#  明るさ
# gamma1 = 0.50
# gamma2 = 1.7
# for i in range(256):
#     LUT_HC[i] = 255 * pow(float(i) / 255, 1.0 / gamma1)
#     LUT_LC[i] = 255 * pow(float(i) / 255, 1.0 / gamma2)

# 明るさと輝度
# src = cv2.imread("faces/Steve.png", 1)
# high_cont_img = cv2.LUT(src, LUT_HC)
# low_cont_img = cv2.LUT(src, LUT_LC)

# ぼかす
# average_square = (10,10)
# src = cv2.imread("faces/Steve.png", 1)
# blur_img = cv2.blur(src, average_square)

# ノイズ
# src = cv2.imread("faces/Steve.png", 1)
# row,col,ch= src.shape
# mean = 0
# sigma = 15
# gauss = np.random.normal(mean,sigma,(row,col,ch))
# gauss = gauss.reshape(row,col,ch)
# gauss_img = src + gauss

# 左右反転
# src = cv2.imread("faces/Steve.png", 1)
# hflip_img = cv2.flip(src, 1)
# vflip_img = cv2.flip(src, 0)

src = cv2.imread("faces/Steve.png", 1)
hight = src.shape[0]
width = src.shape[1]
half_img = cv2.resize(src,(float(hight)/2,float(width)/2))

cv2.imshow("sono1", half_img)
cv2.imwrite("faces/Steve9.png", half_img)
cv2.waitKey(0)
cv2.destroyAllWindows()