# -*- coding:utf-8 -*-

import os
import socket

import json

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
                r = comm.recv(self.datalength)
                # 检查客户端是否正确
                if not r.endswith('hello comm!'):
                    print TAG, "Error", "unidentified client, close connection..."
                    comm.close()
                    continue
                # 开始通信
                print TAG, "communication client, let's do it"

                r = comm.recv(self.datalength)
                decode = json.loads(r)

                self.serial.write(decode["addr"], decode["cmd"], decode["data"])

                comm.close()
        except:
            pass
        finally:
            communication.close()

    def monitor(self):
        pass


if __name__ == "__main__":

    ss = serialService.SerialService('COM1')

    socketService = SocketService(ss)
    socketService.communicate()