from .base import BaseSource
from .types import Types


class Topics(BaseSource):

    def __init__(self):
        super(Topics, self).__init__()

        self._start_urls = [
            'https://api.zhihu.com/topics/19660752/best_answerers?excerpt_len=75',
            'https://api.zhihu.com/topics/19578699/best_answers?excerpt_len=75',
            'https://api.zhihu.com/topics/19554405/best_answers?excerpt_len=75',
            'https://api.zhihu.com/topics/19551506/best_answers?excerpt_len=75',
            'https://api.zhihu.com/topics/19553176/best_answers?excerpt_len=75',
        ]

    def _parse(self, json_objs):
        for obj in json_objs['data']:
            t = obj.get('type')
            if t != 'answer':
                continue

            url = obj['question']['url']
            self.publish(url, Types.QUESTION)
