"""
code speace
@Time    : 2024/3/9 12:20
@Author  : 泪懿:dgl
@File    : init_user.py
"""

from faker import Faker
Fake=Faker(locale='zh_CN')



import django
import os

basr_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import sys
sys.path.append(basr_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE','SBug.settings')
django.setup()
# print(Fake.name(),Fake.email(),Fake.phone_number(),Fake.password())

from web import models

models.UserInfo.objects.create(username=str(Fake.name()),email=Fake.email(),mobile_phone=str(Fake.phone_number()),password=Fake.password())
# models.UserInfo.objects.create(username='张三',email='esd@qq.com',mobile_phone='15778203921',password='dssdijsjfd')
# models.UserInfo.objects.create(username='陈硕', email='chengshuo@live.com', mobile_phone='13838383838', password='123123')