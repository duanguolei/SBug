"""
code speace
@Time    : 2024/3/9 18:21
@Author  : 泪懿:dgl
@File    : project.py
"""
import time

from django.shortcuts import render,redirect
from web import models
from django.urls import reverse
from qcloud_cos import CosConfig
from utils.tencent import cos
from qcloud_cos import CosS3Client
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from web.forms.project import ProjectModelForm

@csrf_exempt
def project_list(request):
    if request.method=='GET':
        #查看项目列表
        project_dict = {
            'star': [],
            'my': [],
            'join': []
        }
        projects=models.Project.objects.filter(
            creator=request.tracer.user
        ).all()
        for row in projects:
            if row.star:
                project_dict['star'].append({'value':row,'type':'my'})
            else:
                project_dict['my'].append({'value':row,'type':'my'})

        joinedProjects=models.ProjectUser.objects.filter(user=request.tracer.user)
        for item in joinedProjects:
            if item.star:
                project_dict['star'].append({'value':item.project,'type':'join'})
            else:
                project_dict['join'].append({'value':item.project,'type':'join'})

        form=ProjectModelForm(request)

        return render(request,'web/project_list.html',{'form':form,'project_dict':project_dict})
    else:
        form =ProjectModelForm(request,request.POST)
        if form.is_valid():
            form.instance.creator=request.tracer.user
            """
            {手机号}-{时间}--}-1314084628
            """
            bucket="{}-{}-1314084628".format(str(request.tracer.user.mobile_phone),str(int(time.time()*1000)))
            regin='ap-chengdu'


            cos.create_bucket(bucket)
            form.instance.bucket=bucket
            form.instance.region=regin
            form.save()

            PROJECT_INIT_LIST=models.IssuesType.PROJECT_INIT_LIST
            for type in PROJECT_INIT_LIST:
                issuertype=models.IssuesType(title=type,
                                             project=form.instance)
                issuertype.save()

            return JsonResponse({'status':True})
        else:
            return JsonResponse({'status':False,'error':form.errors})



def project_star(request,project_type,project_id):
    """
    星标项目
    :param request:
    :return:
    """
    if project_type=='my':

        models.Project.objects.filter(id=project_id,creator=request.tracer.user).update(star=True)
        return redirect('web:project.project_list')

    if project_type=='join':
        models.ProjectUser.objects.filter(project_id=project_id,user=request.tracer.user).update(star=True)
        return redirect('web:project.project_list')

    return HttpResponse('请求错误')

def project_unstar(request,project_type,project_id):
    """
    星标项目
    :param request:
    :return:
    """
    if project_type=='my':

        models.Project.objects.filter(id=project_id,creator=request.tracer.user).update(star=False)
        return redirect('web:project.project_list')

    if project_type=='join':
        models.ProjectUser.objects.filter(project_id=project_id,user=request.tracer.user).update(star=False)
        return redirect('web:project.project_list')

    HttpResponse('请求错误')




