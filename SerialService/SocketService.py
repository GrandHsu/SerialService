# -*- coding:utf-8 -*-
''' SocketService '''

import os
import socket
import threading

import json
import traceback

import serialService

class SocketService(object):

    # 不能直接绑定 localhost, 否则别的机器不能访问本机
    localhost = '192.168.0.119'
    datalength = 1024
    comm_port = 15051
    monitor_port = 15052

    communication = None
    monitor = None
    
    def __init__(self, serial):
        self.serial = serial

    def start(self):
        self.monitor()
        self.communicate()
        # 正常退出 或 出现异常
        
        # self.monitor.close()
        # self.communication.close()

    def communicate(self):
        tag = '[communicate]'
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c.bind((self.localhost, self.comm_port))
        c.listen(1)
        try:
            while True:
                print tag, "accepting..."
                self.communication, address = c.accept()
                receive_from_socket = self.communication.recv(self.datalength)
                # 检查客户端是否正确
                if not receive_from_socket.endswith('hello comm!'):
                    print TAG, "Error", "unidentified client, close connection..."
                    communication.close()
                    continue
                # 开始通信
                print tag, "communication client, let's do it"
                while True:
                    receive_from_socket = self.communication.recv(self.datalength)
                    # print tag, 'log', receive_from_socket
                    # client 断开了
                    if len(receive_from_socket) is 0:
                        print tag, "connection lost..."
                        self.communication.close()
                        break
                    
                    decode = json.loads(receive_from_socket)
                    # print tag, 'log', decode

                    frame = self.serial.write(decode["addr"], decode["cmd"], decode["data"])
                    print tag, "send ->", frame

                    success, data, frame = self.serial.read(0.5)
                    if success is False:
                        print tag, "-> recv", "Error", data
                        print tag, "abandon this frame & continue..."
                        encode = {"error": data}
                        self.communication.send(json.dumps(encode) + "\r\n")
                    else:
                        print tag, "recv", frame
                        encode = {"addr": data[0], "cmd": data[1], "data": "".join(data[2]), "error": "NONE"}
                        self.communication.send(json.dumps(encode) + "\r\n")

                self.communication.close()
        except Exception, e:
            traceback.print_exc()
            print e
        finally:
            c.close()

    def monitor(self):
        tag = '[monitor]'
        print tag, "init monitor thread..."
        
        m = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        m.bind((self.localhost, self.monitor_port))
        m.listen(1)

        def get():
            self.monitor, address = m.accept()
            print tag, "get one connection"
            return self.monitor
        
        t = threading.Thread(target=get)
        t.setDaemon(True)
        t.start()


if __name__ == "__main__":
    serial_socket = serialService.SerialService('COM3')
    socketService = SocketService(serial_socket)
    socketService.start()
    