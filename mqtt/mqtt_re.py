import paho.mqtt.client as mqtt
import time

HOST = "47.100.240.126"
PORT = 1883

def client_loop():
    client_id = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    client = mqtt.Client(client_id)    # ClientId不能重复，所以使用当前时间
    client.username_pw_set("xuqi", "qwert")  # 必须设置，否则会返回「Connected with result code 4」
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(HOST, PORT, 60)
    client.loop_forever()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("test3")

def on_message(client, userdata, msg):
    data = msg.payload.decode("utf-8")
    print(msg.topic+" "+data)
    with open('out_mqtt.txt','a',encoding='utf-8') as f:
        f.write(data+'\n')


if __name__ == '__main__':
    print('start....')
    client_loop()
