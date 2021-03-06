import json

from django.http import JsonResponse
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from dwebsocket import accept_websocket

from asset.forms import AssetForm
from asset.models import Asset
from asset.ssh_client import ControlSsh

# Create your views here.
# from sset import traverse, system_path_search
from asset.utils import system_path_search, traverse


class AssetListView(ListView):
    model = Asset


def asset(request):
    return render(request, 'demoapps/asset/asset_list.html')


class AssetCreateView(CreateView):
    form_class = AssetForm
    template_name = '../templates/demoapps/asset/asset_form.html'
    success_url = reverse_lazy('asset-url:asset-list')
    model = Asset

    def get_context_data(self, **kwargs):
        kwargs['title']='创建主机配置'
        return super().get_context_data(**kwargs)


class AssetUpdateView(UpdateView):
    pk_url_kwarg = 'id'
    form_class = AssetForm
    template_name = 'demoapps/asset/asset_form.html'
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
        try:
            xssh = ControlSsh(**asset.config_dict())
            log_list += xssh.find_log_list(path)
        except Exception as e:
            kwargs_data['errors'] = str(e)
    return render(request, 'demoapps/asset/tailf.html', kwargs_data)


def local_tailf(request):
    root_path = "/data/xls/runtime/"
    data = {'root_path': root_path}
    # 倒叙取值
    try:
        search_path_list = map(lambda x: x[-1][len(root_path):],
            sorted(traverse(root_path), key=lambda x: x[0], reverse=True))
        data['search_path_list'] = search_path_list
    except FileNotFoundError as e:
        data['errors'] = str(e)
    return render(request, 'demoapps/asset/local_tailf.html', data)


def local_file_list(request):
    local_path = request.GET.get('local_path')
    root_path = "/data/xls/runtime/"
    if len(local_path)<=len(root_path) or root_path!=local_path[:len(root_path)]:
        return HttpResponse({"errors": 'not permmission'}, status=403)
    local_path_list = system_path_search(local_path)
    return HttpResponse(json.dumps(local_path_list))


@accept_websocket
def tailf_socket(request):
    if request.is_websocket():#判断是不是websocket连接
        path, log_name = request.GET.get('path'), request.GET.get('log_name')
        asset_id = request.GET.get('asset_id')[0]
        asset = get_object_or_404(Asset, pk=asset_id)
        xssh = ControlSsh(**asset.config_dict())
        log_path = path+log_name if path[-1] == "/" else path+'/'+log_name
        xssh.send_tailf_log(log_path, request.websocket)


@accept_websocket
def local_tailf_socket(request):
    if request.is_websocket():#判断是不是websocket连接
        file_path = request.GET.get('file_path')
        asset = get_object_or_404(Asset, pk=request.GET.get('asset_id', 0) or 0)
        root_path = "/data/xls/runtime"
        if root_path not in file_path:
            request.websocket.send(json.dumps({'code': 400, 'message': '该路径不允许访问'}))
            return HttpResponse('')
        xssh = ControlSsh(**asset.config_dict())
        xssh.send_tailf_log(file_path, request.websocket)
    return HttpResponse('')