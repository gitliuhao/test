from django.conf import settings
from django.db import models

# Create your models here.


class Asset(models.Model):
    username = models.CharField(max_length=20, blank=True, verbose_name='用户名')
    host = models.CharField(max_length=20, blank=True, verbose_name='主机ip', unique=True)
    ssh_secret_key = models.FileField(verbose_name='ssh远程秘钥', upload_to='ssh_key')

    def ssh_key_url(self):
        return "{d_path}{s_path}".format(d_path=settings.BASE_DIR, s_path=self.ssh_secret_key.url)

    class Meta:
        verbose_name = "主机"
