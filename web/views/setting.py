"""
code speace
@Time    : 2024/3/19 12:29
@Author  : 泪懿:dgl
@File    : setting.py
"""
from web import models
from django.shortcuts import  render,redirect
from django.http import JsonResponse
from utils.tencent import cos

def settings(request,project_id):
    return render(request,'web/settings.html')



def setting_delete(request,project_id):
    if request.method=='GET':

        return render(request,'web/setting_delete.html')

    else:
        project_name=request.POST.get('project_name')
        if not project_name or project_name!=request.tracer.project.name:
            return render(request, 'web/setting_delete.html',{"eorro":'项目名错误'})
        else:
            #只有当前创建者可以删除

            if request.tracer.project.creator!=request.tracer.user:
                return render(request, 'web/setting_delete.html', {"eorro": '项目创建者可以删除错误'})

            cos.delete_bucket(request.tracer.project.bucket)
            models.Project.objects.filter(name=request.tracer.project.name).first().delete()
            return redirect('web:project.project_list')





