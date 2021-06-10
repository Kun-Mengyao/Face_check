from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
import json
from login.models import User


def register(request):
    info = request.params['data']

    # 从请求消息中 获取要添加客户的信息
    # 并且插入到数据库中
    # 返回值 就是对应插入记录的对象
    record = User.objects.create(name=info['name'],
                                 phonenumber=info['phonenumber'],
                                 password=info['password'],
                                 photo=info['photo'])

    return JsonResponse({'ret': 0, 'id': record.id})


def personalInfo(request):
    # 返回一个 QuerySet 对象 ，包含所有的表记录
    # 每条表记录都是是一个dict对象，
    # key 是字段名，value 是 字段值
    qs = User.objects.values()

    # 定义返回字符串
    retStr = ''
    for user in qs:
        for name, value in user.items():
            retStr += f'{name} : {value} | '

        # <br> 表示换行
        retStr += '<br>'

    return HttpResponse(retStr)
