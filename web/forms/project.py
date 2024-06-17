"""
code speace
@Time    : 2024/3/9 20:23
@Author  : 泪懿:dgl
@File    : project.py
"""
from django import forms
from .bookstrapform import BootStrapForm
from web.forms.widgets import  ColorRadioSelect
from web import models
from django.core.exceptions import ValidationError
class ProjectModelForm(BootStrapForm,forms.ModelForm):
    bookstrap_class_exclude=['color']
    def __init__(self,request,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.request=request


    class Meta:

        model=models.Project
        fields=['name','color','desc']
        widgets={
            'desc':forms.Textarea(),
            'color':forms.RadioSelect()
        }

    def clean_name(self):
        """
        项目校验

        :return:
        """
        name = self.cleaned_data['name']
        exit=models.Project.objects.filter(name=name,creator=self.request.tracer.user).exists()
        if exit:
            raise ValidationError("该项目已存在")

        project_num=self.request.tracer.price_policy.project_num

        if project_num<=models.Project.objects.filter(creator=self.request.tracer.user).count():
            raise ValidationError("项目创建额度已满，创建失败")

        return name

    def clean_color(self):
        color=self.cleaned_data['color']
        return color
