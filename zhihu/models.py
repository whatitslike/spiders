import json
import datetime
import threading

from elasticsearch import Elasticsearch

from . import logger
from .agent import do_request
from q import zhihu_c, zhihu_qname


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
        es.index(index='zhihu', doc_type=type, id=data['id'], body=data)

    @classmethod
    def _do_job(cls):
        zhihu_c.basic_consume(cls.save, zhihu_qname, no_ack=True)
        zhihu_c.start_consuming()

    @classmethod
    def start(cls):
        t = threading.Thread(target=cls._do_job)
        t.daemon = True
        t.start()

