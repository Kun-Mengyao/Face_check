from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def register_page(request):
    return HttpResponse("注册界面")
