from django.conf.urls import url
from jenkins_a.views import api

urlpatterns = (
    url(r'^job/building/list/$', api.JobBuildingListApi.as_view(), name='job-building-list'),
    url(r'^job/building/stop/$', api.JobBuildingStopApi.as_view(), name='job-building-stop'),
    url(r'^job/name/list/$', api.JobNameListApi.as_view(), name='job-name-list'),
    url(r'^job/build/faild/list/$', api.JobBuildFaildListApi.as_view(), name='job-build-failed-list'),
    url(r'^job/build/delete/$', api.JobBuildDeleteApi.as_view(), name='job-build-delete'),
    url(r'^job/build/console/$', api.JobConsoleInputApi.as_view(),
        name='job-build-console-input-api'),
    url(r'^job/build/$', api.JobBuildApi.as_view(), name='job-build'),
)