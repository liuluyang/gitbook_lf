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

def img_download(html_url, img_url, img_name):
    """

    :param html_url:
    :param img_url:
    :param img_name:
    :return:
    """
    url = urljoin(html_url, img_url)
    # urlretrieve(urljoin(html_url, img_url), './assets/{}'.format(img_name))
    data_img = requests.get(url, headers=headers)
    with open('./assets/{}'.format(img_name), 'wb') as f:
        f.write(data_img.content)


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
    href_list = list(html.xpath('//a/@href'))[:]
    for h in href_list:
        # print(h)
        h_new = urljoin(BASE_URL, h)
        # print(h)
        if h_new.endswith('.html'):
            print(h_new, h)
            h_path = h.replace('/', '\\')
            print(h_path)
            h_path_list = h_path.split('\\')
            h_path_list.pop()
            print(h_path_list)
            html_full_path = os.path.join(BASE_PATH, h_path)
            # with open(html_full_path, 'w') as f:
            #     f.write('python')
            # print(html_full_path)

            if h_path_list:
                # for h_per in h_path_list:
                #     h_full = u
                dir_path = os.path.join(BASE_PATH, '\\'.join(h_path_list))
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)
                pass

            content = page_content_get(h_new)

            html = etree.HTML(content)
            src_list = html.xpath('//img/@src')
            for src in src_list:
                img_name = src.split('/')[-1]

                # img_name = img_name.replace('%', '')
                # img_name = '../assets/{}'.format(img_name)
                # content.replace(src, img_name)
                print(h_new, src, img_name)
                img_download(h_new, src, img_name)

            print(content)
            content = content.replace('%', '%25')
            with open(html_full_path, 'w', encoding='utf8') as f:
                f.write(content)
            time.sleep(1)


    # with open('content.html', 'w', encoding='utf8') as f:
    #     f.write(content)

# from urllib.parse import urljoin
#
# u1 = 'http://book.luffycity.com/python-book/di-2-zhang-python-ji-chu-2/25-ji-ben-shu-ju-lei-xing-2014-2014-zi-fu-chuan.html'
# u2 = '../assets/变量存储.png'
# u3 = 'https://book.apeland.cn/media/images/2019/03/03/image.png'
# print(urljoin(u1, u2))

from lxml import etree
html = etree.parse('./content.html', etree.HTMLParser())
# result = html.xpath('//img/@src')
# print(result)

# href_list = html.xpath('//a/@href')
# # for h in href_list:
# #     print(h)


if __name__ == '__main__':
    """
    """
    page_list_get('http://book.luffycity.com/python-book/')
