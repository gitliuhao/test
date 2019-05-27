import subprocess

import paramiko
from django.conf import settings
from django.shortcuts import render

# Create your views here.
from tailf.task import find_log_list, ControlSsh


def tailf(request):
    server_list = settings.SERVER_DICT.keys()
    path = request.GET.get('path')
    host = request.GET.get('server_ip')
    host_conf = settings.SERVER_DICT.get(host)
    log_list = []
    if host_conf:
        xssh = ControlSsh(host=host, **host_conf)
        log_list += xssh.find_log_list(path)
    return render(request, 'tailf/index.html', {"server_list": server_list, "path": path, 'log_list':  log_list})