# -*- coding:utf-8 -*-

import os
import time

import serial
import serial.tools.list_ports

import CommunicationProtocol as cp

class SerialService(object):
    def __init__(self, port=None, baudrate=115200):
        if port is not None:
            self._serial_port = port
        else:
            try:
                self._serial_port = self.list_serial_ports()
            except IOError, e:
                raise e
            except SystemExit, e:
                raise e

        self._serial_baudrate = baudrate
        self._serial = self.open_serial(self._serial_port, self._serial_baudrate)

    def open_serial(self, port, baudrate):
        ''' 以 指定波特率 打开 指定串口\n @port\t\t\t- 端口号\n @baudrate\t- 波特率 '''
        try:
            print "Trying to open serial port: {0} @ {1} bps...".format(port, baudrate)
            _serial = serial.Serial(port, baudrate)
            print "[-o-] Listening [{0}]".format(port)
            return _serial
        except serial.SerialException, e:
            print "[)_(] Cannot open serial port {0}, exit...".format(port)
            raise SystemExit("Quitting...")

    def close_serial(self):
        ''' 关闭串口 '''
        self._serial.close()

    def write(self, addr, cmd, data):
        ''' 发送帧\n @addr\t- 地址\n @cmd\t- 指令\n @data\t- 数据\n '''
        frame = cp.frame_make(addr, cmd, data)
        self._serial.write(frame)
        return frame

    def read(self, timeout=0.1):
        ''' 读取帧\n @timeout\t- 超时时间 '''
        # 设置超时
        self._serial.timeout = timeout
        # 读取到帧尾字节
        frame = self._serial.read_until(cp.FRAME_TAIL)
        if len(frame) is 0:
            return False, "TIMEOUT"
        else:
            # 返回原始帧内容，用以监控
            return cp.frame_check(frame), frame

    @staticmethod
    def list_serial_ports():
        ''' 列举当前系统能检测到的串口号 '''
        ports = list(serial.tools.list_ports.comports())
        if len(ports) <= 0:
            raise IOError("No serial ports found.")
        else:
            print "Serial ports :"
            for i, port in enumerate(ports):
                print "\t({0}). {1}".format(i + 1, port)
            choose = None
            while True:
                key = raw_input("\nChoose [1-n or (q)uit]: ")
                if key is 'q':
                    choose = 'quit'
                    break
                else:
                    p = int(key) - 1
                    if p > len(ports):
                        print "Out of range, try again"
                    else:
                        choose = p
                        break
            if choose is 'quit':
                raise SystemExit("Quitting...")
            else:
                port = str(ports[p])
                return (port.split(' '))[0]

    '''
    #def communicate(self, addr, cmd, data, timeout=1):
    #     def handler(signum, frame):    
    #        raise AssertionError
    #     try:
    #         signal.signal(signal.SIGALRM, handler)
    #         self.write(addr, cmd, data)
    #         signal.alarm(timeout)
    #         frame = self.read()
    #         signal.alarm(0)
    #         return frame
    #     except AssertionError:
    #         logger.error("communicate conn't finished in %d seconds, timeout!" % (timeout))
    #         return None
    '''

    def communicate(self, addr, cmd, data, timeout=0.1):
        ''' 完成发送接收一次通信\n @addr\t\t- 地址\n @cmd\t\t- 指令\n @data\t\t- 数据\n @timeout\t- 超时 '''
        ''' TODO 通信过程：\n 主机 -> 从机 frame\n 从机 处理 frame\n 从机 -> 主机 ack_frame 【有超时处理和错误处理】、【重发】（超时重发 & 出错重发）\n 主机 处理 ack '''
        self.write(addr, cmd, data)
        return self.read(timeout)


if __name__ == "__main__":
    serialService = SerialService('COM1')
    print serialService.communicate(1, 1, "This is rsy!", 5)
