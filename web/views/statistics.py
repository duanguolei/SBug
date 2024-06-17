"""
code speace
@Time    : 2024/3/30 13:06
@Author  : 泪懿:dgl
@File    : statistics.py
"""
from django.shortcuts import render,redirect
from django.http import JsonResponse
from web import models
from django.views.decorators.csrf import csrf_exempt

from django.db.models import Count

@csrf_exempt
def statistics(request,project_id):
    if request.method=='GET':
        return render(request,'web/statistics.html')

    else:

        charttype = request.POST.get('type')
        start = request.POST.get('start')
        end = request.POST.get('end')
        # print(charttype)
        if charttype == 'pie':
            data_dict = {}
            for key, text in models.Issues.priority_choices:
                data_dict[key] = {'name': text, 'y': 0,'z':0}

            result = models.Issues.objects.filter(project_id=project_id, create_datetime__gte=start,
                                                  create_datetime__lt=end).values('priority').annotate(
                ck=Count('id')

            )
            for item in result:
                data_dict[item['priority']]['y'] = item['ck']
                data_dict[item['priority']]['z'] = item['ck']

            return JsonResponse({
                'status': True,
                'data': list(data_dict.values())
            })

        if charttype=='projectUserLine':

            assigns=models.Issues.objects.filter(project_id=project_id, create_datetime__gte=start,
                                                   create_datetime__lt=end).values('assign').annotate(ck=Count('id'))

            assign_data = {}
            status_dict = {key: value for key,value in models.Issues.status_choices}
            status_label = models.Issues.status_choices
            categories = list(status_dict.keys())

            for assign in assigns:
                if assign['assign']:
                    assign_data[assign['assign']] = {'name': assign['assign'], 'data': [0] * len(categories)}
                else:
                    assign_data['未指派'] = {'name': '未指派', 'data': [0] * len(categories)}


            result=models.Issues.objects.filter(project_id=project_id, create_datetime__gte=start,
                                                   create_datetime__lt=end)


            for assign in assign_data.keys():
                if assign!='未指派':
                    assgin_result=result.filter(assign=assign).values('status').annotate(ck=Count('id'))
                else:
                    assgin_result = result.filter(assign=None).values('status').annotate(ck=Count('id'))

                for item in assgin_result:
                    assign_data[assign]['data'][categories.index(item['status'])] = item['ck']


            assign_listdatas=[]
            for key,value in assign_data.items():

                name=value.get('name')
                if name != '未指派':
                    username=models.UserInfo.objects.filter(id=name).first().username
                    value['name']=username
                assign_listdatas.append(value)


            return JsonResponse({'status':True,'categories':list(status_dict.values()),'data':assign_listdatas})

            result = models.Issues.objects.filter(project_id=project_id, create_datetime__gte=start,
                                                  create_datetime__lt=end).values('status')

        return JsonResponse({
            'status': True,
            'data':[]
        })