from django.conf import settings
from django.db import models

# Create your models here.
from asset.models import Asset


class JenkinsConfig(models.Model):
    nickname = models.CharField(max_length=50, verbose_name='别名')
    username = models.CharField(max_length=20, verbose_name='用户名')
    password = models.CharField(max_length=20, verbose_name='密码')
    url = models.URLField(verbose_name='访问地址')
    config_path = models.CharField(verbose_name='jenkins数据储存路径', default='~/.jenkins', max_length=50)
    asset = models.OneToOneField(Asset, verbose_name='主机', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "jenkins配置"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s" % self.url

    def config_to_dict(self):
        asset = self.asset
        return {
            'username': self.username,
            'password': self.password,
            'config_path': self.config_path,
            'url': self.url,
            'asset': {
                'key_filename': asset.ssh_key_url(),
                'host': asset.host,
                'username': asset.username,
            }
        }