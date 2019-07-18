from django.conf.urls import url
from jenkins_a.views import apis

urlpatterns = (
    url(r'^job/building/list/$', apis.JobBuildingListApi.as_view(), name='job-building-list'),
    url(r'^job/building/stop/$', apis.JobBuildingStopApi.as_view(), name='job-building-stop'),
    url(r'^job/name/list/$', apis.JobNameListApi.as_view(), name='job-name-list'),
    url(r'^job/build/faild/list/$', apis.JobBuildFaildListApi.as_view(), name='job-build-failed-list'),
    url(r'^job/build/delete/$', apis.JobBuildDeleteApi.as_view(), name='job-build-delete'),
    url(r'^job/build/console/$', apis.JobConsoleInputApi.as_view(),
        name='job-build-console-input-api'),
    url(r'^job/build/$', apis.JobBuildApi.as_view(), name='job-build'),
)