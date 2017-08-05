import json
import time
import random
import threading
import traceback

import pika

from q import get_ch, zhihu_qname
from . import logger
from .agent import do_request
from .types import Types


class BaseSource:

    def __init__(self):
        self._logger = logger
        self._start_urls = []
        self._zhihu_ch = get_ch(zhihu_qname)

    def _parse_answer_url(self, q_url):
        schema = 'https://api.zhihu.com/questions/%s/answers'
        qid = q_url.split('/')[-1]
        return schema % qid

    @property
    def _start_url(self):
        return random.choice(self._start_urls)

    def get_answer_url_by_question_url(self, url):
        answers_url = self._parse_answer_url(url)
        answer_json_objs = do_request(answers_url)
        count = 100
        while not answer_json_objs['paging']['is_end'] and count < 50:
            for obj in answer_json_objs['data']:
                self.answer_queue.put(obj['url'])
                self.publish(obj['url'], Types.ANSWER)
                count -= 1

            url = answer_json_objs['paging']['next']
            answer_json_objs = do_request(url)

    def publish(self, url, type, site='zhihu'):
        self._zhihu_ch.basic_publish(
            exchange='',
            routing_key=site,
            body=json.dumps({'url': url, 'type': type}),
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            )
        )
        self._logger.info('published %s %s' % (url, type))

    def _parse(self, json_objs):
        raise NotImplementedError

    def _start(self, url, direction):
        while True:
            try:
                json_objs = do_request(url)
                if json_objs['paging']['is_end']:
                    self._logger.info('end reached, sleep for 10 mins!')
                    time.sleep(600)

                    url = self._start_url
                    json_objs = do_request(url)
                    continue

                self._parse(json_objs)

                url = json_objs['paging'][direction]

            except:
                exstr = traceback.format_exc()
                self._logger.error(exstr)
                continue

            finally:
                time.sleep(10)

    def start(self):
        for start_url in self._start_urls:
            t = threading.Thread(target=self._start, args=(start_url, 'next'))
            t.setDaemon(True)
            t.start()
