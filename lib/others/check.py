# coding:utf-8
"""(暂时没用)"""

import re

pattern = dict(
    email=re.compile(r'^([\w\-.]+)@([\w-]+)(\.([\w-]+))+$'),
    password=re.compile(
        r'^[0-9A-Za-z`~!@#$%^&*()_+\-=\{\}\[\]:;"\'<>,.\\|?/]{6,24}$'))
