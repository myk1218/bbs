from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.CharField(
        max_length=64,
        verbose_name="标题"
    )
    created = models.DateTimeField(
        auto_now_add=True, #创建时间
        verbose_name="创建时间"
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name="更新时间"
    )
    content = models.TextField(
        max_length=255,
        verbose_name="内容"
    )