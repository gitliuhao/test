import json
import os

from django.http import JsonResponse
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from dwebsocket import accept_websocket

from asset.forms import AssetForm
from asset.models import Asset
from asset.task import ControlSsh

# Create your views here.


def system_path_search(curpath):
    find_t, curpath_list='', []
    # 判断路径是否包含'/'
    # 尾部名称find_t默认为''
    if curpath[-1]!='/':
        #包含则去掉尾数路径名称并赋值
        *curpath_list, find_t = curpath.split('/')
        # 重新分配路径
        curpath = '/'.join(curpath_list) + '/'
    try:
        d_list = os.listdir(curpath)
        search_list = [curpath+ t for t in d_list if find_t in t]
        return search_list
    except FileNotFoundError:
        return []


class AssetListView(ListView):
    model = Asset


def asset(request):
    return render(request, 'asset/asset_list.html')


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
        try:
            xssh = ControlSsh(username=asset.username, host=asset.host, key_filename=asset.ssh_key_url())
            log_list += xssh.find_log_list(path)
        except Exception as e:
            kwargs_data['errors'] = str(e)
    return render(request, '../templates/asset/tailf.html', kwargs_data)


def local_tailf(request):
    return render(request, 'asset/local_tailf.html', {'root_path': '/data/xls/runtime/'})


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
        xssh = ControlSsh(username=asset.username, host=asset.host, key_filename=asset.ssh_key_url())
        log_path = path+log_name if path[-1] == "/" else path+'/'+log_name
        xssh.send_tailf_log(log_path, request.websocket)


@accept_websocket
def local_tailf_socket(request):

    if request.is_websocket():#判断是不是websocket连接
        log_path = request.GET.get('log_path')
        root_path = "/data/xls/runtime"
        if len(log_path) <= len(root_path) or root_path != log_path[:len(root_path)]:
            HttpResponse({"errors": 'not permmission'}, status=403)
        xssh = ControlSsh()
        xssh.send_tailf_log(log_path, request.websocket)
    return HttpResponse('')