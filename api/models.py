#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/12 10:34
# @Author  : KuoYu
# @Site    : pythonic.site
# @File    : models
# @Software: PyCharm
from concurrent.futures import ThreadPoolExecutor

import pymongo
import tornado.web
from tornado import gen
from tornado.concurrent import run_on_executor
import json
from api.utils import *


class BaseHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(20)

    col_name = None
    include_field = ()
    image_field = ()
    show_field = {}
    success_msg = {'status': 200}
    failure_msg = {'status': 404}

    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)
        self.show_field.update({i: 1 for i in self.include_field})
        # 绝对不显示_id
        self.show_field.update({'_id': 0, 'id': 1})
        self.col = MongodbUtils(col_name=self.col_name).col

    # 查询
    # 采用异步, 使用seige测试1000并发 可持续5分钟以上
    @gen.coroutine
    def get(self, uid):
        context = yield self.search(uid)
        self.write(context)

    @run_on_executor
    def search(self, uid):
        res = self.col.find_one({'id': str(uid)}, self.show_field) \
            if uid else \
            {i['id']: i for i in self.col.find({}, self.show_field).sort('_id', pymongo.DESCENDING).limit(20) if 'id' in i}
        context = json.dumps(res)
        return context

    def put(self, *args, **kwargs):
        with json_deserializer(self.request.body) as json_str:
            uid = json_str.get('id', '')
            find_res = self.col.find_one({"id": uid}, self.show_field)
            if find_res is not None:
                self.col.update_one({"id": uid}, {"$set": json_str})
                self.set_status(200)
                self.write(self.success_msg)
            else:
                self.set_status(404)
                self.write(self.failure_msg)

    # 提交
    def post(self, *args, **kwargs):
        with json_deserializer(self.request.body) as json_str:
            uid = json_str.get('id', '')
            res = self.col.find_one({"id": uid}, self.show_field)
            if uid:
                if res is None:
                    res_dict = {key: json_str.get(key, '') for key in self.include_field}
                    if any(res_dict.values()):
                        self.col.insert_one(res_dict)
                else:
                    self.put(self, args, kwargs)
                self.write(self.success_msg)
            else:
                self.write(self.failure_msg)

    # 根据id删除
    def delete(self, uid):
        (self.send_error(404) & self.write(self.failure_msg)) \
            if not uid \
            else (self.col.find_one_and_delete({'id': str(uid)}) & self.write(self.success_msg))

    def data_received(self, chunk):
        super(BaseHandler, self).data_received(chunk)


class UserHandler(BaseHandler):
    col_name = 'user'
    image_field = ('avatar',)
    include_field = (
        'id', 'name', 'avatar', 'mail', 'phone'
    )


class RecordHandler(BaseHandler):
    col_name = 'record'
    include_field = (
        'id', 'time', 'description'
    )


class DeviceHandler(BaseHandler):
    col_name = 'device'
    include_field = (
        'id', 'name', 'description'
    )


class FieldHandler(BaseHandler):
    col_name = 'field'
    image_field = ('image',)
    include_field = (
        'id', 'name', 'image',
        'humidity', 'temperature', 'lighting',
        'co2', 'conductivity', 'salt'
    )


# TODO:实现文件上传
@tornado.web.stream_request_body
class FileHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass
