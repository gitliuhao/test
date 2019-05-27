from django.conf.urls import url

from asset import views

urlpatterns = (
    url(r'^$', views.AssetListView.as_view(), name='asset-list'),
    url(r'^/tailf$', views.tailf, name='tailf-index'),
)