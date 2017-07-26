from .base import BaseSource
from .types import Types


class People(BaseSource):

    def __init__(self):
        super(People, self).__init__()

        self._start_urls = [
            'https://api.zhihu.com/search_v3?correction=1&excerpt_len=70&q=%E5%84%BF%E7%A7%91%E5%8C%BB%E7%94%9F&t=people'
        ]

    def _parse(self, json_objs):
        for obj in json_objs['data']:
            t = obj.get('type')
            if t != 'search_result':
                continue

            t = obj['object']
            if t['type'] != 'people':
                continue

            self.publish(t['url'], Types.PEOPLE)
