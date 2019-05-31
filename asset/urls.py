from django.conf.urls import url

from asset import views

urlpatterns = (
    # url(r'^$', views.asset, name='asset-list'),
    url(r'^$', views.local_tailf, name='local-tailf'),
    url(r'^create/$', views.AssetCreateView.as_view(), name='asset-create'),
    url(r'^update/(?P<id>\d+)/$', views.AssetUpdateView.as_view(), name='asset-update'),
    url(r'^delete/(?P<id>\d+)/$', views.asset_delete, name='asset-delete'),
    url(r'^tailf/$', views.tailf, name='tailf-index'),
    # url(r'^local-tailf/$', views.local_tailf, name='local-tailf'),
    url(r'^local-file/$', views.local_file_list, name='local-file'),
    url(r'^ws/asset/tailf/$', views.tailf_socket, name='tailf-websocket'),
    url(r'^ws/local-asset/tailf/$', views.local_tailf_socket, name='local-tailf-websocket'),
)