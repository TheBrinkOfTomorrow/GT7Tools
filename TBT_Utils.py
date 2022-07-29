import math

#print("This is my file to demonstrate best practices.")

class TBT_TimeFormatter:
    hours = 0
    minutes = 0
    seconds = 0
    thousandths = 0

    def __init__(self, milliSecondsIn):
        super(TBT_TimeFormatter, self).__init__()
        self.totalMilliSeconds = milliSecondsIn
        self.hours = math.floor( milliSecondsIn / ( 1000 * 60 *  60) ) 
        self.minutes = math.floor( ( milliSecondsIn / ( 1000 * 60 ) ) % 60 ) 
        self.seconds = math.floor( ( milliSecondsIn / 1000 ) % 60  )
        self.milliSeconds = math.floor(milliSecondsIn % 1000 )
        print(milliSecondsIn, self.hours, self.minutes, self.seconds, self.milliSeconds)
    
    def getHours(self):
        return self.hours
    def getMinutes(self):
        return self.minutes
    def getSeconds(self):
        return self.seconds
    def getMillis(self):
        return self.milliSeconds

def main():
    print('Hello')
    MILLIS_IN = 13515200
    testFormatter = TBT_TimeFormatter(MILLIS_IN)

    print('Millseconds: In', MILLIS_IN,';  Out: ', testFormatter.totalMilliSeconds)

if __name__ == "__main__":
    main()
