from datetime import datetime

class Time:
    def __init__(self, string):
        self.string = string
        self.time = datetime.strptime(string, '%Y-%m-%d %H:%M:%S')
        self.t = self.getT(string)
        self.seconds = self.time.timestamp()
        
    def toString(self):
        return self.string
    
    def toSeconds(self):
        return self.seconds
    
    def getT(self, s):
        return datetime.strptime(s.split(' ')[1], '%H:%M:%S')