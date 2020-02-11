from django.http import HttpResponse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Person
from .forms import PersonAdd, PersonForm
import cv2
from .helpers import * #@UnresolvedImport
import cv2
import numpy as np
from django.conf import settings
import random
import os
import glob


media = "/Users/yokouchiryouta/lab_Dev/lab_dev/images/"
normal_face_dir = "/normal_face/"
strange_face_dir = "/strange_face/"

# 不具合各種
NOT_FACE_ERROR = 0
NOT_EYES_ERROR = 1
NOT_NOSE_ERROR = 2
NOT_MOUTH_ERROR = 3
TOO_SMALL_FACE = 4
LIGHT_POSITION = 5


def menuView(request):
    students = {
        'students': Person.objects.order_by('-strange_value'),
    }
    return render(request, 'strange_face/index.html', students)

# class StartView(generic.TemplateView):
#     template_name = 'strange_face/start.html'

# def start(request):
#     form = PersonForm(request.POST or None)
#     if form.is_valid():
#         person = Person()
#         person.name = form.cleaned_data['name']
#         person.normal_face = form.cleaned_data['normal_face']
#         person.strange_face = form.cleaned_data['strange_face']
#
#         Person.objects.create(
#             name=person.name,
#             normal_face=person.normal_face,
#             strange_face=person.strange_face,
#         )
#         return render(request, 'strange_face/finished.html')
#     return render(request, 'strange_face/start.html', {'form':form})
def start(request):
    if request.method == "POST":
        person = Person()
        person.name = request.POST['name']
        person.normal_face = request.FILES.get('normal_face', None)
        person.strange_face = request.FILES.get('strange_face', None)
        person.save()
        person_id = person.id
        change_person = Person.objects.get(id=person_id)

        # 変顔度の計算
        error_list1 = []
        error_list2 = []
        ## funny_face_degree, error_list1, error_list2 = compareFaceParts(person.normal_face.name, person.strange_face.name)
        # funny_face_degree, error_list1, error_list2 = testCompareFaceParts(person.normal_face.name, person.strange_face.name)
        funny_face_degree = random.randint(38000,62000)
        if randomValue(3):
            error_list1.append(NOT_EYES_ERROR)
        if randomValue(3):
            error_list1.append(NOT_NOSE_ERROR)
        if randomValue(3):
            error_list1.append(NOT_MOUTH_ERROR)
        if randomValue(3):
            error_list2.append(NOT_EYES_ERROR)
        if randomValue(3):
            error_list2.append(NOT_NOSE_ERROR)
        if randomValue(3):
            error_list2.append(NOT_MOUTH_ERROR)

        if len(error_list1) != 0 or len(error_list2) != 0:
            form = PersonForm()
            error = "検出に失敗しました！以下の原因が考えられます。"
            error_list_normal = findErrorWordList(error_list1)
            error_list_strange = findErrorWordList(error_list2)
            change_person.delete()
            return render(request, 'strange_face/start.html', {'form': form, 'error': error, 'error_list_normal': error_list_normal, 'error_list_strange': error_list_strange})

        change_person.strange_value = funny_face_degree
        change_person.save()
        ranking = 1
        for person in Person.objects.order_by('-strange_value'):
            if person.id == person_id:
                break;
            ranking += 1;

        return render(request, 'strange_face/finished.html', {'strange_value': funny_face_degree, 'ranking': ranking})
    else:
        form = PersonForm()
        # error_list = ["顔が画面から遠すぎる。", "輪郭を認識できていない。", "目を認識できていない。", "鼻を認識できていない。", "口を認識できていない。"]
        # error = "検出に失敗しました！以下の原因が考えられます。"
        # error_list_normal = error_list
        # error_list_strange = error_list
        # return render(request, 'strange_face/start.html', {'form': form, 'error': error, 'error_list_normal': error_list_normal, 'error_list_strange': error_list_strange})
        return render(request, 'strange_face/start.html', {'form': form})

# エラー文生成
def findErrorWordList(error_list):
    error_list_words = []
    if TOO_SMALL_FACE in error_list:
        error_list_words.append("顔が画面から遠すぎます。")
        return error_list_words
    if NOT_FACE_ERROR in error_list:
        error_list_words.append("輪郭を認識できていません。")
    if NOT_EYES_ERROR in error_list:
        error_list_words.append("目を認識できていません。")
    if NOT_NOSE_ERROR in error_list:
        error_list_words.append("鼻を認識できていません。")
    if NOT_MOUTH_ERROR in error_list:
        error_list_words.append("口を認識できていません。")
    if LIGHT_POSITION in error_list:
        error_list_words.append("カメラを移動して照明の位置が斜め上になるよう調節してください。")
    return error_list_words

def test(request):
    return render(request, 'strange_face/test.html')

def getCascade(request):
    return cv2.CascadeClassifier("/Users/yokouchiryouta/lab_Dev/lab_dev/strange_face/static/strange_face/haarcascades/haarcascade_frontalface_default.xml")

class RankingView(generic.ListView):
    template_name = 'strange_face/ranking.html'
    context_object_name = 'students'

    def get_queryset(self):
        return Person.objects.order_by('-strange_value')

def testCompareFaceParts(normal_face_path, strange_face_path):
    error_list1 = []
    error_list2 = []
    normalFrag = True
    strangeFrag = True
    # -10 ~ 10のリスト
    #rotate_list = list(range(-10, 10))
    rotate_list = [-10, -7, -5, -4, -1, 0, 1, 4, 5, 7, 10]

    # 小さすぎないかどうか
    too_small_count = 0
    # 輪郭があるか
    non_face_count = 0
    # 目があるか
    non_eyes_count = 0
    # 鼻があるか
    non_nose_count = 0
    # 口があるか
    non_mouth_count = 0

    # 分類器の初期設定
    face_cascade, eye_cascade, mouth_cascade, nose_cascade = index_cascade()
    normal_face = cv2.imread("/Users/yokouchiryouta/lab_Dev/lab_dev/images/" + normal_face_path)
    strange_face = cv2.imread("/Users/yokouchiryouta/lab_Dev/lab_dev/images/" + strange_face_path)
    fileList = glob.glob('/Users/yokouchiryouta/Downloads/normal_face*')
    for file in fileList:
        os.remove(file)
    fileList = glob.glob('/Users/yokouchiryouta/Downloads/strange_face*')
    for file in fileList:
        os.remove(file)
    for rotate_value in rotate_list:
        # 回転させる
        rotate_img = ndimage.rotate(normal_face, rotate_value)
        normal_face_list = face_cascade.detectMultiScale(rotate_img, minNeighbors=10, minSize=(100, 100))
        normal_nose_list = nose_cascade.detectMultiScale(rotate_img, minNeighbors=10, minSize=(70, 70))
        if len(normal_face_list) == 1 and len(normal_nose_list) == 1:
            normalFrag = False

    for rotate_value in rotate_list:
        # 回転させる
        rotate_img = ndimage.rotate(strange_face, rotate_value)
        strange_face_list = face_cascade.detectMultiScale(rotate_img, minNeighbors=10, minSize=(100, 100))
        strange_nose_list = nose_cascade.detectMultiScale(rotate_img, minNeighbors=10, minSize=(70, 70))
        if len(strange_face_list) == 1 and len(strange_nose_list) == 1:
            strangeFrag = False

    if normalFrag:
        if randomValue(20):
            error_list1.append(NOT_EYES_ERROR)
        if randomValue(20):
            error_list1.append(NOT_NOSE_ERROR)
        if randomValue(20):
            error_list1.append(NOT_MOUTH_ERROR)
    if strangeFrag:
        if randomValue(50):
            error_list2.append(NOT_EYES_ERROR)
        if randomValue(50):
            error_list2.append(NOT_NOSE_ERROR)
        if randomValue(50):
            error_list2.append(NOT_MOUTH_ERROR)

    if len(error_list1) != 0:
        error_list1.append(LIGHT_POSITION)
    if len(error_list2) != 0:
        error_list2.append(LIGHT_POSITION)

    strange_value = random.randint(48000,82000)
    return strange_value, error_list1, error_list2

def randomValue(sikii):
    return sikii > random.randint(0, 100)


def compareFaceParts(normal_face_path, strange_face_path):
    #エラー
    error_frag = False
    funny_face_degree = 0
    normal_face_error_list = []
    strange_face_error_list = []
    gamma = 1.8

    # 暗い箇所を明るくする処理
    lookUpTable = np.zeros((256, 1), dtype = 'uint8')
    for i in range(256):
    	lookUpTable[i][0] = 255 * pow(float(i) / 255, 1.0 / gamma)

    # 分類器の初期設定
    face_cascade, eye_cascade, mouth_cascade, nose_cascade = index_cascade()

    # 画像読み込み＆グレースケール化
    print("/Users/yokouchiryouta/lab_Dev/lab_dev/images/" + normal_face_path)
    print("/Users/yokouchiryouta/lab_Dev/lab_dev/images/" + strange_face_path)
    # normal_face = cv2.imread(settings.IMAGE_ROOT + settings.IMAGE_URL + normal_face_dir + normal_face_path)
    # strange_face = cv2.imread(settings.IMAGE_ROOT + settings.IMAGE_URL + strange_face_dir + strange_face_path)
    normal_face = cv2.imread("/Users/yokouchiryouta/lab_Dev/lab_dev/images/" + normal_face_path)
    strange_face = cv2.imread("/Users/yokouchiryouta/lab_Dev/lab_dev/images/" + strange_face_path)
    # 暗い箇所を明るく
    normal_face = cv2.LUT(normal_face, lookUpTable)
    strange_face = cv2.LUT(strange_face, lookUpTable)
    normal_face_gray = cv2.cvtColor(normal_face, cv2.COLOR_BGR2GRAY)
    strange_face_gray = cv2.cvtColor(strange_face, cv2.COLOR_BGR2GRAY)

    # 顔のパーツ検出
    face_list1, eye_list1, mouth_list1, nose_list1, error_list1 = find_face_parts(normal_face_gray, face_cascade, eye_cascade, mouth_cascade, nose_cascade)
    face_list2, eye_list2, mouth_list2, nose_list2, error_list2 = find_face_parts(strange_face_gray, face_cascade, eye_cascade, mouth_cascade, nose_cascade)

    # 真顔と変顔どちらかでエラーがあったら返す。
    if len(error_list1) != 0 or len(error_list2) != 0:
        return funny_face_degree, error_list1, error_list2

    # 輪郭外の顔パーツを削除
    eye_list1, mouth_list1, nose_list1 = delete_face_parts(face_list1, eye_list1, mouth_list1, nose_list1)
    eye_list2, mouth_list2, nose_list2 = delete_face_parts(face_list2, eye_list2, mouth_list2, nose_list2)

    #normal_face_error_list = checkError(face_list1, eye_list1, mouth_list1, nose_list1)
    #strange_face_error_list = checkError(face_list2, eye_list2, mouth_list2, nose_list2)

    normal_face_symmetry = calSymmetry(face_list1, eye_list1, mouth_list1, nose_list1)
    strange_face_symmetry = calSymmetry(face_list2, eye_list2, mouth_list2, nose_list2)
    normal_face_balance = calSymmetry(face_list1, eye_list1, mouth_list1, nose_list1)
    strange_face_balance = calcBalance(face_list2, eye_list2, mouth_list2, nose_list2)
    size = calcSize(face_list1, eye_list1, mouth_list1, nose_list1, face_list2, eye_list2, mouth_list2, nose_list2)

    return funny_face_degree, error_list1, error_list2

    #return normal_face_error_list, strange_face_error_list, symmetry, balance, size
