import re
import time
import html
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
        return r

    def _get_content(self, group_id):
        url = 'https://www.toutiao.com' + group_id
        r = self._do_request(url)
        result = r.content
        content = result.decode('utf8')

        r = re.search(r'content: (.*?)groupId: ', content, re.DOTALL)
        if not r:
            return ''

        c = r.groups(1)[0].strip()
        c = html.unescape(c)
        return c[:-26]

    def _start(self, start_url):
        r = self._do_request(start_url)
        obj = r.json()
        while obj:
            for d in obj['data']:
                data = d

                content = self._get_content(d['source_url'])
                self.logger.info(content)
                data.update({'content': content})

                now = datetime.datetime.now()
                now_str = now.strftime("%Y-%m-%d %H:%M:%S")
                data.update({'_added_at': now_str})

                self.es.index(index='toutiao', doc_type='feed', body=data)

            url = start_url + '&max_behot_time=' + str(obj['next']['max_behot_time'])
            r = self._do_request(url)
            obj = r.json()

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