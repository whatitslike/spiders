import sys
import time

from zhihu.spider import Spider as ZhihuSpider


if __name__ == '__main__':
    start = time.time()
    s = ZhihuSpider()
    s.do_crawl()
    try:
        while True:
            if time.time() - start > 60 * 60 * 2:
                sys.exit()

            time.sleep(2**10)  # actually sleep forever
    except KeyboardInterrupt:
        print('i am gone, Bye!')

