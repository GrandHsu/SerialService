# -*- coding:utf-8 -*-

FRAME_HEAD = "ttt"
FRAME_TAIL = "~"

FRAME_DATALENGTH = 12
FRAME_FRAMELENGTH = 8 + FRAME_DATALENGTH * 2

'''
制作通信帧
@addr   - 地址
@cmd    - 指令
@data   - 数据
@return - 帧字符串
'''
def frameMake(addr, cmd, data):
    da = ['0' for _ in range(24)]
    for i, d in enumerate(data):
        split = charSplit(d)
        da[2 * i] = split[0]
        da[2 * i + 1] = split[1]
    da = [chr(addr), chr(cmd)] + da
    check = frameCheckSum(da)
    frame = "{0}{1}{2}{3}".format(FRAME_HEAD, "".join(da), "".join(charSplit(check)), FRAME_TAIL)
    return frame
    
'''
二字节拆分 - 拆分
@char     - 一个字节
@return   - 拆分后的两个字节
'''
def charSplit(char):
    c = ord(char)
    return '{0}{1}'.format(hex(c / 16)[2:].upper(), hex(c % 16)[2:].upper())

'''
二字节拆分 - 组合
@charH    - 高字节
@charL    - 低字节
@return   - 组合后的两个字节
'''
def charCombine(charH, charL):
    return chr(int('{0}{1}'.format(charH, charL), base=16))

'''
计算校验和
@data   - 数据
@return - 校验和值
'''
def frameCheckSum(data):
    check = 0
    for d in data:
        check = check + ord(d)
    return chr(check % 256)

'''
检查数据帧
@frame  - 数据帧
@return - 返回 地址，指令，数据
'''
def frameCheck(frame):
    ''' e 错误输出 '''
    e = "[frameCheck] fail: "

    ''' 检查帧长 '''
    if len(frame) is not FRAME_FRAMELENGTH:
        print e + "length not match!"
        return
    ''' 检查帧头 '''
    if not frame.startswith(FRAME_HEAD):
        print e + "head not match!"
        return
    ''' 检查帧尾 '''
    if not frame.endswith(FRAME_TAIL):
        print e + "tail not match!"
        return
    ''' 校验数据 '''
    if not charCombine(frame[-3], frame[-2]) == frameCheckSum(frame[3:-3]):
        print e + "data check not correct!"
        return
        
    addr = ord(frame[3])
    cmd  = ord(frame[4])
    da = frame[5:-3]
    data = [charCombine(da[2 * i], da[2 * i + 1]) for i in range(len(da)/2)]
        
    return addr, cmd, data


if __name__ == '__main__':
    frame = frameMake(1, 2, "This is rsy!")
    print frame
    print frameCheck(frame)