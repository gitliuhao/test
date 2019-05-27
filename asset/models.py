from django.db import models

# Create your models here.


class Asset(models.Model):
    username = models.CharField(max_length=20, blank=True, verbose_name='用户名')
    host = models.CharField(max_length=20, blank=True, verbose_name='主机ip')
    ssh_secret_key = models.FileField(verbose_name='ssh远程秘钥')

    class Meta:
        verbose_name = "主机"
