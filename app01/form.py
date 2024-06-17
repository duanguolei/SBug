"""
code speace
@Time    : 2024/1/24 10:30
@Author  : 泪懿:dgl
@File    : form.py
"""
from . import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django import forms
class RegisterMOdelForm(forms.ModelForm):
    #重写
    mobile_phone=forms.CharField(label="手机号",validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9]\g{9}$)'
                                                        ,"手机号码格式错误")])
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control','placeholder':"input password"
    }))

    #添加字段
    comfirm_password=forms.CharField(label='重置密码',widget=forms.PasswordInput(
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = '请输入%s' % (field.label,)



