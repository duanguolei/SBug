"""
code speace
@Time    : 2024/3/11 20:13
@Author  : 泪懿:dgl
@File    : manage.py
"""

from django.shortcuts import render,redirect


# def dashboard(request,project_id):
#     return render(request,'web/dashborad.html')


def statistics(request,project_id):
    return render(request,'web/statistics.html')






