import datetime
import os
import sys

import jenkins as jenkins
import requests
from django.conf import settings
from django.http import Http404
from encoder import XML2Dict


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
    def __init__(self, url=None, username=None, password=None, timeout=None, jobs_path=None):
        self._xml2d = None
        self.jobs_path = jobs_path
        if not self.jobs_path:
            self.jobs_path = "/root/.jenkins/jobs/"
        if not url or not username or not password:
            jconf = settings.JENKINSCONF
            url, username, password = jconf['url'], jconf['username'], jconf['password']
        super().__init__(url, username=username, password=password)

    def XML2Dict(self):
        if not self._xml2d:
            self._xml2d = XML2Dict()
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
            name = build['name']
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
        try:
            with open(file_path, 'r') as f:
                b = f.read()
                the_dict = xml.parse(b)
                return the_dict
        except FileNotFoundError:
            pass

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

    def get_all_build_iter(self):
        ''' 返回生成器 每个值为构建历史 '''
        job_name_list = os.listdir(self.jobs_path)
        for job_name in job_name_list:
            job_builds_path = os.path.join(os.path.join(self.jobs_path, job_name), 'builds')
            try:
                build_number_list = os.listdir(job_builds_path)
            except FileNotFoundError:
                continue
            for build_number in build_number_list:
                try:
                    build_number = int(build_number)
                except ValueError:
                    continue
                build = self.get_job_build_info(job_name, build_number)
                if build:
                    build['last_successful'] = self.last_successful_build(job_name)
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