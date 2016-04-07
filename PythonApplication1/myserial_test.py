import serial
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
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            key = msvcrt.getch()
            if key == "q":
                print "Now quit..."
                os._exit(0)


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

def voltage(data):
    print (ord(data[0]) * 256 + ord(data[1]))
    pass


if __name__ == '__main__':
    kl = keyLintener()
    kl.start()

    try:
        mySerial = serial.Serial('COM12', 115200)
        print "listening [COM12]"
    except Exception, e:
        raise e
        print "cannot open serial! Please connect correctly"

    while True:
        get = mySerial.read(2)
        voltage(get)
        # os.system("cls")
