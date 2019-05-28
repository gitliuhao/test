import subprocess

import paramiko
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from asset.forms import AssetForm
from asset.models import Asset
from asset.task import find_log_list, ControlSsh


class AssetListView(ListView):
    model = Asset


class AssetCreateView(CreateView):
    form_class = AssetForm
    template_name = 'asset/asset_form.html'
    success_url = '/asset'
    model = Asset

    def get_context_data(self, **kwargs):
        kwargs['title']='创建主机配置'
        return super().get_context_data(**kwargs)


class AssetUpdateView(UpdateView):
    pk_url_kwarg = 'id'
    form_class = AssetForm
    template_name = 'asset/asset_form.html'
    success_url = '/asset'
    model = Asset

    def get_context_data(self, **kwargs):
        kwargs['title']='修改主机配置'
        return super().get_context_data(**kwargs)


def asset_delete(request, id):
    asset = get_object_or_404(Asset, pk=id)
    asset.delete()
    return JsonResponse({'success': '删除成功'})


def tailf(request):
    assets = Asset.objects.all()
    path = request.GET.get('path')
    asset_id = request.GET.get('asset_id')
    log_list = []
    kwargs_data = {"assets": assets, "path": path, 'log_list':  log_list}
    if asset_id:
        asset = get_object_or_404(Asset, pk=asset_id)
        kwargs_data['select_asset'] = asset
        xssh = ControlSsh(username=asset.username, host=asset.host, key_filename=asset.ssh_key_url())
        log_list += xssh.find_log_list(path)
    return render(request, 'asset/tailf.html', kwargs_data)