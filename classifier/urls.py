from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('predict/', views.predict, name='predict'),
    path('predict-vgg16/', views.predict_vgg16, name='predict_vgg16'),
    path('predict-cnn/', views.predict_cnn, name='predict_cnn'),
    path('history/', views.history, name='history'),
]

