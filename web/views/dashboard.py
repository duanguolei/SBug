"""
code speace
@Time    : 2024/3/28 12:03
@Author  : 泪懿:dgl
@File    : dashboard.py
"""
import collections
import time

from django.shortcuts import render,redirect
from django.http import JsonResponse
from web import models
from django.db.models import Count
import datetime
from django.views.decorators.csrf import csrf_exempt
def dashboard(request,project_id):
    """
    问题数据处理
    :param request:
    :param project_id:
    :return:
    """
    # 分组计算数量
    isuues_state_dict={}
    for key,text in models.Issues.status_choices:
        isuues_state_dict[key]={'text':text,'count':0}

    issues_data=models.Issues.objects.filter(project_id=project_id).values('status').annotate(
        ct=Count('id')
    )
    for item in issues_data:
        isuues_state_dict[item['status']]['count']=item['ct']

    user_name=models.ProjectUser.objects.filter(project_id=project_id).values_list('user_id','user__username')


    top_ten=models.Issues.objects.filter(project_id=project_id,assign__isnull=False).order_by('-id')[:10]


    return render(request,'web/dashborad.html',{'states_dict':isuues_state_dict,
                                                'user_list':user_name,
                                                'top_ten':top_ten
                                                })
@csrf_exempt
def issues_chart(request,project_id):
    #
    """
    查询数据库最近30的所有的数据
    :param request:
    :param project_id:
    :return:
    """
    today=datetime.datetime.now().date()
    # select xxxx,1 as ctime from xxxx
    # select id,name,email from table;
    # select id,name, strftime("%Y-%m-%d",create_datetime) as ctime from table;
    # "DATE_FORMAT(web_transaction.create_datetime,'%%Y-%%m-%%d')"

    date_dict={}

    for i in range(0,30):
        date=today-datetime.timedelta(days=i)
        date_dict[date.strftime("%Y-%m-%d")]=[time.mktime(date.timetuple())*1000,0]
    # print(date_dict)
    # result = models.Issues.objects.filter(project_id=project_id,
    #                                       create_datetime__gte=today - datetime.timedelta(days=30)).\
    #     extra(
    #     select={'ctime': """strftime(web_issues.create_datetime,"%%Y-%%m-%%d")"""}).values('ctime').annotate(ct=Count('id'))
    #这里两个%%告诉数据库这个实占位符

    result = models.Issues.objects.filter(project_id=project_id,
                                          create_datetime__gte=today - datetime.timedelta(days=30)).values('create_datetime','id')



    deel_result=[]
    for value in result.values():
        date=value['create_datetime'].strftime("%Y-%m-%d")
        deel_result.append(date)

    for item in deel_result:

        date_dict[item][1] += 1

    print(date_dict)


    data=list(date_dict.values())
    data.reverse()
    return JsonResponse({'status':True,'data':data})