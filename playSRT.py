import time

class StringTime:
    def __init__(self):
        self.hour = 0
        self.minute = 0
        self.second = 0
        self.totalSecond = 0

    def getTotalSeconds(self):
        self.totalSecond = self.hour*60*60+self.minute*60 + self.second
        return self.totalSecond

    def changeStringToSecond(self,timeString):
        # input like this: 00:00:00,014
        # or usually xx:xx:xx,xxx
        # we need to change this into the seconds.
        if timeString.strip() == "":
            self.hour, self.minute,self.second = 0,0,0
        else:
            self.hour = int(timeString[0:2])
            self.minute = int(timeString[3:5])
            self.second = int(timeString[6:8])
            getPluseSecond = int(timeString[-3:])
            self.second  += int(getPluseSecond)*1.0/1000
    
#line = "00:00:02,460 --> 00:00:03,870"
class SRTPlayer:
    conFile = "configure.dat"
    LINE_LENGTH = 12
    # static information
    def __init__(self):
        self.stringTime = StringTime()
        self.sleepTime = 0
        self.currentTime = 0
        self.startTime = 0
        self.currentTimeLine = ""
        self.srtFile = "File/read.srt"

    def setSrtFile(self,name):
        self.srtFile = "File/"+name

    def getCurrentTime(self,line):
        self.stringTime.changeStringToSecond(line[:self.LINE_LENGTH])
        return self.stringTime.getTotalSeconds()

    def getGapTime(self,line):
        self.stringTime.changeStringToSecond(line[:self.LINE_LENGTH])
        startTime = self.stringTime.getTotalSeconds()
        self.stringTime.changeStringToSecond(line[-1*(self.LINE_LENGTH+1):])
        endTime = self.stringTime.getTotalSeconds()
        return endTime - startTime
        self.beginLine = 0

    def getStartTime(self):
        # set the self.startTime by seconds
        congLine = file(self.conFile,"r")
        self.beginLine = congLine.readline()[:self.LINE_LENGTH]
        self.stringTime.changeStringToSecond(self.beginLine)
        self.startTime = self.stringTime.getTotalSeconds()
        congLine.close()

    def showLine(self):
        # show line by line
        startTime = time.time()
        updated = True
        self.getStartTime()

        beginPrint = False
        for line in self.srtFile.readlines():
            if not beginPrint and line.find(self.beginLine) < 0: # ignore print
                print 'continue'
                continue
            if not beginPrint and line.find(self.beginLine) >= 0:
                print 'find'
                beginPrint = True

            while True:
                if line.find("-->") < 0: # not a time line, just print it
                    print line
                    break
                else:
                    # if is the time line, need wait the currentTime greater than the fileTime, then to nextLine
                    currentTime = time.time() - startTime + self.startTime
                    time.sleep(0.1)
                    fileTime = self.getCurrentTime(line)
                    self.currentTimeLine = line
                    if currentTime > fileTime:
                        print line
                        print '---------------'
                        print ' '
                        print ' ' 
                        break
                        # if the current time is less than file begin time, just continue the loop

    def play(self):
        try:
            self.showLine()
        except KeyboardInterrupt:
            print 'teminated at time :: %s '%self.currentTimeLine
        finally:
            confileFile = file(self.conFile,'w')
            confileFile.write(self.currentTimeLine)
            confileFile.close()

if __name__ == "__main__":
    import sys
    srtPlayer = SRTPlayer()
    if len(sys.argv)>0:
        if sys.argv[1] == '-0':
            print 'ito'
            conFile = open('configure.dat','w')
            conFile.write("")
            conFile.close()

        if len(sys.argv) == 3:
            srtPlayer.setSrtFile(sys.argv[2])

    conFile = open('configure.dat')
    print 'start at :: ',conFile.readline()
    for i in range(3):
        print 'start at %d seconds!'%(3-i)
        time.sleep(1)
    srtPlayer.play()

