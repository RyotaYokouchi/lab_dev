from django.urls import path

from . import views

urlpatterns = [
    path('', views.menuView, name='index'),
    path('start/', views.start, name='start'),
    path('ranking/', views.RankingView.as_view(), name='ranking'),
    path('test/', views.test, name='test'),
    path('cascade/', views.getCascade, name='cascade'),
]
