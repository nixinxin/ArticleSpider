# -*- coding: utf-8 -*-
__author__ = "nixinxin"
import re

aa = """

            2018/03/09 · """

reslut = re.match('.*?(\d+.*\d).*', aa, re.DOTALL)
print(reslut.group(1))