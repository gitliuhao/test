from django.conf.urls import url
from . import views


urlpatterns = (
    url(r'^$', views.JenkinsView.as_view(), name='index'),
    url(r'^job/list/$', views.JobsView.as_view(), name='job-list'),
    url(r'^build/(?P<name>(.*))/(?P<number>\d+)/$', views.JobConsoleInputView.as_view(),
        name='job-build-console-input'),
    url(r'^build/(?P<name>(.*))/$', views.JobBuildListView.as_view(), name='job-build-list'),
)