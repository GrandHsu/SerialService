from Queue import Queue
import random
import time
import  thread

import struct
import serial

# Producer thread
class ComDev:
    def __init__(self):
        self.sharedata = Queue()
        self.dt = 1
        self.nStep = 0
        self.com = None
        
    def Open(self,com):
        try:
            self.com = serial.Serial(com, baudrate=4800, bytesize=8, parity='N', stopbits=1, xonxoff=0, timeout=1)
        except:
            self.com = None
            print 'Open %s fail!' %com
        
    def Close(self):
        if type(self.com) != type(None):
            self.com.close()
            self.com = None
            return True
        return False
    
    def ReadData(self,CmdID,SubCmdID,RevBytes):
        if type(self.com) != type(None):
            try:
                self.com.write(struct.pack('B', CmdID))
                tmp = self.com.read(1)
                self.com.write(struct.pack('B',SubCmdID))
                data = self.com.read(RevBytes)
                return data
            except:
                print 'ReadData fail!'
                self.Close()
                return None
        return None
            
    def SendData(self,CmdID,SubCmdID,Data,SendBytes):
        if type(self.com) != type(None):
            try:
                self.com.write(struct.pack('B', CmdID))
                
                tmp = self.com.read(1)
                
                print tmp
                self.com.write(struct.pack('B',SubCmdID))
                
                self.com.write(struct.pack('B',Data))
                print 1
                return True
            except:
                print 'SendData fail!'
                self.Close()
                return False
        return False
    
    def Transform(self,inData):
        global outData
        try:
            tmpdata= inData[::-1]
            outData = struct.unpack('ffff',tmpdata)
            return outData
        except:
            print 'Transform fail!'
            self.Close()
            return None

    def DevInit(self):
        step1 = self.ReadData(0x0A,0x0B,26)
        step2 = self.ReadData(0x0A,0x0B,26)
        step3 = self.ReadData(0x0A,0x0D,16)
        step4 = self.ReadData(0x0A,0x0B,26)
        step5 = self.ReadData(0x09,0x0B,26)
        step6 = self.ReadData(0x0A,0x09,60)
        step7 = self.ReadData(0x09,0x09,60)
        return True      
        
    def SetDevParam(self,param):
        self.SendData(0X09,0x09,Param)
        
    def Begin(self,dt_ms):
        self.keepGoing = self.running = True
        self.nStep = 0
        self.dt = dt_ms/1000.0
        thread.start_new_thread(self.Run, ())

    def Stop(self):
        self.keepGoing = False

    def IsRunning(self):
        return self.running
    
    def IsOpen(self):
        return type(self.com) != type(None)

    def Run(self):
        while self.keepGoing:
            #data=(random.randint(0,1000),random.randint(0,300))
            self.ReadData(0X0A,0x07,1)
            tmpdata = self.ReadData(0X0A,0x0F,16)
            data = self.Transform(tmpdata)
            self.sharedata.put(data)
            time.sleep(self.dt)
        self.running = False
    
    def GetData(self):
        nsize = self.sharedata.qsize()
        if nsize > 0:
            return self.sharedata.get()
        else:
            return None