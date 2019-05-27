import json
from urllib import parse

from channels.generic.websocket import WebsocketConsumer
# from tailf.tasks import tailf
import _thread

from django.conf import settings

from tailf.task import tailfLog, ControlSsh


class TailfConsumer(WebsocketConsumer):
    def connect(self):
        self.file_id = self.scope["url_route"]["kwargs"]
        url_query = self.scope['query_string']
        # self.result = tailf.delay(self.file_id, self.channel_name)
        # tailfLog(self.channel_name, self.channel_name)
        # print('connect:', self.channel_name, self.result.id)

        # 获取参数
        # 解码
        # 转换成dict
        url_query = self.scope['query_string']
        result = parse.unquote(url_query.decode())
        query_dict = parse.parse_qs(result)
        path, log_name = query_dict.get('path')[0], query_dict.get('log_name')[0]
        host = query_dict.get('server_ip')[0]
        host_conf = settings.SERVER_DICT[host]
        xssh = ControlSsh(host=host, **host_conf)
        log_path = path+log_name if path[-1] == "/" else path+'/'+log_name
        self.accept()
        _thread.start_new_thread(xssh.send_tailf_log, (log_path, self,))
        # self.send(text_data=json.dumps(data))

    def disconnect(self, close_code):
        # 中止执行中的Task
        # self.result.revoke(terminate=True)
        print('disconnect:', self.file_id, self.channel_name)

    def send_message(self, event):
        self.send(text_data=json.dumps({
            "message": event["message"]
        }))