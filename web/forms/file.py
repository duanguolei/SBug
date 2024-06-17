"""
code speace
@Time    : 2024/3/14 17:15
@Author  : 泪懿:dgl
@File    : file.py
"""
from django import forms

from web import models
from django.core.exceptions import ValidationError
from .bookstrapform import BootStrapForm
class FileModalForm(BootStrapForm,forms.ModelForm):

    class Meta:
        model=models.FileRepository
        fields=['name']

    def __init__(self,request,parent_object,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.request=request
        self.parent_object=parent_object

    def clean_name(self):

        name=self.cleaned_data.get('name')

        #判断当前目录下的是否存在

        if self.parent_object:
            exit = models.FileRepository.objects.filter(file_type=2, name=name, project=self.request.tracer.project,
                                                        parent=self.parent_object
                                                        ).exists()


        else:
            exit = models.FileRepository.objects.filter(file_type=2, name=name, project=self.request.tracer.project,
                                                       parent__isnull=True).exists()

        if exit:
            raise ValidationError("文件夹已存在")

        return name


