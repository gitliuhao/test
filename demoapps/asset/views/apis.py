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
        xssh = ControlSsh(username=asset.username, host=asset.host, key_filename=asset.ssh_key_url())
        _, out, _ = xssh.exec_command("ls -Rlt --time=ctime /etc")
        d = out.read().decode()
        data_list = d.split("\n\n")
        text = []
        for x in data_list:
            folder_path, _, *file_list = x.split("\n")
            folder_path = folder_path[:-1]
            p_and_t = []
            for file in file_list:
                if file and file[0] == "-":
                    xlist = file.split(" ")
                    print(xlist)
                    time, file_name= " ".join(xlist[-4:-1]), xlist[-1]
                    p_and_t.append({'time': time, "file_path": folder_path+ "/" + file_name})
            if p_and_t:
                text.append(p_and_t)

        job_building_list = json.dumps(server.get_job_building_list())

        return HttpResponse(job_building_list, content_type="application/json")