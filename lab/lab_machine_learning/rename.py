import os


rename_dir_name1 = "./sorce/真顔/"
rename_dir_name2 = "./sorce/変顔/"

def changeDir(rename_dir_name1, rename_dir_name2):
    rename_dir1 = os.listdir(rename_dir_name1)
    rename_dir2 = os.listdir(rename_dir_name2)

    # 最初から名前変更しようとすると、被ってる番号のファイル名が消滅して、データ数が半分になる
    # なので、それを防止するために、一旦ファイル内の画像データの名前を適当に変えとく必要がある

    for num in range(len(rename_dir1)):
        if confDS(rename_dir1[num]):
            continue
        os.rename(rename_dir_name1 + rename_dir1[num] , rename_dir_name1 + str(num + 9999) + ".jpg")
    for num in range(len(rename_dir2)):
        if confDS(rename_dir1[num]):
            continue
        os.rename(rename_dir_name2 + rename_dir2[num] , rename_dir_name2 + str(num + 9999) + ".jpg")

    # 被りを解消したので正常に行えるはず
    for num in range(len(rename_dir1)):
        if confDS(rename_dir1[num]):
            continue
        os.rename(rename_dir_name1 + rename_dir1[num] , rename_dir_name1 + str(num) + ".jpg")
    for num in range(len(rename_dir2)):
        if confDS(rename_dir1[num]):
            continue
        os.rename(rename_dir_name2 + rename_dir2[num] , rename_dir_name2 + str(num) + ".jpg")

def confDS(file_name):
    if file_name == ".DS_Store":
        True
    else:
        False

changeDir(rename_dir_name1, rename_dir_name2)
# for num in range(len(rename_dir1)):
#     os.rename("./sorce/真顔/" + rename_dir1[num] , "./sorce/真顔/" + str(num) + ".jpg")
#
# for num in range(len(rename_dir2)):
#     os.rename("./sorce/変顔/" + rename_dir2[num] , "./sorce/変顔/" + str(num) + ".jpg")
#
# rename_dir1 = os.listdir("./Face/真顔_face")
# rename_dir2 = os.listdir("./Face/変顔_face")
#
# for num in range(len(rename_dir1)):
#     os.rename("./Face/真顔_face/" + rename_dir1[num] , "./Face/真顔_face/" + str(num) + ".jpg")
#
# for num in range(len(rename_dir2)):
#     os.rename("./Face/変顔_face/" + rename_dir2[num] , "./Face/変顔_face/" + str(num) + ".jpg")
#
# rename_dir1 = os.listdir("./Original/真顔")
# rename_dir2 = os.listdir("./Original/変顔")
#
# for num in range(len(rename_dir1)):
#     os.rename("./Original/真顔/" + rename_dir1[num] , "./Original/真顔/" + str(num) + ".jpg")
#
# for num in range(len(rename_dir2)):
#     os.rename("./Original/変顔/" + rename_dir2[num] , "./Original/変顔/" + str(num) + ".jpg")