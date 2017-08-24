# reference for http://karaage.hatenadiary.jp/entry/2017/08/23/073000
# coding: utf-8

import os
import sys
import traceback
from mimetypes import guess_extension
from time import time, sleep
from urllib.request import urlopen, Request
from urllib.parse import quote
from bs4 import BeautifulSoup

class Fetcher:
    def __init__(self, ua=''):
        self.ua = ua

    def fetch(self, url):
        req = Request(url, headers={'User-Agent': self.ua})
        try:
            with urlopen(req, timeout=3) as p:
                b_content = p.read()
                mime = p.getheader('Content-Type')
        except:
            sys.stderr.write('Error in fetching {}\n'.format(url))
            sys.stderr.write(traceback.format_exc())
            return None, None
        return b_content, mime

fetcher = Fetcher()

def fetch_and_save_img(word):
    data_dir = 'data/'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    for i, img_url in enumerate(img_url_list(word)):
        sleep(0.1)
        img, mime = fetcher.fetch(img_url)
        if not mime or not img:
            continue
        ext = guess_extension(mime.split(';')[0])
        if ext in ('.jpe', '.jpeg'):
            ext = '.jpg'
        if not ext:
            continue
        result_file = os.path.join(data_dir, str(i) + ext)
        with open(result_file, mode='wb') as f:
            f.write(img)
        print('fetched', img_url)


def img_url_list(word):
    url = 'https://twitter.com/search?f=images&vertical=default&q={}&src=typd&lang=ja'.format(quote(word))
    byte_content, _ = fetcher.fetch(url)
    structured_page = BeautifulSoup(byte_content.decode('UTF-8'), 'html.parser')
    img_link_elems = structured_page.find_all('span', attrs={'class': 'AdaptiveStreamGridImage'})
    img_urls = [e.get('data-url') for e in img_link_elems if e.get('data-url').startswith('http')]
    img_urls = list(set(img_urls))
    return img_urls

if __name__ == '__main__':
    word = sys.argv[1]
    fetch_and_save_img(word)
