from django.conf import settings
from django.db import models

# Create your models here.
from asset.models import Asset


class JenkinsConfig(Asset):
    url = models.URLField(verbose_name='访问地址')

    class Meta:
        verbose_name = "jenkins配置"
