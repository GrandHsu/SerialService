# -*- coding:utf-8 -*-

import os
import socket

import json
import traceback

import serialService

class SocketService(object):

    def __init__(self, serial):
        
        self.localhost  = 'localhost'
        self.datalength = 1024
        self.serial = serial

        pass

    def communicate(self):
        TAG = '[communicate]'
        communication = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        communication.bind((self.localhost, 15051))
        communication.listen(1)
        try:
            comm = None
            while True:
                print TAG, "accepting..."
                comm, address = communication.accept()
                #receive_from_socket = comm.recv(self.datalength)
                ## 检查客户端是否正确
                #if not receive_from_socket.endswith('hello comm!'):
                #    print TAG, "Error", "unidentified client, close connection..."
                #    comm.close()
                #    continue
                ## 开始通信
                print TAG, "communication client, let's do it"

                while True:
                    receive_from_socket = comm.recv(self.datalength)
                    decode = json.loads(receive_from_socket)

                    print self.serial.write(decode["addr"], decode["cmd"], decode["data"])

                    print "receive from serial..."
                    receive_from_serial = self.serial.read(2)

                    print receive_from_serial

                    if receive_from_serial[0] is False:
                        print TAG, "Error", receive_from_serial[1], "abandon this frame and continue..."
                        continue

                    data = receive_from_serial[1]
                    encode = { "addr": data[0], "cmd": data[1], "data": "".join(data[2])}

                    send_to_socket = json.dumps(encode)
                    comm.send(send_to_socket)

                comm.close()
        except Exception, e:
            traceback.print_exc()
            print e
        finally:
            communication.close()

    def monitor(self):
        pass


if __name__ == "__main__":

    ss = serialService.SerialService('COM3')

    socketService = SocketService(ss)
    socketService.communicate()