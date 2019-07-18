from django.conf.urls import url
from ..views import apis

urlpatterns = (
    url(r'^system/filename/list/$', apis.SystemFileNamePathListApi.as_view(), name='system-filename-list'),
)