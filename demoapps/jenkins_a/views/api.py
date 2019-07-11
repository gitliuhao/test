import json

import jenkins
from django.http import JsonResponse, HttpResponse
from django.views import View

from jenkins_a.utils import JenkinsServer


class JobBuildingListApi(View):
    ''' 正在运行的任务构建列表'''
    def get(self, request, *args, **kwargs):
        server = JenkinsServer()
        job_building_list = json.dumps(server.get_job_building_list())

        return HttpResponse(job_building_list, content_type="application/json")


class JobBuildingStopApi(View):
    ''' 中断运行中的任务构建 '''
    def post(self, request, *args, **kwargs):
        name, number = request.POST.get('name'), request.POST.get('number')
        try:
            server = JenkinsServer()
            server.stop_build(name=name, number=number)
            return JsonResponse({'success': True, 'code': 200})
        except Exception as e:
            return JsonResponse({'success': False, 'code': 400, 'error': str(e)})


class JobBuildFaildListApi(View):
    ''' 失败的构建记录列表 '''
    def get(self, request, *args, **kwargs):
        server = JenkinsServer()
        name = request.GET.get('job_name')
        build_iter = server.get_all_build_iter(name=name)
        job_build_faild_list = [build for build in build_iter if build['result'] == 'FAILURE']
        return HttpResponse(json.dumps(job_build_faild_list), content_type="application/json")


class JobBuildDeleteApi(View):
    ''' 构建记录删除操作'''
    def post(self, request, *args, **kwargs):
        name, number = request.POST.get('name'), request.POST.get('number')
        server = JenkinsServer()
        try:
            server.delete_job_build(name, int(number))
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


class JobBuildApi(View):
    ''' 任务构建 '''
    def post(self, request, *args, **kwargs):
        server = JenkinsServer()
        name = request.POST.get('name')
        try:
            queue = server.build_job(name)
            return JsonResponse({'success': True})
        except jenkins.EmptyResponseException as e:
            return JsonResponse({'success': False, 'error': str(e)[:200]})
