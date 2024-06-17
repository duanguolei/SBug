"""
code speace
@Time    : 2024/3/7 20:29
@Author  : 泪懿:dgl
@File    : auth.py
"""
import datetime
import copy

from django.utils.deprecation import MiddlewareMixin
from web import models
from django.shortcuts import render,redirect
from django.conf import settings

class Tracer(object):
    def __init__(self):
        self.user=None
        self.price_policy=None
        self.project=None



class AuthMIddleware(MiddlewareMixin):
    def process_request(self,request):
        """
        如果用户登录，request 中赋值
        :param request:
        :return:
        """

        trace=Tracer()

        user=request.session.get('user_id',-1)

        user_obj=models.UserInfo.objects.filter(id=user).first()
        if user_obj:
            trace.user=user_obj



        #黑名单:没有登录不可以访问

        for url in settings.BLACK_REGEX_URL_LIST:
            if url in request.path_info:
                if not  user_obj:
                    return redirect('web:login')
                else:
                    if_projects=True

        if user_obj:
            transaction_object = models.Transaction.objects.filter(user=user_obj, status=2).order_by('-id').first()
            # 判断是否过期
            if transaction_object:
                current_datetime = datetime.datetime.now()
                if transaction_object.end_datetime and transaction_object.end_datetime < current_datetime:
                    transaction_object = models.Transaction.objects.filter(user=user_obj, status=2, count=0).first()
            else:
                transaction_object = models.Transaction.objects.filter(user=user_obj, status=2, count=0).first()


            trace.price_policy = transaction_object.price_policy
        request.tracer = trace


    def process_view(self, request, view, *args, **kwargs):

        # 判断URL是否是以manage开头，如果是则判断项目ID是否是我创建 or 参与
        if not request.path_info.startswith('/web/manage/'):
            return

        args_lsits=copy.copy(args)
        for i in args_lsits:
            if isinstance(i,dict):
                project_id=i.get('project_id',0)
                if project_id:
                    break


        # 是否是我创建的
        project_object = models.Project.objects.filter(creator=request.tracer.user, id=project_id).first()
        if project_object:
            # 是我创建的项目的话，我就让他通过
            request.tracer.project = project_object
            return

        # 是否是我参与的项目
        project_user_object = models.ProjectUser.objects.filter(user=request.tracer.user, project_id=project_id).first()
        if project_user_object:
            # 是我参与的项目
            request.tracer.project = project_user_object.project
            return

        return redirect('web:project.project_list')











