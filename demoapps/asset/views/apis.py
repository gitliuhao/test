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
        job_building_list = json.dumps(server.get_job_building_list())

        return HttpResponse(job_building_list, content_type="application/json")