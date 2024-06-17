"""
code speace
@Time    : 2024/3/20 13:49
@Author  : 泪懿:dgl
@File    : issues.py
"""
from django import forms
from web import models
from .bookstrapform import BootStrapForm

class IssuesModalFrom(BootStrapForm,forms.ModelForm):


    class Meta:
        model=models.Issues
        exclude=[
            'project',
            'creator',
            'create_datetime',
            'latest_update_datetime'

        ]
        # data - live - search=true 可以搜索功能
        # 'data-actions-box'多选或者单选
        widgets={
            'assign':forms.Select(attrs={'class':'selectpicker','data-live-search':'true'}),
            'attention':forms.SelectMultiple(attrs={'class':'selectpicker','data-live-search':'true','data-actions-box':'true'}),
            "parent": forms.Select(attrs={'class': "selectpicker", "data-live-search": "true"}),
        }

    def __init__(self,request,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.request=request


        #获取问题类型
        self.fields['issues_type'].choices = models.IssuesType.objects.filter(
            project=request.tracer.project).values_list('id', 'title')

        #2当前项目的所有模块

        module_list=[('','没有任何选中选项')]
        module_object_list=models.Module.objects.filter(project=request.tracer.project).values_list('id','title')
        module_list.extend(module_object_list)
        self.fields['module'].choices=module_list



        # 3.指派和关注者
        # 数据库找到当前项目的参与者 和 创建者
        total_user_list = [(request.tracer.project.creator_id, request.tracer.project.creator.username), ]
        project_user_list = models.ProjectUser.objects.filter(project=request.tracer.project).values_list('user_id',
                                                                                                          'user__username')
        total_user_list.extend(project_user_list)

        self.fields['assign'].choices = [("", "没有选中任何项")] + total_user_list
        self.fields['attention'].choices = total_user_list

        # 4. 当前项目已创建的问题
        parent_list = [("", "没有选中任何项")]
        parent_object_list = models.Issues.objects.filter(project=request.tracer.project).values_list('id', 'subject')
        parent_list.extend(parent_object_list)
        self.fields['parent'].choices = parent_list








class IssuesReplyModalFrom(BootStrapForm,forms.ModelForm):

    class Meta:

        model=models.IssuesRely
        fields=['content','reply_type']


class InviteModelFrom(BootStrapForm,forms.ModelForm):
    class Meta:
        model=models.ProjectInvite
        fields=['period','count']




