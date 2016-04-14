# -*- coding:utf-8 -*-

FRAME_HEAD = "ttt"
FRAME_TAIL = "~"

FRAME_DATALENGTH = 12
FRAME_FRAMELENGTH = 8 + FRAME_DATALENGTH * 2

def frame_make(addr, cmd, data):
    ''' 制作通信帧\n @addr\t\t- 地址\n @cmd\t\t- 指令\n @data\t\t- 数据\n @return\t- 帧字符串 '''
    da = ['0' for _ in range(24)]
    for i, d in enumerate(data):
        split = char_split(d)
        da[2 * i] = split[0]
        da[2 * i + 1] = split[1]
    da = [chr(addr), chr(cmd)] + da
    check = frame_check_sum(da)
    frame = "{0}{1}{2}{3}".format(FRAME_HEAD, "".join(da), "".join(char_split(check)), FRAME_TAIL)
    return frame
    
def char_split(char):
    ''' 二字节拆分\t- 拆分\n @char\t\t\t- 一个字节\n @return\t\t- 拆分后的两个字节 '''
    c = ord(char)
    return '{0}{1}'.format(hex(c / 16)[2:].upper(), hex(c % 16)[2:].upper())

def char_combine(charH, charL):
    ''' 二字节拆分\t- 组合\n @charH\t\t- 高字节\n @charL\t\t\t- 低字节\n @return\t\t- 组合后的两个字节\n '''
    return chr(int('{0}{1}'.format(charH, charL), base=16))

def frame_check_sum(data):
    ''' 计算校验和\n @data\t\t- 数据\n @return\t- 校验和值 '''
    check = 0
    for d in data:
        check = check + ord(d)
    return chr(check % 256)

def frame_check(frame):
    ''' 检查数据帧\n @frame\t- 数据帧\n @return\t- 返回 地址，指令，数据 '''
    ''' e 错误输出 '''
    e = "[frameCheck] fail: "

    ''' 检查帧长 '''
    if len(frame) is not FRAME_FRAMELENGTH:
        print e + "length not match!"
        return False, "E.LENGTH"
    ''' 检查帧头 '''
    if not frame.startswith(FRAME_HEAD):
        print e + "head not match!"
        return False, "E.HEAD"
    ''' 检查帧尾 '''
    if not frame.endswith(FRAME_TAIL):
        print e + "tail not match!"
        return False, "E.TAIL"
    ''' 校验数据 '''
    if not char_combine(frame[-3], frame[-2]) == frame_check_sum(frame[3:-3]):
        print e + "data check not correct!"
        return False, "E.CHECK"
    addr, cmd, da = ord(frame[3]), ord(frame[4]), frame[5:-3]
    data = [char_combine(da[2 * i], da[2 * i + 1]) for i in range(len(da)/2)]
    return True, (addr, cmd, data)


if __name__ == '__main__':
    frame = frame_make(1, 2, "This is rsy!")
    print frame
    print frame_check(frame)