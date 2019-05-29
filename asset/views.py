from django.http import jsonresponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import listview, createview, updateview
from dwebsocket import accept_websocket

from asset.forms import assetform
from asset.models import asset
from asset.task import controlssh


# create your views here.


class assetlistview(listview):
    model = asset


class assetcreateview(createview):
    form_class = assetform
    template_name = 'asset/asset_form.html'
    success_url = '/asset'
    model = asset

    def get_context_data(self, **kwargs):
        kwargs['title']='创建主机配置'
        return super().get_context_data(**kwargs)


class assetupdateview(updateview):
    pk_url_kwarg = 'id'
    form_class = assetform
    template_name = 'asset/asset_form.html'
    success_url = '/asset'
    model = asset

    def get_context_data(self, **kwargs):
        kwargs['title']='修改主机配置'
        return super().get_context_data(**kwargs)


def asset_delete(request, id):
    asset = get_object_or_404(asset, pk=id)
    asset.delete()
    return jsonresponse({'success': '删除成功'})


def tailf(request):
    assets = asset.objects.all()
    path = request.get.get('path')
    asset_id = request.get.get('asset_id')
    log_list = []
    kwargs_data = {"assets": assets, "path": path, 'log_list':  log_list}
    if asset_id:
        asset = get_object_or_404(asset, pk=asset_id)
        kwargs_data['select_asset'] = asset
        xssh = controlssh(username=asset.username, host=asset.host, key_filename=asset.ssh_key_url())
        log_list += xssh.find_log_list(path)
    return render(request, 'asset/tailf.html', kwargs_data)


@accept_websocket
def tailf_websocket(request):
    if request.is_websocket():#判断是不是websocket连接
        path, log_name = request.get.get('path'), request.get.get('log_name')

        asset_id = request.get.get('asset_id')[0]
        asset = get_object_or_404(asset, pk=asset_id)
        xssh = controlssh(username=asset.username, host=asset.host, key_filename=asset.ssh_key_url())
        log_path = path+log_name if path[-1] == "/" else path+'/'+log_name
        xssh.send_tailf_log(log_path, request.websocket)