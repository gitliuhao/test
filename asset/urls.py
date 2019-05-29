from django.conf.urls import url

from asset import views

urlpatterns = (
    url(r'^$', views.AssetListView.as_view(), name='asset-list'),
    url(r'^/create$', views.AssetCreateView.as_view(), name='asset-create'),
    url(r'^/update/(?P<id>\d+)/$', views.AssetUpdateView.as_view(), name='asset-update'),
    url(r'^/delete/(?P<id>\d+)/$', views.asset_delete, name='asset-delete'),
    url(r'^/tailf$', views.tailf, name='tailf-index'),
    url(r'^/ws/asset$', views.tailf_websocket, name='tailf-websocket'),
)