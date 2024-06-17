"""
code speace
@Time    : 2024/3/20 13:28
@Author  : 泪懿:dgl
@File    : issues.py
"""
import datetime
import requests

import pytz
from django.shortcuts import render,reverse
from web.forms.issues import IssuesModalFrom,IssuesReplyModalFrom,InviteModelFrom
from django.http import JsonResponse,HttpResponse
from web.models import Issues,IssuesRely
# from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.views.decorators.csrf import  csrf_exempt
from django.utils.safestring import mark_safe
from  web import models
from utils.pagination import Pagination
from utils.encrypt import uid
class  CheckFilter(object):
    def __init__(self,name,datalist,request):
        self.data_list=datalist
        self.name=name
        self.request=request

    def __iter__(self):
        for item in self.data_list:
            key = str(item[0])
            text = item[1]
            ck = ""
            # 如果当前用户请求的URL中status和当前循环key相等
            value_list = self.request.GET.getlist(self.name)
            if key in value_list:
                ck = 'checked'
                value_list.remove(key)
            else:
                value_list.append(key)

            # 为自己生成URL
            # 在当前URL的基础上去增加一项
            # status=1&age=19
            from django.http import QueryDict
            query_dict = self.request.GET.copy()
            query_dict._mutabler = True
            query_dict.setlist(self.name, value_list)

            param_url = query_dict.urlencode()
            if param_url:
                url = "{}?{}".format(self.request.path_info, param_url)  # status=1&status=2&status=3&xx=1
            else:
                url = self.request.path_info

            tpl = '<a class="cell" href="{url}"><input type="checkbox" {ck} /><label>{text}</label></a>'
            html = tpl.format(url=url, ck=ck, text=text)
            yield mark_safe(html)

class SelectFilter(object):
    def __init__(self, name, data_list, request):
        self.name = name
        self.data_list = data_list
        self.request = request

    def __iter__(self):
        yield mark_safe("<select class='select2' multiple='multiple' style='width:100%;' >")
        for item in self.data_list:

            key = str(item[0])
            text = item[1]

            selected = ""
            value_list = self.request.GET.getlist(self.name)
            if key in value_list:
                selected = 'selected'
                value_list.remove(key)
            else:
                value_list.append(key)

            query_dict = self.request.GET.copy()
            query_dict._mutable = True
            query_dict.setlist(self.name, value_list)


            param_url = query_dict.urlencode()
            if param_url:
                url = "{}?{}".format(self.request.path_info, param_url)  # status=1&status=2&status=3&xx=1
            else:
                url = self.request.path_info

            html = "<option value='{url}' {selected} >{text}</option>".format(url=url, selected=selected, text=text)
            yield mark_safe(html)
        yield mark_safe("</select>")

def issues(request,project_id):
    """
    主页
    :param request:
    :param project_id:
    :return:
    """

    if request.method=='GET':

        #每页渲染5个
        limit_page = 5


        #获取用户传参，删选
        allow_filter_name=['issues_type','module','subject',
                           'priority','status','assign','attention',
                           'mode','parent']

        condition={}
        for name in allow_filter_name:
            value_list=request.GET.getlist(name)
            if not value_list:
                condition
            else:
                condition['{}__in'.format(name)]=value_list

        issues_all_list=Issues.objects.filter(project=request.tracer.project).filter(**condition).all()

        page_object = Pagination(
            current_page=request.GET.get('page',1),
            all_count=issues_all_list.count(),
            base_url=request.path_info,
            query_params=request.GET,
            per_page=limit_page,
        )
        contacts= issues_all_list[page_object.start:page_object.end]

        # now_page=request.GET.get('page',1)
        # paginator=Paginator(issues_all_list,page)
        #
        #
        # try:
        #     contacts=paginator.page(now_page)
        # except PageNotAnInteger:
        #     # 如果用户请求的页码号不是整数，显示第一页
        #     contacts = paginator.page(1)
        # except EmptyPage:
        #     # 如果用户请求的页码号超过了最大页码号，显示最后一页
        #     contacts = paginator.page(paginator.num_pages)



        form=IssuesModalFrom(request)

        project_issues_type = models.IssuesType.objects.filter(project_id=project_id).values_list('id', 'title')

        project_total_user = [(request.tracer.project.creator_id, request.tracer.project.creator.username,)]
        join_user = models.ProjectUser.objects.filter(project_id=project_id).values_list('user_id', 'user__username')
        project_total_user.extend(join_user)

        invite_form=InviteModelFrom()


        return render(request,'web/issues.html',{"form":form,
                                                 'page_html': page_object.page_html(),
                                                 'invite_form':invite_form,
                                                 'item_list':contacts,
                                                 'filter_list': [
                                                     {'title': "问题类型",
                                                      'filter': CheckFilter('issues_type', project_issues_type,
                                                                            request)},
                                                     {'title': "状态",
                                                      'filter': CheckFilter('status', Issues.status_choices,
                                                                            request)},
                                                     {'title': "优先级",
                                                      'filter': CheckFilter('priority', Issues.priority_choices,
                                                                            request)},
                                                     {'title': "指派者",
                                                      'filter': SelectFilter('assign', project_total_user, request)},
                                                     {'title': "关注者",
                                                      'filter': SelectFilter('attention', project_total_user, request)},
                                                 ]
                                                 })

    else:
        form=IssuesModalFrom(request,request.POST)
        if form.is_valid():
            form.instance.project=request.tracer.project
            form.instance.creator=request.tracer.user

            form.save()
            return JsonResponse({'status':True})
        else:

            return JsonResponse({'status':False,"error": form.errors})


@csrf_exempt
def issues_detail(request,project_id,detail_id):
    if request.method=='GET':
        issues_object=None
        if detail_id:
            issues_object=Issues.objects.filter(id=detail_id,project=request.tracer.project).first()
            if issues_object:
                form=IssuesModalFrom(request,instance=issues_object)
                return render(request, 'web/issues_detai.html',{'form':form,'issues_object':issues_object})
    else:
        if detail_id:
            import copy
            issues_object = Issues.objects.filter(id=detail_id, project=request.tracer.project).first()
            issues_object_copy=copy.copy(issues_object)
            form = IssuesModalFrom(request, request.POST, instance=issues_object)
            if form.is_valid():

                issuesRely=IssuesRely()
                issuesRely.reply_type=1
                issuesRely.issues=issues_object

                changed_fields = form.changed_data

                iseersesRely_dict={
                    'issues_type':'问题类型',
                    'module':'问题模块',
                    'subject':'问题主题',
                    'desc':'问题描述',
                    'priority':'问题优先级',
                    'status':'问题状态',
                    'assign':'问题指派',
                    'attention':'问题关注者',
                    'mode':'问题模式',
                    'parent':'父问题',}


                content=f'{request.tracer.user.username}:'

                for fileds in changed_fields:
                    filed_object=Issues._meta.get_field(fileds)
                    if fileds in ['priority','status','mode','parent']:
                        if fileds=='priority':
                            origin=issues_object_copy.get_priority_display()
                            laster=form.instance.get_priority_display()
                        if fileds=='status':
                            origin = issues_object_copy.get_status_display()
                            laster = form.instance.get_status_display()
                        if fileds=='mode':
                            origin = issues_object_copy.get_mode_display()
                            laster = form.instance.get_mode_display()
                        if fileds=='parent':
                            origin = issues_object_copy.get_parent_display()
                            laster = form.instance.get_parent_display()

                        content+=iseersesRely_dict.get(fileds)+f': {origin} 修改为:{laster}<br>'
                    else:

                        origin = getattr(issues_object_copy, fileds)
                        laster = getattr(form.instance, fileds)

                        content += iseersesRely_dict.get(fileds) + f': {origin} 修改为:{laster}<br>'

                issuesRely.content=content

                issuesRely.creator=request.tracer.user
                issuesRely.save()
                form.save()

                return JsonResponse({'status': True})

            else:
                return JsonResponse({'status': False, 'error': form.errors})











    return render(request, 'web/issues_detai.html')

@csrf_exempt
def issues_record(request,project_id,issues_id):

    if request.method=='GET':

        reply_list=IssuesRely.objects.filter(issues_id=issues_id,issues__project=request.tracer.project)
        #将queryset转换成json格式
        data_list=[]
        for row in reply_list:
            data={
                'id':row.id,
                'reply_type_text':row.get_reply_type_display(),#得到对应字符
                'content':row.content,
                'creator':row.creator.username,
                'date':row.create_datetime.strftime('%Y-%m-%d %H:%M'),

            }
            if row.reply:
                data['parent_id']=row.reply.id
            else:
                data['parent_id']=''
            data_list.append(data)

        return JsonResponse({'status':True,'datas':data_list})
    else:
        #这里案例说应该是用modelFrom 但是算了，不用了，暂时，有时间又改

        form=IssuesReplyModalFrom(request.POST)
        reply_id = request.POST.get('reply_id', None)

        if form.is_valid():
            form.instance.creator = request.tracer.user
            form.instance.issues = Issues.objects.filter(id=issues_id).first()

            if reply_id:
                form.instance.reply = IssuesRely.objects.filter(id=reply_id).first()

            form.save()
            return JsonResponse({
                    'status': True
                })
        else:
            return JsonResponse({
                'status': False, 'eorro': form.errors
            })


def issues_invite(request,project_id):
    if request.method=='POST':
        form=InviteModelFrom(request.POST)
        if form.is_valid():
            """
            生成的验证,
            save to db
            only creator can make
            """
            result={'status':True,'error':''}
            if request.tracer.user!=request.tracer.project.creator:
                form.add_error('period','无权创建邀请码')
                result['status']=False
                result['error']=form.errors

                return JsonResponse(result)

            random_invite_code=uid(request.tracer.user.mobile_phone)
            form.instance.project=request.tracer.project
            form.instance.code=random_invite_code
            form.instance.creator=request.tracer.user
            form.save()

            url_path=reverse('web:invite_join',kwargs={'code':random_invite_code})

            url='{scheme}://{host}{path}'.format(
                scheme=request.scheme,
                host=request.get_host(),
                path=url_path
            )

            result['code']=url

            return JsonResponse(result)

        else:
            return JsonResponse({'status':False,'error':form.errors})


def invite_join(request,code):
    invite_object=models.ProjectInvite.objects.filter(code=code).first()

    if not invite_object:
        return render(request,'web/invite_join.html',{'error':'邀请码不存在'})

    if invite_object.project.creator==request.tracer.user:
        return render(request, 'web/invite_join.html', {'error': '创建者无需加入'})

    if models.ProjectUser.objects.filter(project=invite_object.project,user=request.tracer.user).exists():
        return render(request, 'web/invite_join.html', {'error': '你已加入，无需加入'})

    #当前项目的创建者
    near_transation=models.Transaction.objects.filter(user=invite_object.project.creator,status=2).order_by('-id').first()
    project_member=near_transation.price_policy.project_member



    #目前成员数量
    current_member=invite_object.use_count

    most_member=invite_object.count
    if current_member >= project_member:
        return render(request, 'web/invite_join.html', {'error': '项目成员已满,无法加入'})

    if most_member:
        if current_member >= most_member :
            return render(request, 'web/invite_join.html', {'error': '该链接邀请次数已满,无法加入'})

    curent_date=datetime.datetime.now()
    limit_time=invite_object.create_datetime+datetime.timedelta(minutes=invite_object.period)
    curent_date = curent_date.replace(tzinfo=pytz.timezone('Asia/Shanghai'))
    limit_time=limit_time.replace(tzinfo=pytz.timezone('Asia/Shanghai'))
    if curent_date>limit_time:
        return render(request, 'web/invite_join.html', {'error': '邀请码已过期'})

    invite_object.use_count=invite_object.use_count+1
    invite_object.project.join_count+=1
    invite_object.save()
    invite_object.project.save()

    models.ProjectUser.objects.create(user=request.tracer.user,project=invite_object.project)
    models.ProjectUser.save()


    return render(request, 'web/invite_join.html', {'status':True,'project':invite_object})














