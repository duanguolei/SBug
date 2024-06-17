"""
code speace
@Time    : 2024/3/11 19:22
@Author  : 泪懿:dgl
@File    : project.py
"""
from django.template import Library
from web import models

from django.urls import reverse

register = Library()


@register.inclusion_tag('web/inclusion/all_project_list.html')
def all_project_lsit(request):
    my_projects_list=models.Project.objects.filter(creator=request.tracer.user)

    join_projects_list=models.ProjectUser.objects.filter(user=request.tracer.user)
    return {
        'my':my_projects_list,
        'join':join_projects_list,
        'request':request
    }




@register.inclusion_tag('web/inclusion/manage_menu_list.html')
def manage_menu_list(request):
    data_list = [
        {'title': '概览', 'url': reverse("web:dashboard", kwargs={'project_id': request.tracer.project.id})},
        {'title': '问题', 'url': reverse("web:issues", kwargs={'project_id': request.tracer.project.id})},
        {'title': '统计', 'url': reverse("web:statistics", kwargs={'project_id': request.tracer.project.id})},
        {'title': 'wiki', 'url': reverse("web:wiki", kwargs={'project_id': request.tracer.project.id})},
        {'title': '文件', 'url': reverse("web:file", kwargs={'project_id': request.tracer.project.id})},
        {'title': '配置', 'url': reverse("web:setting", kwargs={'project_id': request.tracer.project.id})},
    ]

    for item in data_list:
        # 当前用户访问的URL：request.path_info:  /manage/4/issues/xxx/add/
        if request.path_info.startswith(item['url']):
            item['class'] = 'active'

    return {'data_list': data_list}




@register.filter
def divide_by_1024(value):
    try:
        return round(float(value) / 1024,2)
    except (TypeError, ValueError):
        return value


@register.filter
def string_num_just(num):
    if num<100:
        num=str(num).rjust(3,'0')

    return '#{}'.format(num)


@register.filter()
def dovide_file_type(value):
    file_extensions = {
        'image': ['png', 'jpg', 'jpeg', 'gif', 'bmp'],
        'word': ['docx','doc'],
        'video': ['mp4', 'avi', 'mov', 'wmv', 'mkv'],
        'audio': ['mp3', 'wav', 'ogg', 'flac', 'aac'],
        'pdf': ['pdf',"PDF"],
        'excel': ['xls', 'xlsx', 'csv', 'ods'],
        'powerpoint': ['ppt', 'pptx'],
        'zip': ['zip', 'rar', 'tar', '7z'],
        'code': ['html', 'css', 'js', 'py', 'java', 'cpp', 'c'],
        'database': ['sql', 'db', 'mdb', 'accdb'],

        'text': ['txt', 'log', 'md'],
        'audio': ['mp3', 'wav', 'ogg'],
        'video': ['mp4', 'avi', 'mkv'],

    }
    type=value.split('.')[-1]
    for key,values in file_extensions.items():
        if type.strip() in values:
            return key

    return 'o'


@register.filter()
def user_space(size):
    size=abs(size)
    if size>=1024**3:
        return str(round(size/(1024**3),2))+' GB'
    elif size>=1024**2:
        return str(round(size/(1024**2),2)) +" MB"

    elif size>=1024:
        return str(round(size/1024,2))+' KB'


    else:
        return str(round(size,2))+' B'