#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/12 14:28
# @Author  : KuoYu
# @Site    : pythonic.site
# @File    : mongoUtil
# @Software: PyCharm
import contextlib
import json
import re

from pymongo import MongoClient


class MongodbUtils():
    col = None

    def __init__(self, db_name='farm', col_name='test'):
        self.client = MongoClient('127.0.0.1')
        self.setDB(db_name)
        self.setCollection(col_name)

    def setDB(self, db_name):
        if self.client is None:
            raise Exception("not set client")
        self.db = self.client[db_name]

    def setCollection(self, col_name):
        if self.db is None:
            raise Exception("not set db")
        self.col = self.db[col_name]


@contextlib.contextmanager
def json_deserializer(my_str):
    try:
        yield json.loads(my_str)
    except ValueError:
        # log here not vaild JSON
        yield {"status":"not valid json"}


# 弃用保留。 原因：保证json格式正确即可
# 格式化request.body内的json
def _format_body2json(context):
    body = re.sub(b"(,?)(\w+?)\s*?:", b"\1'\2':", context)
    res = body.replace(b"'", b'"')
    return res
