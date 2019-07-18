from django.conf.urls import url
from jenkins_a.views import views


urlpatterns = (
    url(r'^job/building/list/$', views.JobBuildingListView.as_view(), name='job-building-list'),
    url(r'^job/build/failed/list/$', views.JobBuildFaildList.as_view(), name='job-build-failed-list'),
    url(r'^$', views.JenkinsView.as_view(), name='index'),
    url(r'^job/list/$', views.JobsView.as_view(), name='job-list'),
    url(r'^job/create/$', views.JobCreateView.as_view(), name='job-create'),
    url(r'^job/(?P<name>(.*))/delete/$', views.JobDeleteView.as_view(), name='job-delete'),
    url(r'^job/config/update/(?P<name>(.*))/$', views.JobUpdateView.as_view(), name='job-config-update'),
    url(r'^job/config/(?P<name>(.*))/get/$', views.JobConfigView.as_view(), name='get-job-config'),
    url(r'^job/build/$', views.JobBuildView.as_view(), name='get-job-build'),
    url(r'^build/(?P<name>(.*))/(?P<number>\d+)/console/$', views.JobConsoleInputView.as_view(),
        name='job-build-console-input'),
    # url(r'^build/(?P<name>(.*))/(?P<number>\d+)/console/api/$', views.JobConsoleInputApi.as_view(),
    #     name='job-build-console-input-api'),

    url(r'^build/(?P<name>(.*))/list/$', views.JobBuildListView.as_view(), name='job-build-list'),
    url(r'^build/(?P<name>(.*))/list/api/$', views.JobBuildListApi.as_view(), name='job-build-list-api'),
)