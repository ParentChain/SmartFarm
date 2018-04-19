#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/11 15:54
# @Author  : KuoYu
# @Site    : pythonic.site
# @File    : mqtt_test
# @Software: PyCharm
import paho.mqtt.client as mqtt


def on_connect(client,userdata,rc):
    print("Connected with RESTful code"+str(rc))
    client.subscribe("$SYS/#")

def on_msg(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))



if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_msg
    client.connect("118.113.128.82", 1883, 60)
    client.loop_forever()