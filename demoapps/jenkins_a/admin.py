from django.contrib import admin

# Register your models here.
from asset.admin import RegisterModel
from jenkins_a.models import JenkinsConfig

RegisterModel(JenkinsConfig).register()

