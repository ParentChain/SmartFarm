import logging
import os

import paho.mqtt.client as MQTT
import tornado.httpserver
import tornado.ioloop
import tornado.netutil
import tornado.web
from tornado.options import define

from api.models import *

# define('port', default=8848, type=int, help='default 8848')
define('allowed_hosts', default='localhost:8848', multiple=True, help='Allowed')

logger = logging.getLogger()
fm = tornado.log.LogFormatter(
    fmt='[%(asctime)s]%(color)s[%(levelname)s]%(end_color)s[(module)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')
tornado.log.enable_pretty_logging(logger=logger)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/api/farm/field/(.*)", FieldHandler),
            (r"/api/farm/user/(.*)", UserHandler),
            (r"/api/farm/device/(.*)", DeviceHandler),
            (r"/api/farm/record/(.*)", RecordHandler),
        ]
        settings = {
            'static_path': os.path.join(os.path.dirname(__file__), "static"),
            'template_path': os.path.join(os.path.dirname(__file__), "template"),
            'debug': False,
        }
        tornado.web.Application.__init__(self, handlers, settings=settings)


def run_tornado(port):
    tornado.options.parse_command_line()
    sockets = tornado.netutil.bind_sockets(port)
    tornado.process.fork_processes(0)
    http_server = tornado.httpserver.HTTPServer(Application(), xheaders=True)
    http_server.add_sockets(sockets)
    # http_server.bind(options.port)
    logger.info("start the tornado at port {}".format(port))

    try:
        # http_server.start(0)
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        logger.info("finished the tornado ")


def run_mqtt_client(host="127.0.0.1", port=1883):
    def on_message(client, userdata, msg):
        with json_deserializer(msg.payload.decode()) as json_str:
            # TODO[1]:实现消息接收的存储 （并发 实时 motor 实现异步MongoDB操作）
            print(msg.topic + ":" + json.dumps(json_str))

    # TODO[2]：实现publish的
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe([("index/field", 0), ("index/record", 0), ("detail/field", 0)])


    client = MQTT.Client()
    client.username_pw_set("admin", "password")  # 必须设置，否则会返回「Connected with result code 4」
    client.on_connect = on_connect
    client.on_message = on_message
    try:
        client.connect_async(host, port, 60)
        logger.info("start the mqtt at port {} in {}".format(port, host))
        client.loop_forever()
    except KeyboardInterrupt:
        client.disconnect()
        logger.info("finished mqtt server")

if __name__ == '__main__':
    from multiprocessing import Process

    ps = [
        Process(target=run_tornado, args=(8848,)),
        Process(target=run_mqtt_client)
    ]

    for p in ps:
        p.start()
