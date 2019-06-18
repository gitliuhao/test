from django.conf.urls import url
from jenkins_a.views import api

urlpatterns = (
    url(r'^job/building/list/$', api.JobBuildingListApi.as_view(), name='job-building-list'),
    url(r'^job/building/stop/$', api.JobBuildingStopApi.as_view(), name='job-building-stop'),
    url(r'^job/build/faild/list/$', api.JobBuildFaildListApi.as_view(), name='job-build-failed-list'),
)