# 顔認識する対象を決定（検索ワードを入力）
SearchName = ["名前１","名前２","名前３","名前４"]
# 画像の取得枚数の上限
ImgNumber =600
# CNNで学習するときの画像のサイズを設定（サイズが大きいと学習に時間がかかる）
ImgSize=(250,250)
input_shape=(250,250,3)

import os
# オリジナル画像用のフォルダ
os.makedirs("./Original", exist_ok=True)
# 顔の画像用のフォルダ
os.makedirs("./Face", exist_ok=True)
# ImgSizeで設定したサイズに編集された顔画像用のフォルダ
os.makedirs("./FaceEdited", exist_ok=True)
# テストデータを入れる用のフォルダ
os.makedirs("./test", exist_ok=True)