from django.db import models

# Create your models here.

class User(models.Model):

    SEX = (
        ('男性','男性'),
        ('女性','女'),
        ('保密','保密')
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

    plt_icon = models.URLField(
        default='',
        verbose_name='第三方平台url',
    )

    @property
    def avatar(self):
        #统一的头像地址
        return self.plt_icon if self.plt_icon else self.icon.url
