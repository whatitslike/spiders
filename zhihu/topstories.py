from .base import BaseSource
from .types import Types


class TopStory(BaseSource):

    def __init__(self):
        super(TopStory, self).__init__()

        self._start_urls = [
            'https://api.zhihu.com/topstory?action=pull&before_id=9&limit=10&action_feed=True&session_token=443067487ef8beca7e6eda932e25725d',
            'https://api.zhihu.com/topstory?action=pull&before_id=109&limit=10&action_feed=True&session_token=443067487ef8beca7e6eda932e25725d',
        ]

    def _parse(self, json_objs):
        for obj in json_objs['data']:
            t = obj.get('type')
            if t != 'feed':
                continue

            t = obj.get('target')
            if not t:
                continue

            a = t.get('type')
            if a != 'answer':
                continue

            self.publish(t['url'], Types.ANSWER)
            self.publish(t['question']['url'], Types.QUESTION)
            self.get_answer_url_by_question_url(t['question']['url'])
