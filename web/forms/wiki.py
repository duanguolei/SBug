"""
code speace
@Time    : 2024/3/12 13:10
@Author  : 泪懿:dgl
@File    : wiki.py
"""
from django import forms
from django.core.exceptions import ValidationError
from web import models
from .bookstrapform import BootStrapForm
class WikiMFormModel(BootStrapForm,forms.ModelForm):
    class Meta:
        model=models.Wiki
        #移除
        exclude=[
            'project','depth'
        ]



    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 找到想要的字段把他绑定显示的数据重置
        # 数据 = 去数据库中获取 当前项目所有的wiki标题

        total_data_list = [("", "请选择"),]
        data_list = models.Wiki.objects.filter(project=request.tracer.project).values_list('id', 'title')
        total_data_list.extend(data_list)

        self.fields['parent'].choices = total_data_list

    def clean_content(self):

        content=self.cleaned_data['content']

        if "<script" in content or '<ifram' in content or '<style' in content:
            raise  ValidationError('不能出现非法字符')

        return content

