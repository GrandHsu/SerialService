# -*- coding:utf-8 -*-

import struct

FRAME_HEAD = "ttt"
FRAME_TAIL = "~"

class CommunicationProtocol(object):
    def __init__(self, *args, **kwargs):
        return super(CommunicationProtocol, self).__init__(*args, **kwargs)

    @staticmethod
    def frameMake(addr, cmd, data):
        da = ['0' for _ in range(24)]
        for i, d in enumerate(data):
            split = CommunicationProtocol.charSplit(d)
            da[2 * i] = split[0]
            da[2 * i + 1] = split[1]
        check = CommunicationProtocol.frameCheckSum(da)
        frame = "{0}{1}{2}{3}{4}{5}".format(FRAME_HEAD,chr(addr), chr(cmd), "".join(da), "".join(CommunicationProtocol.charSplit(check)), FRAME_TAIL)
        return frame
    
    @staticmethod
    def charSplit(char):
        c = ord(char)
        return '{0}{1}'.format(hex(c / 16)[2:].upper(), hex(c % 16)[2:].upper())

    @staticmethod
    def frameCheckSum(data):
        check = 0
        for d in data:
            check = check + ord(d)
        return chr(check % 256)

    @staticmethod
    def frameCheck(frame):
        if FRAME_HEAD != frame[0:3]:
            print "[frameCheck] fail : head not match!"
            return
        


if __name__ == '__main__':
    frame = CommunicationProtocol.frameMake(1, 2, "111111111111")
    print frame
    CommunicationProtocol.frameCheck(frame)