from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
import json
from login.models import User
from django.contrib.auth import authenticate, login
import cv2
import os

'''
{
    "name":"小明",
    "phonenumber":"13345679934",
    "password":"123456",
    "photo":"jpg.jpg"
}
'''


# 注册
def register(request):
    request.params = json.loads(request.body)
    info = request.params
    if User.objects.filter(phonenumber=info['phonenumber']).exists():
        response = HttpResponse()
        response.status_code = 400
        return response
    # 从请求消息中 获取要添加客户的信息
    # 并且插入到数据库中
    # 返回值 就是对应插入记录的对象
    record = User.objects.create(name=info['name'],
                                 phonenumber=info['phonenumber'],
                                 password=info['password'],
                                 photo=info['photo'])
    return JsonResponse({'ret': 0, 'phonenumber': record.phonenumber})


# 登录
def signIn(request):
    # 从 HTTP POST 请求中获取用户名、密码参数
    request.params = json.loads(request.body)
    info = request.params
    print(info)
    if User.objects.filter(phonenumber=info['phonenumber'], password=info['password']).exists():
        request.session['phonenumber'] = info['phonenumber']
        return JsonResponse({'ret': 0, 'phonenumber': info['phonenumber']})
    # 使用 Django auth 库里面的 方法校验用户名、密码
    # user = authenticate(phonenumber=info['phonenumber'], password=info['password'])
    #
    # # 如果能找到用户，并且密码正确
    # print(user)
    # if user is not None:
    #     print(11)
    #     if user.is_active:
    #         if user.is_superuser:
    #             login(request, user)
    #             # 在session中存入用户类型
    #             request.session['usertype'] = 'mgr'
    #
    #             return JsonResponse({'ret': 0})
    #         else:
    #             return JsonResponse({'ret': 1, 'msg': '请使用管理员账户登录'})
    #     else:
    #         return JsonResponse({'ret': 0, 'msg': '用户已经被禁用'})

    # 否则就是用户名、密码有误
    response = HttpResponse()
    response.status_code = 400
    return response


def faceCheck(request):
    if request.method == 'POST':
        if request.FILES:
            myFile = request.FILES.get('userfile')
            print(myFile)
            if myFile:
                dir = os.path.abspath('.')
                destination = open(os.path.join(dir, myFile.name),
                                   'wb+')
                for chunk in myFile.chunks():
                    destination.write(chunk)
                destination.close()
        return HttpResponse('ok')


def personalInfo(request):
    # 返回一个 QuerySet 对象 ，包含所有的表记录
    # 每条表记录都是是一个dict对象，
    # key 是字段名，value 是 字段值
    # qs = User.objects.values()
    #
    # # 定义返回字符串
    # retStr = ''
    # for user in qs:
    #     for name, value in user.items():
    #         retStr += f'{name} : {value} | '
    #
    #     # <br> 表示换行
    #     retStr += '<br>'
    # print(qs)
    # return HttpResponse(retStr)

    qs = User.objects.values().filter(phonenumber='19865488784')
    print(qs)
    return HttpResponse(qs)


def picShow(request):
    # path = request.GET['img_path']                # 使用params，参数在url上
    path = json.loads(request.body)['img_path']
    ret_img_data = open(path, 'rb').read()

    return HttpResponse(ret_img_data, content_type='image/jpg')
