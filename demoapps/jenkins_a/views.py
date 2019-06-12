import datetime

import jenkins
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from jenkins_a.forms import JobConfForm
from jenkins_a.utils import stamp_to_datetime


class JenkinsView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse("jenkins-url:job-list"))


class JobsView(View):
    def get(self, request, *args, **kwargs):
        server = jenkins.Jenkins('http://localhost:8080', username='jenkins', password='jenkins')
        jobs_data_list = []
        for job in  server.get_all_jobs():
            job_name = job['name']
            info = server.get_job_info(name=job_name)
            job_data = {'name': job_name}
            lastBuild = info.get('lastBuild')
            if lastBuild:
                number =lastBuild['number']
                build_info = server.get_build_info(name=job_name, number=number)
                lastBuild['datetime'] = stamp_to_datetime(build_info['timestamp'], unit='ms', format="%Y-%m-%d %H:%M")
                job_data['lastBuild'] = lastBuild
            lastSuccessfulBuild = info.get('lastSuccessfulBuild')
            if lastSuccessfulBuild:
                number =lastSuccessfulBuild['number']
                build_info = server.get_build_info(name=job_name, number=number)
                lastSuccessfulBuild['datetime'] = stamp_to_datetime(build_info['timestamp'], unit='ms', format="%Y-%m-%d %H:%M")
                job_data['lastSuccessfulBuild'] = lastSuccessfulBuild
            lastFailedBuild = info.get('lastFailedBuild')
            if lastFailedBuild:
                number =lastFailedBuild['number']
                build_info = server.get_build_info(name=job_name, number=number)
                lastFailedBuild['datetime'] = stamp_to_datetime(build_info['timestamp'], unit='ms', format="%Y-%m-%d %H:%M")
                job_data['lastFailedBuild'] =  lastFailedBuild
            jobs_data_list.append(job_data)
        return render(request, 'demoapps/jenkins/job_list.html', {'jobs': jobs_data_list})


class JobBuildListView(View):
    def get(self, request, name, *args, **kwargs):
        server = jenkins.Jenkins('http://localhost:8080', username='jenkins', password='jenkins')
        job_info = server.get_job_info(name=name)
        builds = job_info.get('builds', [])
        for b in builds:
            timestamp = server.get_build_info(name=name, number=b['number'])['timestamp']
            b['datetime'] = stamp_to_datetime(timestamp, unit='ms', format="%Y-%m-%d %H:%M")
        return render(request, 'demoapps/jenkins/build_list.html', {'builds': builds, 'name': name})


class JobConsoleInputView(View):
    def get(self, request, name, number, *args, **kwargs):
        server = jenkins.Jenkins('http://localhost:8080', username='jenkins', password='jenkins')
        build_console_output = server.get_build_console_output(name=name, number=int(number))
        build_console_output_list = build_console_output.split('\n')
        return render(request, 'demoapps/jenkins/console_input.html', {'build_console_output_list': build_console_output_list})


class JobCreateView(View):
    def get(self, request, *args, **kwargs):
        forms = JobConfForm()
        return render(request, 'demoapps/jenkins/job_config_form.html', {'forms': forms})