# 导入 socket、sys 模块
import socket
import sys
from _thread import *

# 创建 socket 对象
serversocket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM) 

# 获取本地主机名
host ="172.19.128.98"
port = 9999

# 绑定端口号
serversocket.bind((host, port))

# 设置最大连接数，超过后排队
serversocket.listen(10)
    # 建立客户端连接
clientsocket,addr = serversocket.accept()    
  # print (msg.decode('utf-8'))

def clientthread(clientsocket):
    while True:
        try:
            data = clientsocket.recv(1024)
            if data == b'' or data == b' ':
            	break
            if data is not None or data != '':
                msg = data.decode('utf-8')
                print(msg)
                with open('out_socket.txt','a',encoding='utf-8') as f:
                    f.write(msg+'\n')

            else: print('None')
            # data_loaded = json.loads(data)
        except socket.error:
                print("One Client Connected over!")
                break
    clientsocket.close()

    # msg='欢迎访问菜鸟教程！'+ "\r\n"
    # clientsocket.send(msg.encode('utf-8'))
clientthread(clientsocket)

# clientsocket.close()
serversocket.close()