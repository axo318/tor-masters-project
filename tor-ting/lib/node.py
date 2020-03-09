import os
from .debug import Debug
import time

COMMAND = 'cd ~/ting; /home/pi/ting/ting '

class Node(Debug):

    def __init__(self, ref_node=None, fp=None, **kwargs):
        self.ref_node = ref_node
        self.fp = str(fp)
        self.x_time = kwargs.get('x_time')
        self.cycle = kwargs.get('cycle', 1)

    def curTime(self):
        return int(round(time.time() * 1000))

    def measure(self):
        # Get milliseconds time
        initial_time = self.curTime()

        while(self.curTime() < initial_time + x_time*60000):
            self.show('Current time is less than',initial_time)
            self.execMeasurement()

    def execMeasurement(self):
        self.show(self.curTime(),'Measurement for',str(self.fp),'is being performed...')
        os.system(COMMAND+ self.ref_node +' '+ self.fp)
