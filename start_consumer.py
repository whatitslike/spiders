import time

from zhihu.models import ZhihuModel


if __name__ == '__main__':
    ZhihuModel.start()
    while True:
        time.sleep(60)
