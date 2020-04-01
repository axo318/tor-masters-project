from datetime import datetime

class Time:
    def __init__(self, string):
        self.string = string
        self.time = datetime.strptime(string, '%Y-%m-%d %H:%M:%S')
        self.seconds = self.time.timestamp()
        
    def toString(self):
        return self.string
    
    def toSeconds(self):
        return self.seconds