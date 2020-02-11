from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.layers import Activation, Conv2D, Dense, Flatten, MaxPooling2D
from tensorflow.keras.models import Sequential
import os

# 加工前の画像ディレクトリのパス
original_dir_path = "./faces/original/"
# 加工後の画像ディレクトリのパス
train_dir_path = "./faces/train/"
# テストディレクトリのパス
test_dir_path = "./faces/test/"

#Names = os.listdir(train_dir_path)
input_shape=(250,250,3)


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
print(model.output_shape)
model.add(Flatten())
print(model.output_shape)
model.add(Dense(256))
print(model.output_shape)
model.add(Activation("sigmoid"))
model.add(Dense(128))
print(model.output_shape)
model.add(Activation('sigmoid'))
model.add(Dense(2))
print(model.output_shape)
model.add(Activation('softmax'))