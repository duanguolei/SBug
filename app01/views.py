import random

from django.shortcuts import render

# Create your views here.
from utils.tencent.sms import send_sms_single,send_sms_multi
from django.shortcuts import HttpResponse

from django.conf import settings
def send_sms(request):
    """
    发送短信
    :param request:
    :return:
    ?tpl=login
    ?tpl=register
    """
    tpl=request.GET.get('tpl')
    phone=request.GET.get('phe')

    template_id=settings.TENCENT_SMS_TYPE.get(tpl)
    if not template_id:
        return HttpResponse("模型不存在")

    code=random.randrange(100000,999999)
    if tpl=='register':
        res=send_sms_single(
        '15770289601',template_id,[code,5]
        )
    else:
        res = send_sms_single(
            '15770289601', template_id, [code]
        )

    if res['result']==0:
        return HttpResponse("发送成功")
    else:
        return HttpResponse(res['errmsg'])

from .form import RegisterMOdelForm
from django import forms

def register(request):
    form=RegisterMOdelForm()
    return render(request, 'app01/register.html', {'form':form})




