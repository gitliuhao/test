import subprocess

import paramiko
from django.conf import settings
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, CreateView

from asset.models import Asset
from asset.task import find_log_list, ControlSsh


class AssetListView(ListView):
    model = Asset


class AssetCreateView(CreateView):
    model = Asset


def tailf(request):
    server_list = settings.SERVER_DICT.keys()
    path = request.GET.get('path')
    host = request.GET.get('server_ip')
    host_conf = settings.SERVER_DICT.get(host)
    log_list = []
    if host_conf:
        xssh = ControlSsh(host=host, **host_conf)
        log_list += xssh.find_log_list(path)
    return render(request, 'asset/tailf.html', {"server_list": server_list, "path": path, 'log_list':  log_list})