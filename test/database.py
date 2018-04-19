#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/12 11:14
# @Author  : KuoYu
# @Site    : pythonic.site
# @File    : database
# @Software: PyCharm
import urllib.parse

from pymongo import MongoClient

#完全不需要密码，mongoDB内部执行即可
client = MongoClient()


print(client)

db = client['new'] # 有则返回new DB对象，无则创建且返回
# db = client.news
print(db)
# collect = db.papers
collect =  db["papers"]
collect.insert({"name":"something"})
# idkey = collect.insert({'name':'hello2','context':'i am mongoDB'})
# print(idkey)

print(collect.find_one('name'))

client.close()
print('-'*5)
post1 = collect.find_one({'foo':'bar'})
post2 = collect.find_one('id')
print(post1)
print(post2)
