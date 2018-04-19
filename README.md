

Farm

MQTTTLENS

SWAGGER

DATABASE: MANGODB

FILE: IMG



http://120.78.158.96:8080/swagger-ui.html



## Tornado

> API，非阻塞可以大量连接，实时连接

### pymongo

```python
# exists判断是否存在
m = db[collName].find({"s": None}).count()  
n = db[collName].find({"s": {'$regex': ".*"}}).count()  
k = db[collName].find({"si": None}).count()  
z = db[collName].find({"si": {'$exists': True}}).count()  
```



## MQTT

> MQTT协议，实时性，传递JSON

#### 安装

[centos6.5 mosquitto 安装]:https://app.yinxiang.com/shard/s2/nl/16139344/a7cea12a-05ad-43dc-b915-73de664d9afb
[如何使用mqtt]:https://zhuanlan.zhihu.com/p/31284319

```bash
 linux下安装MQTT
/usr/sbin/mosquitto -c /etc/mosquitto/mosquitto.conf #不会修改就不要乱修改 -d 守护进程后台运行
#server：
mosquitto_pub -t "主题" -h 127.0.0.1 -m "{\"pin\":17,\"value\":0}"
#client：
mosquitto_sub -v -t "主题" -h 127.0.0.1    （先启动）
```



```python
# MQTT 客户端
import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("iot.eclipse.org", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
```

## Django

> ## 数据展示，配合e-chart



## Numpy和Pandas

> 数据处理

## 资料收集

[pymongo API]: http://api.mongodb.com/python/current/api/index.html
[pymongo 文档]: http://api.mongodb.com/python/current/tutorial.html
[什么是bson]: https://pypi.python.org/pypi/python-bsonjs
[tornado 入门 request]: https://moreoronce.gitbooks.io/learnpython/content/300/308.html
[python如何构建MQ消息队列]: https://www.rabbitmq.com/tutorials/tutorial-one-python.html
[tornado 项目启动]: https://mirrors.segmentfault.com/itt2zh/ch1.html#ch1-1-1
[tornado 中文文档]: http://tornado-zh.readthedocs.io/zh/latest/httpclient.html#request

```bash
siege http://localhost:8848/api/farm/field/ -c3000 -t4s # 4s内3000并发
```



# 问题

- 什么是长轮询

- 什么是MQ消息队列

- 什么是websocket

- 如何同时运行两个程序？

- 父进程被杀之后？

  ```python
  def daemonize(pid_file=None):
      """
      创建守护进程
      :param pid_file: 保存进程id的文件
      :return:
      """
      # 从父进程fork一个子进程出来
      pid = os.fork()
      # 子进程的pid一定为0，父进程大于0
      if pid:
          # 退出父进程，sys.exit()方法比os._exit()方法会多执行一些刷新缓冲工作
          sys.exit(0)

      # 子进程默认继承父进程的工作目录，最好是变更到根目录，否则回影响文件系统的卸载
      os.chdir('/')
      # 子进程默认继承父进程的umask（文件权限掩码），重设为0（完全控制），以免影响程序读写文件
      os.umask(0)
      # 让子进程成为新的会话组长和进程组长
      os.setsid()

      # 注意了，这里是第2次fork，也就是子进程的子进程，我们把它叫为孙子进程
      _pid = os.fork()
      if _pid:
          # 退出子进程
          sys.exit(0)

      # 此时，孙子进程已经是守护进程了，接下来重定向标准输入、输出、错误的描述符(是重定向而不是关闭, 这样可以避免程序在 print 的时候出错)

      # 刷新缓冲区先，小心使得万年船
      sys.stdout.flush()
      sys.stderr.flush()

      # dup2函数原子化地关闭和复制文件描述符，重定向到/dev/nul，即丢弃所有输入输出
      with open('/dev/null') as read_null, open('/dev/null', 'w') as write_null:
          os.dup2(read_null.fileno(), sys.stdin.fileno())
          os.dup2(write_null.fileno(), sys.stdout.fileno())
          os.dup2(write_null.fileno(), sys.stderr.fileno())

      # 写入pid文件
      if pid_file:
          with open(pid_file, 'w+') as f:
              f.write(str(os.getpid()))
          # 注册退出函数，进程异常退出时移除pid文件
          atexit.register(os.remove, pid_file)
  ```

- tornado 如何多线程？

  不实现多线程，因为tornado是单线程轮询[tornado 多进程实现]["https://blog.csdn.net/weiwangchao_/article/details/74990178"]

- 异步和非阻塞什么时候使用?
