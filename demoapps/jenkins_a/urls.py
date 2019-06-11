from django.conf.urls import url
from . import views


urlpatterns = (
    url(r'^$', views.JenkinsView.as_view(), name='index'),
    url(r'^job/list/$', views.JobsView.as_view(), name='job-list'),
)