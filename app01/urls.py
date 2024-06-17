"""
code speace
@Time    : 2024/1/20 16:17
@Author  : 泪懿:dgl
@File    : urls.py
"""
import django.conf
from django.urls import path
from . import views
app_name="app01"
urlpatterns = [
    path("send/sms",views.send_sms),
    path("register",views.register)
]

