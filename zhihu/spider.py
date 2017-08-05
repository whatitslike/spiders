from zhihu import (
    explore_feeds,
    topstories,
    columns,
    hot,
    roundtables,
    topics,
    people,
)


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

    def do_crawl(self):
        for source in self.sources:
            source.start()
