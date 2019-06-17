from django.http import JsonResponse
from django.views import View

from jenkins_a.utils import JenkinsServer


class JobBuildingListApi(View):
    def get(self, request, *args, **kwargs):
        server = JenkinsServer()
        return JsonResponse(server.get_running_builds())