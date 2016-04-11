# -*- coding:utf-8 -*-

import os
import threading
import time

import serial
import serial.tools.list_ports

import CommunicationProtocol as cp

class SerialService(object):
    def __init__(self):
        pass

if __name__ == "__main__":
    frame = cp.frameMake(1, 2, "This is rsy!")
    print frame
    print cp.frameCheck(frame)
