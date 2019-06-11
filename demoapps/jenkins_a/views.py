from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View


class JenkinsView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse("jenkins-url:job-list"))


class JobsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'demoapps/jenkins/job_list.html')
