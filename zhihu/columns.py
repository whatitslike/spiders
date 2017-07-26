from .base import BaseSource
from .agent import do_request
from .types import Types


class Columns(BaseSource):

    def __init__(self):
        super(Columns, self).__init__()

        self._start_urls = [
            'https://api.zhihu.com/columns?classify=1&excerpt_len=75'
            'https://api.zhihu.com/columns?classify=2&excerpt_len=75'
            'https://api.zhihu.com/columns?classify=4&excerpt_len=75'
            'https://api.zhihu.com/columns?classify=3&excerpt_len=75'
            'https://api.zhihu.com/columns?classify=5&excerpt_len=75'
            'https://api.zhihu.com/columns?classify=6&excerpt_len=75'
            'https://api.zhihu.com/columns?classify=7&excerpt_len=75'
            'https://api.zhihu.com/columns?classify=8&excerpt_len=75'
            'https://api.zhihu.com/columns?classify=9&excerpt_len=75'
            'https://api.zhihu.com/columns?classify=12&excerpt_len=75'
            'https://api.zhihu.com/columns?classify=13&excerpt_len=75'
            'https://api.zhihu.com/columns?classify=16&excerpt_len=75',
        ]

    def _get_article_urls(self, column_url):
        return column_url + '/articles?limit=20&offset=10'

    def _parse(self, json_objs):
        urls = []
        while not json_objs['paging']['is_end']:
            for obj in json_objs['data']:
                if obj['type'] == 'column':
                    urls.append(obj['url'])

            url = json_objs['paging']['next']
            json_objs = do_request(url)

        article_urls = []
        for url in urls:
            url = self._get_article_urls(url)
            article_urls.append(url)

        for article_url in article_urls:
            json_objs = do_request(article_url)
            for obj in json_objs['data']:
                if obj['type'] != 'article':
                    continue

                self.publish(obj['url'], Types.ARTICLE)

