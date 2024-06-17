"""
code speace
@Time    : 2024/1/25 11:05
@Author  : 泪懿:dgl
@File    : account.py
"""
import uuid

from web.forms.account import RegisterMOdelForm,SendSmsForm,LoginSmsForm,LoginForm
from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from django.conf import settings
from web import models
from django_redis import get_redis_connection
from django.db.models import Q
from utils.captacher import get_img_code
import datetime
def register(request):

    if request.method=='GET':
        form = RegisterMOdelForm()

        return render(request,'web/register.html',{"form":form})

    else:
        form = RegisterMOdelForm(request.POST)
        if form.is_valid():
            instance=form.save()
            policy=models.PricePolcy.objects.filter(category=1).first()
            models.Transaction.objects.create(
                status=2,
                order=str(uuid.uuid4()),
                user=instance,
                price_policy=policy,
                count=0,
                price=0,
                start_datetime=datetime.datetime.now(),
            )

            return JsonResponse(
                {'status':True,'data':'/web/login/',
                 }
            )
        else:
            return JsonResponse(
                {'status':False,'error':form.errors}
            )



def send_sms(request):

    form=SendSmsForm(request,data=request.GET)

    mobile_phone = request.GET.get('mobile_phone')
    tpl = request.GET.get('tpl')
    sms_template_id = settings.TENCENT_SMS_TYPE[tpl]

    if form.is_valid():
        # 发送短信
        #写入redis
        return JsonResponse({
            'status':True
        })
    else:
        return JsonResponse({
            'status':False,'error':form.errors
        })

def login_sms(request):
    if request.method=='GET':
        form=LoginSmsForm()

        return render(request,'web/login_sms.html',{'form':form})
    else:
        form=LoginSmsForm(request.POST)
        if form.is_valid():
            user_Obj = models.UserInfo.objects.filter(mobile_phone=form.cleaned_data['mobile_phone']).first()
            request.session['user_id'] = user_Obj.id
            request.session.set_expiry(60 * 60 * 24)
            return JsonResponse(
                {'status':True,'data':'/web/index/'}
            )
        else:
            return JsonResponse(
                {'status':False,'error':form.errors}
            )


def login(request):
    if request.method=='GET':
        form=LoginForm(request)
        return  render(request,'web/login.html',{'form':form})
    else:
        form=LoginForm(request,data=request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            # user_Obj=models.UserInfo.objects.filter(username=username,password=password).filter()
            user_Obj=models.UserInfo.objects.filter(Q(email=username)|Q(mobile_phone=username)|Q(username=username)).filter(password=password).first()

            if user_Obj:
                request.session['user_id']=user_Obj.id
                request.session.set_expiry(60*60*24)
                return JsonResponse(
                {'status': True, 'data': "/web/index/"}
            )
            else:
                form.add_error('username', '用户名或密码错误')
                return JsonResponse({"status": False, 'error': form.errors})

        return JsonResponse({"status": False, 'error': form.errors})

def captch(request):
    """
    生成图片验证码
    :param request:
    :return:
    """
    code,img=get_img_code()
    request.session['captch_code']=code
    request.session.set_expiry(60)

    from io import BytesIO
    stram=BytesIO()
    img.save(stram,'png')

    return HttpResponse(
        stram.getvalue()
    )

def logout(request):
    request.session.flush()
    return redirect('web:login')

