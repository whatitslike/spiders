from .base import BaseSource
from .types import Types


class ExploreFeeds(BaseSource):

    def __init__(self):
        super(ExploreFeeds, self).__init__()

        self._start_urls = [
            'https://api.zhihu.com/explore/feeds?limit=20&offset=20',
        ]

    def _parse(self, json_objs):
        for obj in json_objs['data']:
            t = obj.get('type')
            if t != 'explore_feed':
                continue

            t = obj.get('target', {}).get('type')
            if t == 'answer':
                url = obj['target']['url']
                self.publish(url, Types.ANSWER)

                url = obj['target']['question']['url']
                self.publish(url, Types.QUESTION)
                self.get_answer_url_by_question_url(url)

            elif t == 'article':
                url = obj['target']['url']
                self.publish(url, Types.ARTICLE)

