from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
import json
from login.models import User
import cv2


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
        response.status_code=400
        return response
    # 从请求消息中 获取要添加客户的信息
    # 并且插入到数据库中
    # 返回值 就是对应插入记录的对象
    record = User.objects.create(name=info['name'],
                                 phonenumber=info['phonenumber'],
                                 password=info['password'],
                                 photo=info['photo'])
    response = HttpResponse()
    response.status_code = 200
    return response
    # return JsonResponse({'ret': 0, 'phonenumber': record.phonenumber})


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