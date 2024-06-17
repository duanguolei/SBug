"""
code speace
@Time    : 2024/1/24 17:38
@Author  : 泪懿:dgl
@File    : urls.py
"""
from django.urls import path,re_path,reverse,include
app_name='web'
from .views import account,home,project,manage,wiki,file,setting,issues,dashboard,statistics
urlpatterns = [
        re_path(r'^register/$',account.register,name='register'),
        re_path(r'^send/sms/$',account.send_sms,name='send_sms'),
        re_path(r'^login_sms/$',account.login_sms,name='login_sms'),
        re_path(r'^login/$',account.login,name='login'),
        re_path(r'^captch/$',account.captch,name='captch'),
        re_path(r'^logout/$',account.logout,name='logout'),
        re_path(r'^index/$',home.index,name='index'),
        re_path(r'^$',home.index,name=''),
        re_path(r'^price',home.price,name='price'),
        re_path(r'^payment/(?P<plocy_id>\d+)/$',home.payment,name='payment'),
        re_path(r'^pay/',home.pay,name='pay'),
        re_path(r'^pay_notify/$', home.pay_notify, name='pay_notify'),
            #项目管理

        re_path(r'^project/list$',project.project_list,name='project.project_list'),
        re_path(r'^project/star/(?P<project_type>\w+)/(?P<project_id>\d+)/$',project.project_star,name='project.project_star'),
        re_path(r'^project/unstar/(?P<project_type>\w+)/(?P<project_id>\d+)/$',project.project_unstar,name='project.project_unstar'),

        re_path(r'^manage/(?P<project_id>\d+)/',include(
            [

        re_path(r'^dashboard/$',dashboard.dashboard,name='dashboard'),
        re_path(r'^dashboard/issues/chart/$',dashboard.issues_chart,name='issues_chart'),

        re_path(r'^issues/$',issues.issues,name='issues'),
        re_path(r'^issues/detail/(?P<detail_id>\d+)$',issues.issues_detail,name='issues_detail'),
        re_path(r'^issues/record/(?P<issues_id>\d+)$',issues.issues_record,name='issues_record'),
        re_path(r'^issues/invite/$',issues.issues_invite,name='issues_invite'),



        re_path(r'^statistics',statistics.statistics,name='statistics'),



        re_path(r'^file/$',file.file,name='file'),
        re_path(r'^file_delete/$',file.file_delete,name='file_delete'),
        re_path(r'^file_post/$',file.file_post,name='file_post'),

        re_path(r'^cos_credential/$', file.cos_credential, name='cos_credential'),


        re_path(r'^wiki/$',wiki.wiki,name='wiki'),
        re_path(r'^wiki_add/$',wiki.wiki_add,name='wiki_add'),
        re_path(r'^wiki_delete/(?P<wiki_id>\d+)/$',wiki.wiki_delete,name='wiki_delete'),
        re_path(r'^wiki_edit/(?P<wiki_id>\d+)/$',wiki.wiki_edit,name='wiki_edit'),
        re_path(r'^wiki_upload/$',wiki.wiki_upload,name='wiki_upload'),

        re_path(r'^weki_catelog/$',wiki.weki_catelog,name='weki_catelog'),


        re_path(r'^setting/$',setting.settings,name='setting'),
        re_path(r'^setting/delete/$',setting.setting_delete,name='setting_delete'),
            ]
        ),None),

        re_path(r'mdeditor/', include('mdeditor.urls')),

        re_path(r'^invite/join/(?P<code>\w+)/$',issues.invite_join,name='invite_join'),



        ]


from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)







