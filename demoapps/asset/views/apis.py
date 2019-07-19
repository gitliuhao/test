import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic.base import View

from asset.models import Asset
from asset.ssh_client import ControlSsh


class SystemFileNamePathListApi(View):
    ''' 查看远程系统路径下文件名路径 '''
    def get(self, request, *args, **kwargs):
        asset_id = request.GET.get('asset_id', 0) or 0
        asset = get_object_or_404(Asset, pk=asset_id)
        import datetime
        xssh = ControlSsh(**asset.config_dict())
        _, out, _ = xssh.exec_command("ls -Rl --time-style=\"+%Y-%m-%d %H:%M:%S\" /data/xls/runtime")
        d = out.read().decode()
        data_list = d.split("\n\n")
        text = []
        for x in (i for i in data_list if i):
            folder_path, _, *file_list = x.split("\n")
            folder_path = folder_path[:-1]
            for file in file_list:
                if file and file[0] == "-":
                    xlist = file.split(" ")
                    time, file_name= " ".join(xlist[-3:-1]), xlist[-1]
                    text.append({'time': time, "file_path": folder_path+ "/" + file_name})
        name_list = map(
            lambda d: d['file_path'],
            sorted(text, key=lambda x: datetime.datetime.strptime(x['time'], "%Y-%m-%d %H:%M:%S"), reverse=True))
        json_name_list = json.dumps(list(name_list))

        return HttpResponse(json_name_list, content_type="application/json")