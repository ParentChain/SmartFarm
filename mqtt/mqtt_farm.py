import json

import paho.mqtt.client as mqtt
from api.utils import json_deserializer

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe([("index/field", 0), ("index/record", 0), ("detail/field", 0)])


def on_message(client, userdata, msg):
    with json_deserializer(msg.payload.decode()) as json_str:
        #TODO[1]:实现消息接收的存储 （并发 实时 motor 实现异步MongoDB操作）
        print(msg.topic+":"+json.dumps(json_str))
#TODO[2]：实现publish的
if __name__=='__main__':
    client = mqtt.Client()
    client.username_pw_set("admin", "password")  # 必须设置，否则会返回「Connected with result code 4」
    client.on_connect = on_connect
    client.on_message = on_message

    HOST = "192.168.20.128"
    try:
        client.connect_async(HOST, 1883, 60)
        client.loop_forever()
    except KeyboardInterrupt:
        client.disconnect()

# class MqttClient(mqtt.Client):
#     def connect(self, rc):
#         print("Connected with result code " + str(rc))
#         client.subscribe([("index/field", 0), ("index/record", 0), ("detail/field", 0)])