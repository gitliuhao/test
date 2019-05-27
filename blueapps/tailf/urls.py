from django.conf.urls import url
from tailf import views

urlpatterns = (
    url(r'^$', views.tailf, name='tailf-index'),
)