from django.db import models


class User(models.Model):
    user_name = models.CharField(max_length=20)  # 用户名
    pass_word = models.CharField(max_length=20)  # 密码
    phone = models.CharField(max_length=20)  # 电话
    email = models.CharField(max_length=30)  # 邮箱
    create_time = models.DateTimeField('create time')  # 创建时间
    power = models.CharField(max_length=30)  # 用户权限
