"""
code speace
@Time    : 2024/3/12 12:29
@Author  : 泪懿:dgl
@File    : wiki.py
"""
from django.shortcuts import render,redirect,reverse
from django.http import JsonResponse,HttpResponse
from web import models
from utils import encrypt
from web.forms.wiki import WikiMFormModel
from utils.tencent import cos
# from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.views.decorators.csrf import csrf_exempt,csrf_protect
def wiki(request,project_id):
    wiki_id=request.GET.get('wiki_id')


    if wiki_id and wiki_id.isdigit():

        wiki_object=models.Wiki.objects.filter(id=wiki_id,project_id=request.tracer.project.id).first()
        print(wiki_object)
        return render(request, 'web/wiki.html',{'wiki_object':wiki_object})

    else:
        return render(request,'web/wiki.html')

def wiki_add(request,project_id):
    if request.method=='POST':
        form = WikiMFormModel(request,request.POST)
        if form.is_valid():
            if form.instance.parent:
                depth=form.instance.parent.depth

                form.instance.depath=depth+1
            else:

                form.instance.depath = 1


            form.instance.project=request.tracer.project
            form.save()
            url=reverse('web:wiki',kwargs={"project_id":project_id})
            return redirect(url)
        else:
            return render(request, 'web/wiki_form.html', {'form':form, 'error':form.errors})

    else:
        form=WikiMFormModel(request)
        return render(request,'web/wiki_form.html',{"form":form})

def weki_catelog(request,project_id):
    data=models.Wiki.objects.filter(project=request.tracer.project).all().values('id','title','parent_id').order_by('depth','id')
    # print(data)
    return JsonResponse({
        'status':True,
        'data':list(data)
    })

def wiki_delete(request,project_id,wiki_id):
    models.Wiki.objects.filter(project_id=project_id,id=wiki_id).delete()
    url=reverse('web:wiki',kwargs={
        'project_id':project_id
    })

    return redirect(url)


def wiki_edit(request,project_id,wiki_id):
    wiki_object=models.Wiki.objects.filter(project_id=project_id, id=wiki_id).first()
    if not wiki_object:
        url = reverse('web:wiki', kwargs={
            'project_id': project_id
        })
        return redirect(url)
    else:
        if request.method=='GET':
            form=WikiMFormModel(request, instance=wiki_object)

            return render(request,'web/wiki_form.html',{'form':form})
        else:
            form=WikiMFormModel(request,request.POST)
            if form.is_valid():
                if form.instance.parent:
                    depth = form.instance.parent.depth

                    form.instance.depath = depth + 1
                else:

                    form.instance.depath = 1
                form.instance.project = request.tracer.project
                form.instance.id=wiki_id
                form.save()
                url = reverse('web:wiki', kwargs={"project_id": project_id})
                url+='?wiki_id='+wiki_id
                return redirect(url)
            else:
                return render(request, 'web/wiki_form.html', {'form': form, 'error': form.errors})


@csrf_exempt
def wiki_upload(request,project_id):
    print('收到消息')
    image_object=request.FILES.get(
        'editormd-image-file'
    )
    if image_object:
        #文件对象上传到筒中
        img_ext=image_object.name.split('.')[-1]
        file_name_key="{}.{}".format(encrypt.uid(str(request.tracer.user.mobile_phone)),img_ext)
        bucket=request.tracer.project.bucket

        img_url=cos.upload_bucket(
            buket=bucket,
            key=file_name_key,
            image=image_object,

        )

        return JsonResponse({
            'success':1,
            'message':None,
            "url":img_url
        })
    else:
        return JsonResponse({
            'success': 0,
            'message':'文件不存在'

        })

