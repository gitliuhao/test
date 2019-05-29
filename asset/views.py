from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from dwebsocket import accept_websocket

from asset.forms import AssetForm
from asset.models import Asset
from asset.task import ControlSsh


# Create your views here.


class AssetListView(ListView):
    model = Asset


class AssetCreateView(CreateView):
    form_class = AssetForm
    template_name = '../templates/asset/asset_form.html'
    success_url = reverse_lazy('asset-url:asset-list')
    model = Asset

    def get_context_data(self, **kwargs):
        kwargs['title']='创建主机配置'
        return super().get_context_data(**kwargs)


class AssetUpdateView(UpdateView):
    pk_url_kwarg = 'id'
    form_class = AssetForm
    template_name = 'asset/asset_form.html'
    success_url = reverse_lazy('asset-url:asset-list')
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
    return render(request, '../templates/asset/tailf.html', kwargs_data)


@accept_websocket
def tailf_websocket(request):
    if request.is_websocket():#判断是不是websocket连接
        path, log_name = request.GET.get('path'), request.GET.get('log_name')

        asset_id = request.GET.get('asset_id')[0]
        asset = get_object_or_404(Asset, pk=asset_id)
        xssh = ControlSsh(username=asset.username, host=asset.host, key_filename=asset.ssh_key_url())
        log_path = path+log_name if path[-1] == "/" else path+'/'+log_name
        xssh.send_tailf_log(log_path, request.websocket)