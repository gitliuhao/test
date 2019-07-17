from django.conf import settings
from django.db import models

# Create your models here.
from asset.models import AssetAbstract


class JenkinsConfig(AssetAbstract):
    url = models.URLField(verbose_name='访问地址')

    class Meta:
        verbose_name = "jenkins配置"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s@%s" % (self.username, self.host)