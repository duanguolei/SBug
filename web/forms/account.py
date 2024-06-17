"""
code speace
@Time    : 2024/3/6 13:18
@Author  : 泪懿:dgl
@File    : account.py
"""
import random

from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django import forms
from django.conf import settings
from web import models

from django_redis import get_redis_connection

from utils.tencent.sms import send_sms_single
from utils.encrypt import md5
from .bookstrapform import BootStrapForm


class RegisterMOdelForm(BootStrapForm,forms.ModelForm):
    #重写
    mobile_phone = forms.CharField(label='手机号', validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误'), ])
    password = forms.CharField(
        label='密码',
        min_length=6,
        max_length=32,
        error_messages={
            'min_length':'密码长度不低于6个字符',
            'max_length':"密码长度不多于32个字符"
        }
        ,

        widget=forms.PasswordInput(attrs={
        'class':'form-control','placeholder':"input password"
    }))

    #添加字段
    comfirm_password=forms.CharField(label='再次输入密码',widget=forms.PasswordInput(
        attrs={
        'class':'form-control','placeholder':"input confirm password"
    }
    ))
    code=forms.CharField(label='验证码',widget=forms.TextInput(attrs={
        'class':'form-control','placeholder':"input code"
    }))
    class Meta:
        model=models.UserInfo
        fields=['username','email','password','comfirm_password',
                'mobile_phone','code']


    #初始化重写



    def clean_username(self):
        model = models.UserInfo
        username=self.cleaned_data['username']
        if model.objects.filter(username=username).exists():
            # raise ValidationError(f"{username} 用户名已存在")
            self.add_error('username','用户已存在')


        return username

    def clean_email(self):
        model = models.UserInfo
        email= self.cleaned_data['email']
        if model.objects.filter(email=email).exists():
            raise ValidationError(f"{email} 邮箱已存在")

        return email

    def clean_code(self):

        code=self.cleaned_data['code'].strip()
        redis=get_redis_connection()
        redis_code=redis.get(self.cleaned_data['mobile_phone'])
        if not redis_code:
            raise ValidationError("请先获取验证码")
        if str(code)!=str(redis_code.decode('utf-8')):
            raise ValidationError("验证码错误，请重新获取")

        return code

    def clean_mobile_phone(self):
        model = models.UserInfo
        mobile_phone= self.cleaned_data['mobile_phone']
        if model.objects.filter(mobile_phone=mobile_phone).exists():
            # raise ValidationError(f"{mobile_phone} 手机号码已被使用")
            self.add_error('mobile_phone','电话号码已被使用')
        return mobile_phone


    def clean_password(self):
        pwd=self.cleaned_data['password']
        # 加密
        pwd=md5(pwd)

        return pwd


def clean_comfirm_password(self):
        confilm_password=self.cleaned_data['comfirm_password']
        confilm_password=md5(confilm_password)
        password=self.cleaned_data['password']
        if password!=confilm_password:
            raise ValidationError("两次密码不一致，请重新输入")





class SendSmsForm(forms.Form):
    mobile_phone = forms.CharField(label='手机号', validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误'), ])

    def __init__(self,request,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.request=request



    def clean_mobile_phone(self):
        mobile_phone=self.cleaned_data['mobile_phone']
        tpl=self.request.GET.get('tpl')
        template_id=settings.TENCENT_SMS_TYPE.get(tpl,0)
        if not template_id:
            raise ValidationError('短信类型不存在')

        exists=models.UserInfo.objects.filter(mobile_phone=mobile_phone).exists()
        if tpl=='login':
            if not exists:
                raise ValidationError("手机号不存在")

        if tpl=='register':
            if exists:
                raise ValidationError("手机号已经存在")

        #发送短信 写入redis
        conn = get_redis_connection()
        code=random.randrange(1000,9999)
        if tpl=='login':
            if conn.get(mobile_phone):
                raise ValidationError(f'请等待60s后重新获取')
            sms = send_sms_single(mobile_phone, template_id, [code, ])
            if str(sms['result']) != '0':
                raise ValidationError(f'短信发送失败:{sms["errmsg"]}')
            conn.set(mobile_phone, code, ex=360)

        if tpl=='register':

            if  conn.get(mobile_phone):
                raise ValidationError(f'请等待60s后重新获取')

            sms=send_sms_single(mobile_phone,template_id,[code,1])
            if str(sms['result']) != '0':
                raise ValidationError(f'短信发送失败:{sms["errmsg"]}')
            conn.set(mobile_phone, code, ex=60)

        return mobile_phone

class LoginSmsForm(BootStrapForm,forms.Form):
    mobile_phone = forms.CharField(label='手机号', validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误'), ])
    code = forms.CharField(label='验证码', widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': "input code"
    }))



    def clean_code(self):
        mobile_phone=self.cleaned_data['mobile_phone']
        redis=get_redis_connection()
        if not redis.get(mobile_phone):
            raise ValidationError('请先获取或者重新获取验证码')

        code=self.cleaned_data['code']
        redis_code=redis.get(mobile_phone).decode('utf-8')
        if code.strip()!=redis_code:
            raise ValidationError("验证码错误")
        return code

class LoginForm(BootStrapForm,forms.Form):
    username=forms.CharField(label='用户名或邮箱或电话号码',)

    password=forms.CharField(label='密码',min_length=6,max_length=32,     error_messages={
            'min_length':'密码长度不低于6个字符',
            'max_length':"密码长度不多于32个字符"
        },widget=forms.PasswordInput(render_value=True))

    code=forms.CharField(label='图片验证码')


    def __init__(self,request,*args,**kwargs):
        self.request=request
        super().__init__(*args,**kwargs)

    def clean_code(self):

        code=self.cleaned_data['code']

        session_code=self.request.session.get('captch_code')
        if not  session_code:
            raise ValidationError("验证码过期，请重新点击")
        if code.upper().strip()!=session_code.upper():
            raise ValidationError("验证码输入错误")
        return code

    def clean_password(self):
        return md5(self.cleaned_data['password'])






