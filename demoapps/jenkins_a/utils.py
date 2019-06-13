import datetime

import jenkins as jenkins
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