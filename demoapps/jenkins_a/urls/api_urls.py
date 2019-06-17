from django.conf.urls import url
from jenkins_a.views import api

urlpatterns = (
    url(r'^job/building/list$', api.JobBuildingListApi.as_view(), name='job-building-list'),
)