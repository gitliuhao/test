import json

import jenkins
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from jenkins_a.forms import JobConfForm
from jenkins_a.models import JenkinsConfig
from jenkins_a.utils import stamp_to_datetime, JenkinsServer


class JobBuildingListView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'objects': JenkinsConfig.objects.all()
        }
        return render(request, 'demoapps/jenkins/job_building_list.html', context)


class JobBuildFaildList(View):
    def get(self, request, *args, **kwargs):
        context = {
            'objects': JenkinsConfig.objects.all()
        }
        return render(request, 'demoapps/jenkins/job_build_faild_list.html', context)


class JenkinsView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse("jenkins_a-url:job-build-failed-list"))


class JobsView(View):
    def get(self, request, *args, **kwargs):
        j_server = JenkinsServer()
        jobs_data_list = j_server.get_all_job_details()
        return render(request, 'demoapps/jenkins/job_list.html', {'jobs': jobs_data_list})


class JobBuildListView(View):
    def get(self, request, name, *args, **kwargs):
        return render(request, 'demoapps/jenkins/build_list.html', {'name': name})


class JobBuildListApi(View):
    def get(self, request, name, *args, **kwargs):
        server = JenkinsServer()
        job_info = server.get_job_info(name=name)
        builds = job_info.get('builds', [])
        for b in builds:
            build_info = server.get_build_info(name=name, number=b['number'])
            timestamp = build_info['timestamp']
            b['detail'] = build_info
            b['datetime'] = stamp_to_datetime(timestamp, unit='ms', format="%Y-%m-%d %H:%M")
        return HttpResponse(json.dumps(builds), content_type="application/json")


class JobConsoleInputView(View):
    def get(self, request, name, number, *args, **kwargs):
        server = jenkins.Jenkins('http://localhost:8080', username='jenkins', password='jenkins')
        build_console_output = server.get_build_console_output(name=name, number=int(number))
        build_console_output_list = build_console_output.split('\n')
        return render(request, 'demoapps/jenkins/console_input.html',
                      {'build_console_output_list': build_console_output_list,
                       'name': name, 'number': number})


class JobCreateView(View):
    ''' Job 创建'''

    def get(self, request, *args, **kwargs):
        forms = JobConfForm()
        return render(request, 'demoapps/jenkins/job_config_form.html', {'forms': forms})

    def post(self, request, *args, **kwargs):
        forms = JobConfForm(data=request.POST, files=request.FILES)
        if not forms.is_valid():
            return render(request, 'demoapps/jenkins/job_config_form.html', {'forms': forms})

        j_server = JenkinsServer()
        data = forms.cleaned_data
        name, config_xml = data['name'], data['config_xml']
        cx = config_xml.file.read().decode()
        try:
            j_server.create_job(name=name, config_xml=cx)
        except Exception as e:
            return render(request, 'demoapps/jenkins/job_config_form.html', {'forms': forms, 'error': str(e)[:100]})
        return HttpResponseRedirect(reverse('jenkins_a-url:job-list'))


class JobDeleteView(View):
    def get(self, request, name, *args, **kwargs):
        server = JenkinsServer()
        server.delete_job(name)
        return JsonResponse({'success': '删除成功'})


class JobUpdateView(View):
    ''' Job 配置修改 '''

    def get(self, request, name, *args, **kwargs):
        forms = JobConfForm(initial={'name': name})
        return render(request, 'demoapps/jenkins/job_config_form.html', {'forms': forms})

    def post(self, request, name, *args, **kwargs):
        forms = JobConfForm(data=request.POST, files=request.FILES)
        if not forms.is_valid():
            return render(request, 'demoapps/jenkins/job_config_form.html', {'forms': forms})

        j_server = JenkinsServer()
        data = forms.cleaned_data
        name, config_xml = data['name'], data['config_xml']
        cx = config_xml.file.read().decode()
        try:
            j_server.create_job(name=name, config_xml=cx)
        except Exception as e:
            return render(request, 'demoapps/jenkins/job_config_form.html', {'forms': forms, 'error': str(e)[:100]})
        return HttpResponseRedirect(reverse('jenkins_a-url:job-list'))


class JobConfigView(View):
    ''' Job 获取配置文件'''

    def get(self, request, name, *args, **kwargs):
        j_server = JenkinsServer()
        job_xml = j_server.get_job_config(name)
        response = HttpResponse(job_xml, content_type="application/xml")
        response['Content-Disposition'] = 'attachment;filename="%s.xml"' % name
        return response


class JobBuildView(View):
    ''' Job 立即构建
    '''

    def post(self, request, *args, **kwargs):
        server = JenkinsServer()
        name = request.POST.get('name')
        try:
            queue = server.build_job(name)
            return JsonResponse({'succes': True})
        except jenkins.EmptyResponseException as e:
            return JsonResponse({'succes': False, 'error': str(e)[:200]})
