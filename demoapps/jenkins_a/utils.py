import datetime
import os
from urllib import parse

import jenkins as jenkins
import requests
import xmltodict
from django.http import Http404

from asset.ssh_client import ControlSsh


def stamp_to_datetime(stamp, unit='s', format=None):
    if unit=="ms":
        stamp = int(stamp) / 1000
    d = datetime.datetime.fromtimestamp(stamp)
    if format:
        return d.strftime(format)
    return d


def bytes_dict_decode(bytes_dict):
    if isinstance(bytes_dict, dict):
        for key in bytes_dict.keys():
            v = bytes_dict[key]
            bytes_dict[key] = bytes_dict_decode(v)
    elif isinstance(bytes_dict, list):
        for v in bytes_dict:
            bytes_dict_decode(v)
    elif isinstance(bytes_dict, bytes):
        bytes_dict = bytes_dict.decode()
    return bytes_dict


class JenkinsServer(jenkins.Jenkins):
    def __init__(self, url=None, username=None, password=None, timeout=None, config_path=None, asset=None):
        self._xml2d = None
        self.asset = asset
        self.jobs_path = os.path.join(config_path, 'jobs')
        self.config_path = config_path
        self._ssh_client = None
        super().__init__(url, username=username, password=password)

    @property
    def ssh_client(self):
        if not self._ssh_client:
            self._ssh_client = ControlSsh(**self.asset).ssh_client
        return self._ssh_client

    def XML2Dict(self):
        if not self._xml2d:
            self._xml2d = xmltodict
        return self._xml2d

    def get_all_job_details(self):
        jobs_data_list = []
        try:
            jobs = self.get_jobs()
        except IOError:
            raise Http404("can't not connect jenkins server")

        for job in jobs:
            job_name = job['name']
            info = self.get_job_info(name=job_name)
            job_data = {'name': job_name}
            lastBuild = info.get('lastBuild')
            if lastBuild:
                number = lastBuild['number']
                build_info = self.get_build_info(name=job_name, number=number)
                lastBuild['datetime'] = stamp_to_datetime(build_info['timestamp'], unit='ms', format="%Y-%m-%d %H:%M")
                job_data['lastBuild'] = lastBuild
            lastSuccessfulBuild = info.get('lastSuccessfulBuild')
            if lastSuccessfulBuild:
                number = lastSuccessfulBuild['number']
                build_info = self.get_build_info(name=job_name, number=number)
                lastSuccessfulBuild['datetime'] = stamp_to_datetime(build_info['timestamp'], unit='ms',
                                                                    format="%Y-%m-%d %H:%M")
                job_data['lastSuccessfulBuild'] = lastSuccessfulBuild
            lastFailedBuild = info.get('lastFailedBuild')
            if lastFailedBuild:
                number = lastFailedBuild['number']
                build_info = self.get_build_info(name=job_name, number=number)
                lastFailedBuild['datetime'] = stamp_to_datetime(build_info['timestamp'], unit='ms',
                                                                format="%Y-%m-%d %H:%M")
                job_data['lastFailedBuild'] = lastFailedBuild
            jobs_data_list.append(job_data)

        return jobs_data_list

    def get_job_building_list(self):
        builds = self.get_running_builds()
        for build in builds:
            name = parse.unquote(build['name'])
            build['name'] = name
            build_info = self.get_build_info(name, build['number'])
            build_info['time'] = stamp_to_datetime(build_info['timestamp'], unit='ms', format="%Y-%m-%d %H:%M")
            build['detail'] = build_info
        return builds

    def get_job_build_faild_list(self):
        jobs = self.get_jobs()
        build_list = []
        for job in jobs:
            name = job['name']
            job_info = self.get_job_info(name)
            builds = job_info.get('builds', [])
            for build in builds:
                build_info = self.get_build_info(name, build['number'])
                if build_info['result'] == 'FAILURE':
                    build_info['time'] = stamp_to_datetime(build_info['timestamp'], unit='ms', format="%Y-%m-%d %H:%M")
                    build['detail'] = build_info
                    build['name'] = name
                    build_list.append(build)
        return build_list

    def delete_job_build(self, name, number):
        folder_url, short_name = self._get_job_folder(name)
        url = self._build_url(jenkins.DELETE_BUILD, locals())
        req = requests.Request('POST', url)
        return self.jenkins_request(req)

    def get_file_path_xml2d(self, file_path):
        xml = self.XML2Dict()
        _, out, _ = self.ssh_client.exec_command("cat %s" % file_path)
        xml_str = out.read()
        if xml_str:
            the_dict = xml.parse(xml_str)
            return the_dict

    def listdir(self, path):
        # job_name_list = [job_name.encode('utf-8', errors='surrogateescape').decode('utf-8') for job_name in
        #                  job_name_list]
        _, out, _ = self.ssh_client.exec_command("ls %s" % path)
        path_list = [x for x in out.read().decode().split('\n') if x]
        return path_list

    def get_job_name_list(self):
        jobs_path = self.jobs_path
        return self.listdir(jobs_path)

    def get_view_job_name_list(self):
        config_xml_path = os.path.join(self.config_path, 'config.xml')
        d = self.get_file_path_xml2d(config_xml_path)
        listView = d['hudson']['views']['listView']
        listView = d['hudson']['views']['listView']
        return d

    def get_job_build_info(self, name, number, field_names=None):
        if field_names is None:
            field_names = ['queueId', 'timestamp', 'startTime', 'result']
        builds_path = os.path.join(os.path.join(self.jobs_path, name), "builds")
        build_path = os.path.join(builds_path, str(number))
        build_xml_path = os.path.join(build_path, 'build.xml')
        build_data = {'name': name, 'number': number}
        the_dict = self.get_file_path_xml2d(build_xml_path)
        if not the_dict:
            return None
        build = the_dict.get('build') or the_dict.get('flow-build')
        for name in field_names:
            build_data[name] = build[name].decode()
        build_data['time'] = stamp_to_datetime(build['timestamp'], unit='ms', format="%Y-%m-%d %H:%M")
        return build_data

    def get_all_build_iter(self, name=None):
        ''' 返回生成器 每个值为构建历史
            @name: 任务名称
        '''
        if name:
            for build in self.get_job_builds_iter(name):
                yield build
        else:
            job_name_list = self.get_job_name_list()
            for job_name in job_name_list:
                for build in self.get_job_builds_iter(job_name):
                    yield build

    def get_job_builds_iter(self, name):
        ''' 查看一个任务的所有构建记录。返回迭代器'''
        job_builds_path = os.path.join(os.path.join(self.jobs_path, name), 'builds')
        try:
            build_number_list = self.listdir(job_builds_path)
        except FileNotFoundError:
            build_number_list = []
        for build_number in build_number_list:
            try:
                build_number = int(build_number)
            except ValueError:
                continue
            build = self.get_job_build_info(name, build_number)
            if build:
                build['last_successful'] = self.last_successful_build(name)
                yield build

    def last_successful_build(self, name):
        ''' 获取任务上次成功的构建信息 '''
        successful_path = os.path.join(os.path.join(self.jobs_path, name), 'lastSuccessful')
        build_successful_path = os.path.join(successful_path, 'build.xml')
        the_dict = self.get_file_path_xml2d(build_successful_path)
        if the_dict:
            the_dict = bytes_dict_decode(the_dict)
            build = the_dict.get('build') or the_dict.get('flow-build')
            build['time'] = stamp_to_datetime(build['timestamp'], unit='ms', format="%Y-%m-%d %H:%M")
            return build

    def get_job_config_dict(self, name):
        xml = self.XML2Dict()
        job_config_path = "{jobs_path}{name}/config.xml".format(jobs_path=self.jobs_path, name=name)
        with open(job_config_path, 'r') as f:
            b = f.read()
            the_dict = xml.parse(b)
            return the_dict