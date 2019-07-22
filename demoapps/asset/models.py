from django.conf import settings
from django.db import models


# Create your models here.
class AssetAbstract(models.Model):
    hostname = models.CharField(max_length=50, verbose_name='主机名', unique=True)
    username = models.CharField(max_length=20, verbose_name='用户名')
    host = models.CharField(max_length=20, blank=True, verbose_name='主机ip', unique=True)
    port = models.IntegerField(blank=True, verbose_name='端口', default=22)
    ssh_secret_key = models.FileField(verbose_name='ssh远程秘钥', upload_to='ssh_key')
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def ssh_key_url(self):
        return "{d_path}{s_path}".format(d_path=settings.BASE_DIR, s_path=self.ssh_secret_key.url)

    def config_dict(self):
        ''' 用于远程登录的配置'''
        return {
            'key_filename': self.ssh_key_url(),
            'username': self.username,
            'host': self.host,
            'port': self.port
        }

    class Meta:
        abstract = True


class Asset(AssetAbstract):
    class Meta:
        verbose_name = "主机"
        verbose_name_plural = "主机列表"

    def __str__(self):
        return "%s@%s" % (self.username, self.host)


class Project(models.Model):
    name = models.CharField(max_length=50, verbose_name='项目名称')
    path = models.CharField(max_length=30, verbose_name='项目路径', default='/data/xls/runtime')
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    assets = models.ManyToManyField(Asset, related_name='projects', verbose_name='所在主机')

    class Meta:
        verbose_name = "项目"
        verbose_name_plural = "项目列表"

    def __str__(self):
        return "%s" % self.name
