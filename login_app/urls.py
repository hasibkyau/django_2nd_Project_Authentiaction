from django.urls import re_path as url
from django.urls import path
from login_app import views

app_name = 'login_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register')
]
