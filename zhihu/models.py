import json
import datetime
import threading

import pika
from elasticsearch import Elasticsearch

from . import logger
from .types import Types
from .agent import do_request
from q import get_ch, zhihu_qname


es = Elasticsearch()


class ZhihuModel:

    @staticmethod
    def save(ch, method, properties, body):
        logger.info('get from queue %s' % body)

        body = json.loads(body)

        type = body['type']
        url = body['url']
        data = do_request(url)

        if data['type'] != type:
            return

        if 'status' in data:
            del data['status']

        now = datetime.datetime.now()
        now_str = now.strftime("%Y-%m-%d %H:%M:%S")
        data.update({'_added_at': now_str})
        if type == Types.PEOPLE:
            i = data['id']
            data['pid'] = i
            del data['id']
            result = es.index(index='zhihu', doc_type=type, body=data)
        else:
            result = es.index(index='zhihu', doc_type=type, id=data['id'], body=data)

        logger.info('save result ', result)

    @classmethod
    def _do_job(cls):
        while True:
            try:
                ch = get_ch(zhihu_qname)
                ch.basic_consume(cls.save, zhihu_qname, no_ack=True)
                ch.start_consuming()
            except pika.exceptions.ConnectionClosed:
                print('reconnect required!')

    @classmethod
    def start(cls):
        for _ in range(4):
            t = threading.Thread(target=cls._do_job)
            t.daemon = True
            t.start()

