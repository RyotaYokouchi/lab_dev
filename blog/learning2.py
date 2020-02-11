import os
import cv2
import glob
from scipy import ndimage
from posix import listdir
import shutil
import random
import numpy as np
from tensorflow.keras.utils import to_categorical

from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.layers import Activation, Conv2D, Dense, Flatten, MaxPooling2D
from tensorflow.keras.models import Sequential

# 加工前の画像ディレクトリのパス
original_dir_path = "./faces/original/"
# 加工後の画像ディレクトリのパス
train_dir_path = "./faces/train/"
# テストディレクトリのパス
test_dir_path = "./faces/test/"

Names = os.listdir(train_dir_path)
input_shape=(250,250,3)

# 教師データのラベル付け
name_count = 0
X_train = []
Y_train = []
for name in Names:
    # DS.Storeを取ってきたらcontinue
    if name == ".DS_Store":
        continue
    img_file_name_list=os.listdir(train_dir_path + name)
    print(name + "：学習用の画像の枚数は" + len(img_file_name_list) + "です。")
    # 画像読み込み
    for img_name in img_file_name_list:
        img = cv2.imread(train_dir_path)
        # 画像データない場合別の画像読み込みへ
        if img is None:
                print('image' + str(name_count) + ':NoImage')
                continue
        else:
            # 学習データを格納してラベル付け
            r,g,b = cv2.split(img)
            img = cv2.merge([r,g,b])
            X_train.append(img)
            Y_train.append(name_count)
    name_count += 1

# テストデータのラベル付け
name_count = 0
X_test = [] # 画像データ読み込み
Y_test = [] # ラベル（名前）
for name in Names:
    # DS.Storeを取ってきたらcontinue
    if name == ".DS_Store":
        continue
    img_file_name_list=os.listdir(test_dir_path + name)
    print(name + "：学習用の画像の枚数は" + len(img_file_name_list) + "です。")
    # 画像読み込み
    for img_name in img_file_name_list:
        img = cv2.imread(test_dir_path)
        # 画像データない場合別の画像読み込みへ
        if img is None:
                print(name + ':NoImage')
                continue
        else:
            # 学習データを格納してラベル付け
            r,g,b = cv2.split(img)
            img = cv2.merge([r,g,b])
            X_test.append(img)
            Y_test.append(name_count)
    name_count += 1

# 下準備
x_train=np.array(X_train)
x_test=np.array(X_test)
y_train = to_categorical(Y_train)
y_test = to_categorical(Y_test)

# モデルの定義
model = Sequential()
model.add(Conv2D(input_shape=input_shape, filters=32,kernel_size=(3, 3),
                 strides=(1, 1), padding="same"))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(filters=32, kernel_size=(3, 3),
                 strides=(1, 1), padding="same"))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(filters=32, kernel_size=(3, 3),
                 strides=(1, 1), padding="same"))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(256))
model.add(Activation("relu"))
model.add(Dense(128))
model.add(Activation('relu'))
model.add(Dense(len(Names)))
model.add(Activation('softmax'))

# モデルを読み込む
model.compile(optimizer='sgd',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# データを使って学習開始
history = model.fit(X_train, y_train, batch_size=70,
                    epochs=350, verbose=1, validation_data=(X_test, y_test))

# 精度の確認
score = model.evaluate(X_test, y_test, batch_size=32, verbose=0)
print('validation loss:{0[0]}\nvalidation accuracy:{0[1]}'.format(score))

import matplotlib.pyplot as plt
#acc, val_accのプロット
plt.plot(history.history["acc"], label="acc", ls="-", marker="o")
plt.plot(history.history["val_acc"], label="val_acc", ls="-", marker="x")
plt.ylabel("accuracy")
plt.xlabel("epoch")
plt.legend(loc="best")
plt.show()

#モデルを保存
model.save("Model.h5")