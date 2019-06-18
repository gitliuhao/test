import json

from django.http import JsonResponse, HttpResponse
from django.views import View

from jenkins_a.utils import JenkinsServer


class JobBuildingListApi(View):
    def get(self, request, *args, **kwargs):
        server = JenkinsServer()
        return HttpResponse(json.dumps(server.get_job_building_list()), content_type="application/json")


class JobBuildingStopApi(View):
    def post(self, request, *args, **kwargs):
        name, number = request.POST.get('name'), request.POST.get('number')
        try:
            server = JenkinsServer()
            server.stop_build(name=name, number=number)
            return JsonResponse({'success': True, 'code': 200})
        except Exception as e:
            return JsonResponse({'success': False, 'code': 400, 'error': str(e)})


class JobBuildFaildListApi(View):
    def get(self, request, *args, **kwargs):
        server = JenkinsServer()
        return HttpResponse(json.dumps(server.get_job_build_faild_list()), content_type="application/json")