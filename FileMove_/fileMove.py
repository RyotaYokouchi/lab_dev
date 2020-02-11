# ある一定以上になったら古いファイルを削除するスクリプト
# CurrentImg：画像のみを入れるファイル
# その他のdir：日付ごとにzipファイルを入れていく。Second, Third,TrashBoxの順
#
# １、CurrentImgの中の画像の枚数を確認
# ２、25000以上のファイル数なら、一番古い日付のものをzipで圧縮
# ３、作ったzipファイルをSecondImgに移動し、CurrentImgから該当する日付のものを削除
# ４、zipファイルをためていき、容量いっぱいになったらThird、TrashBoxという順に移動
# ５、TrashBoxの容量がいっぱいになったら一番古い奴から削除

import os
import datetime
import zipfile
from pymysql.converters import conversions
import shutil

currentImgDirPath = "./CurrentImg/"
secondImgDirPath = "./SecondImg/"
thirdImgDirPath = "./ThirdImg/"
trashBoxDirPath = "./TrashBox/"

# 該当のディレクトリからもっとも古い日付を探す。
# ファイル名は、front-(年)(月)(日)-(時)(分)(秒).jpg と仮定
# 例：front-20190617-062043.jpg
def searchOldDate(path):
    # ディレクトリの中身取得
    files = os.listdir(path)
    # もっとも古い日付
    oldDate = datetime.date.today()

    # ファイル名から年月日を抽出(年)(月)(日)
    for file in files:
        year, month, day = getDate(file)
        date = datetime.date(int(year), int(month), int(day))

        # 取得した日付がoldDateより古いならdateで上書き
        if oldDate > date:
            oldDate = date

    return oldDate

# ファイル名から年月日を抽出(年)(月)(日)
def getDate(fileName):
    year = fileName[6:10]
    month = fileName[10:12]
    day = fileName[12:14]
    return year, month, day

# dateから取得した日付を変換する
def conversionDateString(date):
    year = date.year
    month = date.month
    day = date.day
    # 変換する。 例：2 → 02
    if month / 10 < 1:
        conversionMonth = "0" + str(month)
    if day / 10 < 1:
        conversionDay = "0" + str(day)
    return str(year) + conversionMonth + conversionDay

# currentImgからSecondImgにzipに圧縮して移動
def moveOldImg(upperLimmit):
    # currentImgを取ってくる
    imgs = os.listdir(currentImgDirPath)
    # ファイル数が25000以上の場合の処理
    if len(imgs) >= upperLimmit:
        # もっとも古い日付を取得
        oldDate = conversionDateString(searchOldDate(currentImgDirPath))
        # zipファイルの名前
        zipFileName = "front-" + oldDate
        # ”front-(年)(月)(日).zip”というファイルを作成
        with zipfile.ZipFile(zipFileName, "w", zipfile.ZIP_DEFLATED) as zf:
            # currentImgの中からもっとも古い日付のものをzipにまとめる。
            for imgFileName in imgs:
                if oldDate in imgFileName:
                    # もっとも古い日付を含むファイル名
                    oldImgPath = currentImgDirPath + imgFileName
                    # 作ったzipの中に圧縮
                    zf.write(oldImgPath, oldImgPath)
                    # zipに入れたやつは消す
                    os.remove(oldImgPath, dir_fd=None)
            # 作ったzipファイルをsecondに移動
            print(datetime.datetime.now() + "：" + oldDate + "の日付を含む" + "./" + zipFileName + "を" + secondImgDirPath + "に移動します。")
            shutil.move("./" + zipFileName, secondImgDirPath)
    return

# 上限が来たらzipファイルを移動
def moveOldZip(fromDirPath, toDirPath, upperLimmit):
    # currentImgを取ってくる
    zips = os.listdir(fromDirPath)
    # ファイル数が25000以上の場合の処理
    if len(zips) >= upperLimmit:
        # もっとも古い日付を取得
        oldDate = conversionDateString(searchOldDate(fromDirPath))
        # 古いzipを移動
        for zipFileName in zips:
            if oldDate in zipFileName:
                # 作ったzipファイルをsecondに移動
                print(datetime.datetime.now() + "：" + fromDirPath + zipFileName + "を" + toDirPath + "に移動します。")
                shutil.move(fromDirPath + zipFileName, toDirPath)
    return

# 上限に達した場合に削除
def removeFile(dirPath, upperLimmit):
    # currentImgを取ってくる
    zips = os.listdir(dirPath)
    # ファイル数が25000以上の場合の処理
    if len(zips) >= upperLimmit:
        # もっとも古い日付を取得
        oldDate = conversionDateString(searchOldDate(dirPath))
        # 古いzipを移動
        for zipFileName in zips:
            if oldDate in zipFileName:
                # もっとも古いzipを消す
                print(datetime.datetime.now() + "：" + trashBoxDirPath + "から" + dirPath + zipFileName + "を削除します。")
                os.remove(dirPath + zipFileName, dir_fd=None)

# 始まり
if __name__ == '__main__':
    while True:
        moveOldImg(10)
        moveOldZip(secondImgDirPath, thirdImgDirPath, 2)
        moveOldZip(thirdImgDirPath, trashBoxDirPath, 2)
        removeFile(trashBoxDirPath, 2)

