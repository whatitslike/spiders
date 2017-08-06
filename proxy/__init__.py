import os
import random
import datetime

import requests
from bs4 import BeautifulSoup


class _Proxy:

    def _load_proxy(self):
        f = os.path.join(self._cur, 'proxy.txt')
        with open(f) as _f:
            lines = _f.readlines()
            for line in lines:
                line = line.strip()
                self.__proxies.append(line)

    def _load_updated(self):
        f = os.path.join(self._cur, 'updated')
        with open(f, 'r') as _f:
            c = _f.read()
            c = c.strip()
            return datetime.datetime.strptime(c, '%Y-%m-%d')

    def _update_updated(self):
        now = datetime.datetime.now()
        f = os.path.join(self._cur, 'updated')
        with open(f, 'w') as _f:
            _f.write(now.strftime('%Y-%m-%d'))

    def _save_to_file(self):
        if not self.__proxies:
            return

        f = os.path.join(self._cur, 'proxy.txt')
        with open(f, 'w') as _f:
            for p in self.__proxies:
                _f.write(p + '\n')

            self._update_updated()

    def __init__(self):
        self.__proxies = []

        self._cur = os.path.dirname(os.path.realpath(__file__))

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

        # always load proxy from file
        self._load_proxy()

        # check updated old than 1day
        date = self._load_updated()
        now = datetime.datetime.now()
        if (now - date).days > 1:
            self._retrieve_proxy()
            self._save_to_file()

    def _parse_kuaidaili_content(self, soup_obj):
        trs = soup_obj.find_all('tr')
        for tr in trs:
            ip = tr.find_all(attrs={'data-title': 'IP'})
            port = tr.find_all(attrs={'data-title': 'PORT'})
            if ip and port:
                url = 'http://%s:%s' % (ip[0].text, port[0].text)
                self.__proxies.append(url)
                print(url)

    def _parse_xici_content(self, soup_obj):
        trs = soup_obj.find_all('tr')
        for tr in trs[1:]:
            tds = tr.find_all('td')
            ip = tds[1].text
            port = tds[2].text
            if ip and port:
                url = 'http://%s:%s' % (ip, port)
                self.__proxies.append(url)
                print(url)

    def _retrieve_proxy(self):
        for url in self._kuaidaili_proxy_repo:
            try:
                r = requests.get(
                    url,
                    headers={
                        'User-Agent': (
                            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
                            ' (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'
                        )
                    },
                    proxies=[self.get(),],
                    timeout=2,
                )
                soup = BeautifulSoup(r.content, 'lxml')
                self._parse_kuaidaili_content(soup)
            except Exception as e:
                print(e)

        for url in self._xici_proxy_repo:
            try:
                r = requests.get(
                    url,
                    headers={
                        'User-Agent': (
                            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
                            ' (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'
                        )
                    },
                    proxies=[self.get(),],
                    timeout=3,
                )
                soup = BeautifulSoup(r.content, 'lxml')
                self._parse_xici_content(soup)
            except Exception as e:
                print(e)

    def get(self):
        return random.choice(self.__proxies)


proxy_pool = _Proxy()


if __name__ == '__main__':
    p = _Proxy()
    print(p.get())
