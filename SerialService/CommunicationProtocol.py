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
        check = CommunicationProtocol.frameCheck(da)
        frame = "{0}{1}{2}{3}{4}{5}".format(FRAME_HEAD,chr(addr), chr(cmd), "".join(da), "".join(CommunicationProtocol.charSplit(check)), FRAME_TAIL)
        print frame
    
    @staticmethod
    def charSplit(char):
        c = ord(char)
        return '{0}{1}'.format(hex(c / 16)[2:].upper(), hex(c % 16)[2:].upper())

    @staticmethod
    def frameCheck(data):
        check = 0
        for d in data:
            check = check + ord(d)
        return chr(check % 256)

if __name__ == '__main__':
    CommunicationProtocol.frameMake(1, 2, "111111111111")