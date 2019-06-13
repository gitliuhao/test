from django.conf.urls import url
from . import views


urlpatterns = (
    url(r'^$', views.JenkinsView.as_view(), name='index'),
    url(r'^job/list/$', views.JobsView.as_view(), name='job-list'),
    url(r'^job/create/$', views.JobCreateView.as_view(), name='job-create'),
    url(r'^job/config/update/(?P<name>(.*))/$', views.JobUpdateView.as_view(), name='job-config-update'),
    url(r'^job/config/(?P<name>(.*))/get/$', views.JobConfigView.as_view(), name='get-job-config'),
    url(r'^build/(?P<name>(.*))/(?P<number>\d+)/$', views.JobConsoleInputView.as_view(),
        name='job-build-console-input'),
    url(r'^build/(?P<name>(.*))/$', views.JobBuildListView.as_view(), name='job-build-list'),
)