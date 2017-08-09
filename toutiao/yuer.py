import re
import time
import html
import datetime
import traceback
import threading

import requests
from elasticsearch import Elasticsearch

from utils import get_logger
from proxy import proxy_pool


class Spider:

    def __init__(self):
        self._start_urls = [
            'https://www.toutiao.com/api/pc/feed/?category=news_baby',
            'https://www.toutiao.com/api/pc/feed/?category=news_health',
            'https://www.toutiao.com/api/pc/feed/?category=news_edu',
        ]
        self.logger = get_logger('toutiao')
        self.es = Elasticsearch()

    def _do_request(self, url):
        self.logger.info('get %s' % url)
        proxy = proxy_pool.get()
        try:
            r = requests.get(
                url,
                # proxies={'http': proxy, 'https': proxy},
                headers={
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
                },
                timeout=2
            )
            return r
        except Exception as e:
            print(e)
            traceback.print_exc()

    def _get_content(self, group_id):
        url = 'https://www.toutiao.com' + group_id
        r = self._do_request(url)
        if not r:
            return ''

        result = r.content
        content = result.decode('utf8')

        r = re.search(r'content: (.*?)groupId: ', content, re.DOTALL)
        if not r:
            return ''

        c = r.groups(1)[0].strip()
        c = html.unescape(c)
        return c[:-26]

    def _start(self, url):
        _start_url = url
        while True:
            self.logger.info('get %s' % url)
            r = self._do_request(url)
            if not r:
                continue

            obj = r.json()

            for d in obj['data']:
                data = d

                content = self._get_content(d['source_url'])
                self.logger.info(content)
                data.update({'content': content})

                now = datetime.datetime.now()
                now_str = now.strftime("%Y-%m-%d %H:%M:%S")
                data.update({'_added_at': now_str})

                self.es.index(index='toutiao', doc_type='feed', body=data, id=data['group_id'])

            url = _start_url + '&max_behot_time=' + str(obj['next']['max_behot_time'])

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
