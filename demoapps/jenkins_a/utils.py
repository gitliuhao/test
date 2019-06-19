import datetime

import jenkins as jenkins
import requests
from django.conf import settings
from django.http import Http404


def stamp_to_datetime(stamp, unit='s', format=None):
    if unit=="ms":
        stamp = int(stamp) / 1000
    d = datetime.datetime.fromtimestamp(stamp)
    if format:
        return d.strftime(format)
    return d


class JenkinsServer(jenkins.Jenkins):
    def __init__(self, url=None, username=None, password=None, timeout=None):
        if not url or not username or not password:
            jconf = settings.JENKINSCONF
            url, username, password = jconf['url'], jconf['username'], jconf['password']
        super().__init__(url, username=username, password=password)

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
