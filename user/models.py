from django.db import models

# Create your models here.

class User(models.Model):

    SEX = (
        ('M','男性'),
        ('F','女性'),
        ('S','保密')
    )

    nickname = models.CharField(
        max_length=32,
        unique=True,
        verbose_name="昵称"
    )

    password = models.CharField(
        max_length=128,
        verbose_name='密码'
    )

    age = models.IntegerField(
          default=18,
          verbose_name='年龄'
    )

    sex = models.CharField(
        choices=SEX,
        max_length=8,
        verbose_name='性别'
    )

    icon = models.ImageField(
        verbose_name='头像'
    )