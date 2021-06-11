from django.db import models
import PIL

# 数据库的设计
# Create your models here.
class User(models.Model):
    # 客户名称
    name = models.CharField(max_length=200)

    # 联系电话
    phonenumber = models.CharField(max_length=200, primary_key=True)

    # 地址
    password = models.CharField(max_length=200)

    # 人脸照片
    photo = models.ImageField(upload_to='photos')