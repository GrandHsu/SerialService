# -*- coding:utf-8 -*-

import serial
import serial.tools.list_ports
import time
import threading
import msvcrt
import os

# AllValues = {}
# inputVotage,                        // 12
# outputVotage,                       // 13
# inputCurrent,                       // 14
# outputCurrent,                      // 15
# inputRectifierBridgeOverheat,       // 16
# transformerOverheat,                // 17
# outputRectifierBridgeOverheat,      // 18
# switchTubeOverheat

showBuff = '''
               The Power Monitoring System
========================================================
    1. inputVoltage                     : %(IV)04d V
    2. outputVoltage                    : %(OV)04d V
    3. inputCurrent                     : %(IC)04d A
    4. outputCurrent                    : %(OC)04d A
    5. inputRectifierBridgeOverheat     : %(IH)5.2f C
    6. transformerOverheat              : %(TH)5.2f C
    7. outputRectifierBridgeOverheat    : %(OH)5.2f C
    8. switchTubeOverheat               : %(SH)5.2f C'''


class keyLintener(threading.Thread):
    def __init__(self, file):
        threading.Thread.__init__(self)
        self.file = file
        self.fileStatus = False

    def getFile(self):
        return self.file, self.fileStatus

    def run(self):
        while True:
            key = msvcrt.getch()
            if key == "q":
                if self.file is not None:
                    print "Press c to stop saving FIRST!!!"
                    continue
                print "Now quit..."
                os._exit(0)
            elif key == "s":
                if self.file is None:
                    self.fileStatus = False
                    self.file = open("data/{0}.txt".format(time.strftime('%m %d %H %M %S', time.localtime(time.time()))), 'a')
                else:
                    print "Saving data now... Press c to stop saving"
            elif key == "c":
                if self.file is None:
                    print "Not saving now...  Press s to start saving"
                else:
                    self.fileStatus = True
                    self.file = None
                    # self.file.close() # raise error : I/O operation on closed file
                # print "Save data to {0}".format()


class myPowerMoniter():
    """docstring for myPowerMoniter"""
    def __init__(self, logfile="moniterLog.txt"):
        super(myPowerMoniter, self).__init__()
        self.filename = logfile
        self.loading = "-/|" + '\\'
        self.loadingCount = 0
        self.IV = 0.0
        self.OV = 0.0
        self.IC = 0.0
        self.OC = 0.0
        self.IH = 0.0
        self.TH = 0.0
        self.OH = 0.0
        self.SH = 0.0

    def chars2Int(data, position):
        return (ord(data[position * 2]) + ord(data[position * 2 + 1]) * 256)

    def showData(source):
        data = list(source)
        self.IV = chars2Int(data, 0)
        self.OV = chars2Int(data, 1)
        self.IC = chars2Int(data, 2)
        self.OC = chars2Int(data, 3)
        self.IH = chars2Int(data, 4) / 100.0
        self.TH = chars2Int(data, 5) / 100.0
        self.OH = chars2Int(data, 6) / 100.0
        self.SH = chars2Int(data, 7) / 100.0
        print showBuff % locals()
        print "=========================" + loading[loadingCount] * 5 + "=========================="
        loadingCount += 1
        if loadingCount == 4:
            loadingCount = 0
        # save data to file
        file = open(self.filename, 'a')
        print >> file, time.strftime('%m-%d %H:%M:%S', time.localtime(time.time())), IH, TH, OH, SH
        file.close()


def voltageOutput(data, file):
    s = ""
    for x in xrange(0, len(data) / 2 - 1):
        s += "{0} ".format(ord(data[2 * x]) * 256 + ord(data[2 * x + 1]))
    if file[0] is None:
        print "read {0} char(s) [not saving]".format(len(data))
    else:
        print >> file[0], s
        print "read {0} char(s) [saving]".format(len(data))
        if file[1] is True:
            file[0].close()


def showPorts():
    ports = list(serial.tools.list_ports.comports())
    if len(ports) <= 0:
        print "No serial ports, exit..."
        os._exit(0)
    else:
        print "Serial ports :"
        for port in ports:
            print "\t{0}".format(port)
        p = int(raw_input("\nchoose : ")) - 1
        if p > len(ports):
            print "Out of range, exit..."
            os._exit(0)
        port = str(ports[p])
        return (port.split(' '))[0]

if __name__ == '__main__':
    
    port = showPorts()

    print port
    
    kl = keyLintener(None)
    kl.start()
    try:
        mySerial = serial.Serial(port, 115200)
        print "listening [{0}]".format(port)
    except Exception, e:
        raise e
        print "cannot open serial! Please connect correctly"

    while True:
        get = mySerial.read(101)
        if ord(get[100]) is not 255:
            print ord(get[100]), 'fail'
            mySerial.flushInput()
        else:
            voltageOutput(get, kl.getFile())
        # os.system("cls")
