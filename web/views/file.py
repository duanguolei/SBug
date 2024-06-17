"""
code speace
@Time    : 2024/3/14 16:21
@Author  : 泪懿:dgl
@File    : file.py
"""
import json

import requests
from django.conf import settings
from django.shortcuts import  render,redirect,reverse
from django.http import JsonResponse
from web import models
from django.forms import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from utils.tencent.cos import delete_file,delete_file_list,create_cos_credential
from utils.utils import has_emoji

from web.forms.file import FileModalForm

@csrf_exempt
def file(request,project_id):
    """
    文件列表
    添加文件夹
    :param request:
    :param project_id:
    :return:
    """
    parent_object=None

    if request.method=='GET':

        """
        当前目录下所有文件夹
        """
        floder_id = request.GET.get('folder', 0)
        breadcrumb_list=[]
        if floder_id:
            parent_object=models.FileRepository.objects.filter(id=floder_id).first()
            parent=parent_object
            while  parent:
                # breadcrumb_list.insert(0,{
                #     'id':parent.id,
                #     'name':parent.name,
                # }
                breadcrumb_list.insert(0,model_to_dict(parent,['id','name'])
                                       )
                parent=parent.parent


        query_set = models.FileRepository.objects.filter(project=request.tracer.project)
        if parent_object:
            file_list=query_set.filter(parent=parent_object)
        else:
            file_list = query_set.filter(parent__isnull=True)

        form=FileModalForm(request,parent_object)
        return render(request,'web/file.html',{"form":form,'file_object_list':file_list,
                                               'breadcrumb_list':breadcrumb_list
                                               })

    else:
        parent_object=None
        # print(request)
        floder_id=request.GET.get('folder','')
        if floder_id.isdecimal():
            parent_object=models.FileRepository.objects.filter(
                file_type=2,
                project=request.tracer.project,
                id=floder_id,

            ).first()

        # print(floder_id,parent_object)
        fid=request.POST.get('fid','')
        edit_object=None
        if fid.isdecimal():
            edit_object=models.FileRepository.objects.filter(id=int(fid),file_type=2,project=request.tracer.project).first()

        if edit_object:
            form = FileModalForm(request, parent_object, request.POST,instance=edit_object)
        else:
            form = FileModalForm(request, parent_object, request.POST)

        if form.is_valid():
            form.instance.project=request.tracer.project
            form.instance.file_type=2
            form.instance.update_user=request.tracer.user
            form.instance.parent=parent_object
            form.save()

            return JsonResponse({
                    'status':True
                })


        else:
            return JsonResponse({
                'status':False,
                'error':form.errors,
            })

@csrf_exempt
def file_delete(request,project_id):
    fid=request.POST.get('fid','')
    if fid.isdecimal():
        #删除数据库中的文件以及级联删除
        delete_object=models.FileRepository.objects.filter(id=fid,project=request.tracer.project,update_user=request.tracer.user).first()
        if delete_object.file_type==1:
            #删除文件
            #文件大小返回回去
            file_size=delete_object.file_size
            request.tracer.project.use_space-=file_size
            request.tracer.project.save()

            delete_file(bucket=request.tracer.project.bucket,
                        key=delete_object.key
                        )


        else:
            #删除文件夹以及下面的内容
            total_size=0
            folder_list=[delete_object,]
            key_list=[]
            for foldeer in folder_list:
                child_list=models.FileRepository.objects.filter(
                    project=request.tracer.project,parent=foldeer).order_by('-file_type')

                for child in child_list:
                    if child.file_type==2:
                        folder_list.append(child)
                    else:
                        total_size+=child.file_size
                        key_list.append(
                            {'key':child.key}
                                        )
            delete_file_list(bucket=request.tracer.project.bucket,
                                    key_list=key_list
                                    )

            request.tracer.project.use_space -= total_size
            request.tracer.project.save()
        delete_object.delete()
        return JsonResponse(
            {'status':True}
        )


from sts.sts import Sts
@csrf_exempt
def cos_credential(request,project_id,):
    # print(request.POST)

    file_datas=json.loads(request.body.decode('utf-8'))['data']
    total_size=0

    per_file_size=request.tracer.price_policy.per_file_size

    for file in file_datas:
        # print(file)
        if file['size']>per_file_size*1024*1024:
            return JsonResponse({'status':False,'error':f'单文件超出限制,{file["name"]}超出限制，限制最大文件为{per_file_size}M,可升级套餐'})
        total_size+=file['size']
        # print(file['name'],has_emoji(file['name']))
        if has_emoji(file['name']):
            return JsonResponse({'status':False,'error':f'文件 {file["name"]} 名称存在非法字符，请重新上传'})



    use_space=request.tracer.project.use_space
    project_space=request.tracer.price_policy.project_space*1024*1024*1024

    if use_space+total_size>project_space:
        return JsonResponse({
            'status':False,'error':'容量超过限制，尝试升级套餐或清理空间  '
        })



    result=create_cos_credential(bucket=request.tracer.project.bucket,region=request.tracer.project.region)
    result['status']=True

    return JsonResponse(result)


@csrf_exempt
def file_post(request,project_id,):
    post_type = request.POST.get('type', '')
    folderid = request.POST.get('folderid', '')
    key = request.POST.get('key', '')
    name = request.POST.get('name', '')
    parent_object = None
    if folderid.isdecimal():
        parent_object = models.FileRepository.objects.filter(
            file_type=2,
            project=request.tracer.project,
            id=folderid,

        ).first()


    if post_type=='check':
        exit=models.FileRepository.objects.filter(
            name=name,parent=parent_object,project=request.tracer.project
        ).exists()
        if exit:
            return JsonResponse({
                'status':False,
                'error': f'{name}已存在'
            })
        else:
            return JsonResponse({
                'status':True,
            })

    if post_type=='save':
        size=request.POST.get('file_size','')
        file_path=request.POST.get('file_path','')
        etag=request.POST.get('etag','')
        file_object= models.FileRepository.objects.filter(
            name=name, parent=parent_object, project=request.tracer.project
        ).first()
        if file_object:
            delete_file(
                request.tracer.project.bucket,file_object.key
            )
            request.tracer.project.use_space = int(file_object.file_size)
            file_object.delete()

        form = FileModalForm(
                request, parent_object, request.POST
            )

        if form.is_valid():
            form.instance.parent = parent_object
            form.instance.update_user = request.tracer.user
            form.instance.project = request.tracer.project
            form.instance.key = key

            form.instance.file_type = 1
            form.instance.file_size = size
            form.instance.file_path = f"https://{request.tracer.project.bucket}.cos.{request.tracer.project.region}.myqcloud.com/{key}"

            form.save()

            request.tracer.project.use_space += int(size)
            request.tracer.project.save()

            return JsonResponse({
                'status': True
            })


    return JsonResponse({})

