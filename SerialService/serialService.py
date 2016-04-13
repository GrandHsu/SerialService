# -*- coding:utf-8 -*-

import os
import threading
import time
import signal

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
        try:
            print "Trying to open serial port: {0} @ {1} bps...".format(port, baudrate)
            _serial = serial.Serial(port, baudrate)
            print "[-o-] Listening [{0}]".format(port)
            return _serial
        except serial.SerialException, e:
            print "[)_(] Cannot open serial port {0}, exit...".format(port)

    def close_serial(self):
        self._serial.close()

    def write(self, addr, cmd, data):
        frame = cp.frame_make(addr, cmd, data)
        self._serial.write(frame)

    def read(self, timeout=0.1):
        # frame = self._serial.read(cp.FRAME_FRAMELENGTH)
        # frame = ""
        # while True:
            #char = self._serial.read()
            ## frame.join(char)
            #frame += char
            #if char is cp.FRAME_TAIL:
            #    break
        self._serial.timeout = timeout
        frame = self._serial.read_until(cp.FRAME_TAIL)
        return cp.  (frame)

    @staticmethod
    def list_serial_ports():
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

    def communicate(self, addr, cmd, data, timeout=0.1):
        self.write(addr, cmd, data)
        print self.read(timeout)


if __name__ == "__main__":
    serialService = SerialService('COM1')

    serialService.communicate(1, 2, "This is rsy!", 5)
