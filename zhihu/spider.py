import sys
import time


from zhihu import (
    explore_feeds,
    topstories,
    columns,
    hot,
    roundtables,
    topics,
    people,
)
from .models import ZhihuModel


class Spider:

    def __init__(self):
        self.sources = [
            explore_feeds.ExploreFeeds(),
            topstories.TopStory(),
            columns.Columns(),
            hot.Hot(),
            roundtables.RoundTables(),
            topics.Topics(),
            people.People(),
        ]
        self.consumers = [ZhihuModel, ]

    def do_crawl(self):
        for source in self.sources:
            source.start()

        for consumer in self.consumers:
            consumer.start()

