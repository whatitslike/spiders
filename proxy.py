import random

import requests
from bs4 import BeautifulSoup


class _Proxy:

    def __init__(self):
        self._counter = 0
        self.__proxies = []
        self._proxy_repo = [
            'http://www.kuaidaili.com/free/inha/1/',
            'http://www.kuaidaili.com/free/inha/2/',
            'http://www.kuaidaili.com/free/inha/3/',
            'http://www.kuaidaili.com/free/inha/4/',
            'http://www.kuaidaili.com/free/inha/5/',
            'http://www.kuaidaili.com/free/inha/6/',
            'http://www.kuaidaili.com/free/inha/7/',
            'http://www.kuaidaili.com/free/inha/8/',
            'http://www.kuaidaili.com/free/inha/9/',
            'http://www.kuaidaili.com/free/inha/10/',
        ]

    def _parse_content(self, soup_obj):
        trs = soup_obj.find_all('tr')
        for tr in trs:
            ip = tr.find_all(attrs={'data-title': 'IP'})
            port = tr.find_all(attrs={'data-title': 'PORT'})
            if ip and port:
                url = 'http://%s:%s' % (ip[0].text, port[0].text)
                self.__proxies.append(url)

    def _retrieve_proxy(self):
        for url in self._proxy_repo:
            try:
                r = requests.get(url)
                soup = BeautifulSoup(r.content, 'lxml')
                self._parse_content(soup)
            except Exception as e:
                print(e)

    def get(self):
        if not self.__proxies:
            self._retrieve_proxy()

        # reset proxies after 3600 times
        self._counter += 1
        if self._counter > 3600:
            self.__proxies = []

        return random.choice(self.__proxies)


proxy_pool = _Proxy()


if __name__ == '__main__':
    p = _Proxy()
    print(p.get())
