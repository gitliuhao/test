import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic.base import View


class SystemFileNamePathListApi(View):
    ''' 查看远程系统路径下文件名路径 '''
    def get(self, request, *args, **kwargs):
        jk = get_object_or_404(JenkinsConfig, pk=request.GET.get('jk_id', 0))
        server = JenkinsServer(**jk.config_to_dict())
        job_building_list = json.dumps(server.get_job_building_list())

        return HttpResponse(job_building_list, content_type="application/json")