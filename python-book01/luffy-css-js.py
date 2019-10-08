import requests
import os
import time
import json
from lxml import etree
from urllib.parse import urljoin
from urllib.request import urlretrieve


BASE_URL = 'http://book.luffycity.com/python-book/'
BASE_PATH = os.getcwd()
print(BASE_PATH)

headers = {
    'cookie':'Hm_lvt_9cae5942a3c39f3b6fcf0a32b00277e2=1561510290; Hm_lpvt_9cae5942a3c39f3b6fcf0a32b00277e2=1561510564',
    'Authorization':'Basic bHVmZnktcHl0aG9uOmx1ZmZ5LWJvb2s=',
    'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
}


def page_content_get(url):
    """

    :param url:
    :return:
    """
    resp = requests.get(url, headers=headers)
    content = resp.content.decode('utf8')

    return content



def page_list_get(url):
    """

    :param url:
    :return:
    """
    resp = requests.get(url, headers=headers)
    print(resp.status_code)
    # print(resp.content.decode('utf8'))
    content = resp.content.decode('utf8')
    html = etree.HTML(content)
    print(html)
    # html = etree.tostring(html).decode('utf8')
    # print(html)
    href_list = list(html.xpath('//script/@src'))[:]
    for h in href_list:
        if 'http' in h:
            continue
        # print(h)
        h_new = urljoin(BASE_URL, h)
        # print(h)
        if h_new.endswith('.js'):
            # print(h_new, h)
            h_path = h.replace('/', '\\')
            # print(h_path)
            h_path_list = h_path.split('\\')
            h_path_list.pop()
            # print(h_path_list)
            html_full_path = os.path.join(BASE_PATH, h_path)
            # with open(html_full_path, 'w') as f:
            #     f.write('python')
            # print(html_full_path)

            if h_path_list:
                # for h_per in h_path_list:
                #     h_full = u
                dir_path = os.path.join(BASE_PATH, '\\'.join(h_path_list))
                # print(dir_path)
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)
                pass

            style_scr = urljoin(BASE_URL, h_new)
            print(style_scr)
            content = page_content_get(style_scr)
            with open(html_full_path, 'w', encoding='utf8') as f:
                f.write(content)

            print(html_full_path)


if __name__ == '__main__':
    """
    """
    page_list_get('http://book.luffycity.com/python-book/')