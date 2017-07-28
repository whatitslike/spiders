import random

import requests
from bs4 import BeautifulSoup


class _Proxy:

    def __init__(self):
        self._counter = 0
        self.__proxies = []
        self._kuaidaili_proxy_repo = [
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
        self._xici_proxy_repo = [
            'http://www.xicidaili.com/wt/',
            'http://www.xicidaili.com/wt/2',
            'http://www.xicidaili.com/wt/3',
            'http://www.xicidaili.com/wt/4',
            'http://www.xicidaili.com/wt/5',
            'http://www.xicidaili.com/wt/6',
        ]

    def _parse_kuaidaili_content(self, soup_obj):
        trs = soup_obj.find_all('tr')
        for tr in trs:
            ip = tr.find_all(attrs={'data-title': 'IP'})
            port = tr.find_all(attrs={'data-title': 'PORT'})
            if ip and port:
                url = 'http://%s:%s' % (ip[0].text, port[0].text)
                self.__proxies.append(url)

    def _parse_xici_content(self, soup_obj):
        trs = soup_obj.find_all('tr')
        for tr in trs[1:]:
            tds = tr.find_all('td')
            ip = tds[1].text
            port = tds[2].text
            if ip and port:
                url = 'http://%s:%s' % (ip, port)
                self.__proxies.append(url)

    def _retrieve_proxy(self):
        for url in self._kuaidaili_proxy_repo:
            try:
                r = requests.get(url, timeout=2)
                soup = BeautifulSoup(r.content, 'lxml')
                self._parse_kuaidaili_content(soup)
            except Exception as e:
                print(e)

        for url in self._xici_proxy_repo:
            try:
                r = requests.get(
                    url,
                    timeout=3,
                    headers={
                        'User-Agent': (
                            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
                            ' (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'
                        )
                    }
                )
                soup = BeautifulSoup(r.content, 'lxml')
                self._parse_xici_content(soup)
            except Exception as e:
                print(e)

    def get(self):
        if not self.__proxies:
            self._retrieve_proxy()

        return random.choice(self.__proxies)


proxy_pool = _Proxy()


if __name__ == '__main__':
    p = _Proxy()
    print(p.get())
