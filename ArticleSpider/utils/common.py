# -*- coding: utf-8 -*-
import re

__author__ = "nixinxin"
import hashlib


def get_md5(url):
    if isinstance(url, str):
        url = url.encode('utf-8')
        # 不接受uniconde
        m = hashlib.md5()
        m.update(url)
        return m.hexdigest()


def convert_int(value):
    match = re.match(".*?(\d+.*\d).*", value)
    if match:
        value = match.group(1)
    else:
        value = 0
    return int(value)


if __name__ == '__main__':
    print(get_md5('http://blog.jobbole.com/all-posts/'.encode('utf-8')))
