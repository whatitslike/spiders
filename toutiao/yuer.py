import time
import datetime
import threading

import requests
from elasticsearch import Elasticsearch

from proxy import proxy_pool
from utils import get_logger


class Spider:

    def __init__(self):
        self._start_urls = [
            'https://www.toutiao.com/api/pc/feed/?category=news_baby',
        ]
        self.logger = get_logger('toutiao')
        self.es = Elasticsearch()

    def _do_request(self, url):
        proxy = proxy_pool.get()
        r = requests.get(
            url,
            proxies=[proxy, ]
        )
        obj = r.json()
        return obj

    def _start(self, start_url):
        obj = self._do_request(start_url)
        while obj:
            for d in obj['data']:
                data = d
                now = datetime.datetime.now()
                now_str = now.strftime("%Y-%m-%d %H:%M:%S")
                data.update({'_added_at': now_str})
                self.es.index(index='toutiao', doc_type='feed', body=data)

            url = start_url + '&max_behot_time=' + str(obj['next']['max_behot_time'])
            obj = self._do_request(url)

    def start(self):
        for start_url in self._start_urls:
            t = threading.Thread(target=self._start, args=(start_url,))
            t.setDaemon(True)
            t.start()


if __name__ == '__main__':
    s = Spider()
    s.start()
    while True:
        time.sleep(60)
