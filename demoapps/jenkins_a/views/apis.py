import json

import jenkins
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.views import View

from jenkins_a.models import JenkinsConfig
from jenkins_a.utils import JenkinsServer
from django.core.cache import cache


class JobBuildingListApi(View):
    ''' 正在运行的任务构建列表'''
    def get(self, request, *args, **kwargs):
        jk = get_object_or_404(JenkinsConfig, pk=request.GET.get('jk_id', 0))
        server = JenkinsServer(**jk.config_to_dict())
        job_building_list = json.dumps(server.get_job_building_list())

        return HttpResponse(job_building_list, content_type="application/json")


class JobBuildingStopApi(View):
    ''' 中断运行中的任务构建 '''
    def post(self, request, *args, **kwargs):
        reqd = request.POST
        name, number, jk_id = reqd.get('name'), reqd.get('number'), reqd.get('jk_id', 0) or 0
        jk = get_object_or_404(JenkinsConfig, pk=jk_id)
        try:
            server = JenkinsServer(**jk.config_to_dict())
            server.stop_build(name=name, number=number)
            return JsonResponse({'success': True, 'code': 200})
        except Exception as e:
            return JsonResponse({'success': False, 'code': 400, 'error': str(e)})


class ViewListJobNameListApi(View):
    ''' 查看Viewlist任务分类及任务名称列表 '''
    def get(self, request, *args, **kwargs):
        reqd = request.GET
        jk_id = reqd.get('jk_id', 0) or 0
        jk = get_object_or_404(JenkinsConfig, pk=jk_id)
        server = JenkinsServer(**jk.config_to_dict())
        job_name_list = server.get_job_name_list()
        return HttpResponse(json.dumps(job_name_list),  content_type="application/json")


class JobBuildFaildListApi(View):
    ''' 失败的构建记录列表 '''
    def get(self, request, *args, **kwargs):
        jk_id = request.GET.get('jk_id', 0) or 0
        jk = get_object_or_404(JenkinsConfig, pk=jk_id)
        server = JenkinsServer(**jk.config_to_dict())
        name = request.GET.get('job_name')
        build_iter = server.get_all_build_iter(name=name)
        job_build_faild_list = [build for build in build_iter if build['result'] == 'FAILURE']
        return HttpResponse(json.dumps(job_build_faild_list), content_type="application/json")


class JobBuildDeleteApi(View):
    ''' 构建记录删除操作'''
    def post(self, request, *args, **kwargs):
        reqd = request.POST
        name, number, jk_id = reqd.get('name'), reqd.get('number'), reqd.get('jk_id', 0) or 0
        jk = get_object_or_404(JenkinsConfig, pk=jk_id)
        server = JenkinsServer(**jk.config_to_dict())
        try:
            server.delete_job_build(name, int(number))
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


class JobBuildApi(View):
    ''' 任务构建 '''
    def post(self, request, *args, **kwargs):
        jk_id = request.POST.get('jk_id', 0) or 0
        jk = get_object_or_404(JenkinsConfig, pk=jk_id)
        server = JenkinsServer(**jk.config_to_dict())
        name = request.POST.get('name')
        try:
            queue = server.build_job(name)
            return JsonResponse({'success': True})
        except jenkins.EmptyResponseException as e:
            return JsonResponse({'success': False, 'error': str(e)[:200]})


class JobConsoleInputApi(View):
    ''' 查看任务构建日志 '''
    def get(self, request, *args, **kwargs):
        reqd = request.GET
        name, number, jk_id = reqd.get('name'), reqd.get('number'), reqd.get('jk_id', 0) or 0
        jk = get_object_or_404(JenkinsConfig, pk=jk_id)
        server = JenkinsServer(**jk.config_to_dict())
        number = int(number)
        build_console_output = server.get_build_console_output(name=name, number=number)
        build_info = server.get_build_info(name=name, number=number)
        building = build_info['building']
        cache_name = "{number}_{name}_build_console_output_list".format(name=name, number=number)
        change_output = ''
        # 设置缓存名称
        cach_list = cache.get(cache_name)
        # 获取缓存值，如果不存在则设置缓存值
        if cach_list:
            change_output = build_console_output[len(cach_list):]
        if building:
            cache.set(cache_name, build_console_output)
        else:
            cache.delete(cache_name)

        return JsonResponse({'build_console_output': build_console_output,
                             'building': building, "change_output": change_output})
