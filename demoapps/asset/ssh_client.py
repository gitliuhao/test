from __future__ import absolute_import

import _thread
import json
import subprocess
from time import sleep

import paramiko
import threading
from django.conf import settings

from asset.utils import stop_thread


def send_line(drfsocket_instance, stdout):
    while True:
        line = stdout.readline()
        if line:
            print(line)
            drfsocket_instance.send(json.dumps(
                {
                    "type": "send.message",
                    "message": line
                }
            ).encode())  # 把内容发送到websocket服务端


class ControlSsh(object):

    def __init__(self, cmd='', host=None, username=None, port=22, password=None, key_filename=None):
        self.client = None
        self.cmd, self.host, self.username, self.port, self.password = cmd, host, username, port, password
        self.key_filename = key_filename

    @property
    def ssh_client(self):
        if self.client:
            return self.client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  #

        ssh.connect(self.host, username=self.username, password=self.password,
                    port=self.port, key_filename=self.key_filename, timeout=5)
        self.client = ssh
        return self.client

    def exec_command(self, cmd):
        # 分别保存，标准输入，标准输出，错误输出
        # stdin, stdout, stderr = ssh.exec_command(cmd)
        return self.ssh_client.exec_command(cmd)

    def find_log_list(self, path):
        cmd = "ls -a {log_path}".format(log_path=path)
        if self.host:
            _, stdout, _ = self.exec_command(cmd)
            log_list = [r for r in stdout.read().decode().split('\n') if '.log' in r]
        else:
            popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            line = popen.stdout.readlines()
            log_list = [i.decode().replace('\n', '') for i in line if '.log' in i.decode()]
        return log_list

    def send_tailf_log(self, log_path, drfsocket_instance):
        cmd = "tail -f {log_path}".format(log_path=log_path)
        # 监控远程的日志变动
        if self.host:
            _, stdout, error = self.exec_command(cmd)
            # send_line(drfsocket_instance, stdout)
            t1 = threading.Thread(target=send_line, args=(drfsocket_instance, stdout))
            t1.start()
            while True:
                if drfsocket_instance.has_messages():
                    stop_thread(t1)
                    drfsocket_instance.close()
                    break

        # 监控本地的日志变动
        else:
            popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            while True:
                line = popen.stdout.readline().strip()

                if drfsocket_instance.has_messages():
                    drfsocket_instance.read()
                    drfsocket_instance.close()
                    break
                if line:
                    drfsocket_instance.send(json.dumps(
                        {
                            "type": "send.message",
                            "code": 200,
                            "message": line.decode()
                        }
                    ).encode())  # 把内容发送到websocket服务端


def rcmd(host, password, cmd, port=22, username='root'):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  #

    ssh.connect(host, username=username, password=password, port=port)

    stdin, stdout, stderr = ssh.exec_command(cmd)  # 分别保存，标准输入，标准输出，错误输出

    data = stdout.read()
    error = stderr.read()
    return data


def find_log_list(path, server_ip=''):
    cmd = "ls -a {log_path}".format(log_path=path)
    log_list = []
    if server_ip:
        server_conf = settings.SERVER_DICT[server_ip]
        stdout = rcmd(host=server_ip, cmd=cmd, **server_conf)
        if stdout:
            log_list = [r for r in stdout.decode().split('\n') if '.log' in r]
    else:
        popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        line = popen.stdout.readlines()
        if line:
            log_list = [i.decode().replace('\n', '') for i in line if '.log' in i.decode()]
    return log_list


def tailfLog(log_path, drfsocket_instance, server_ip=''):
    cmd = "tail -f {log_path}".format(log_path=log_path)
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    while True:
        line = popen.stdout.readline().strip()  #获取内容
        if line:
            drfsocket_instance.send(json.dumps(
                {
                    "type": "send.message",
                    "message": str(line.decode())
                }
            ))   #把内容发送到websocket服务端


