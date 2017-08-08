import json

import requests

from . import logger
from proxy import proxy_pool


_headers = {
    'User-Agent': 'osee2unifiedRelease/3.53.0 (iPhone; iOS 10.3.2; Scale/2.00)',
    'x-app-za': 'OS=iOS&Release=10.3.2&Model=iPhone5,2&VersionName=3.56.0&VersionCode=668&Width=640&Height=1136',
    'X-UUID': 'ADDCp6n3-wtLBf1ji8mZKMzrJRMw29chulc=',
    'X-API-Version': '3.0.62',
    'X-APP-VERSION': '3.56.0',
    'Authorization': 'Bearer gt2.0AAAAAAVS-HUL-_epp8IwAAAAAAtNVQJgAgDrwCAkhbZVGCqAKUzf2ACgctdj1A==',
    'X-APP-Build': 'release',
    'X-Network-Type': 'Wifi',
    'Cookie': 'aliyungf_tc=AQAAAG4kqxUUpQsAKBLCb2oeaMZzqj24;q_c1=5e06dd235e074f18b0e72ff26184a3c9|1498697374000|1498697374000;d_c0=ADDCp6n3-wtLBf1ji8mZKMzrJRMw29chulc=|1499497278;z_c0=gt2.0AAAAAAVS-HUL-_epp8IwAAAAAAtNVQJgAgDrwCAkhbZVGCqAKUzf2ACgctdj1A==;zap=72d596a9-0827-403e-b572-423f6682a0f0',
    'X-SUGER': 'SURGQT1BNjI5RTkwMi02RUFBLTQwODktOEQ2Ny02NTNGQTcwMTgxRjU=',
}


def do_request(url):
    logger.info(url)
    proxy = proxy_pool.get()
    r = requests.get(url, headers=_headers, proxies={'http': proxy})
    jsobj = json.loads(r.content)
    return jsobj
