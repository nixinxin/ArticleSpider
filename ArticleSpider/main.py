# -*- coding: utf-8 -*-
__author__ = "nixinxin"

import os
import sys
from scrapy.cmdline import execute

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


execute(['scrapy', 'crawl', 'jobbole'])