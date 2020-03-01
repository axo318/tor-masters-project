import os
from .debug import Debug

COMMAND = 'cd ~/ting; /home/pi/ting/ting '

class Node(Debug):

    def __init__(self, fp=None, ref_node=None):
        self.fp = str(fp)
        self.ref_node = ref_node

    def setFP(self, fp):
        self.fp = fp

    def execMeasurement(self):
        self.show('Measurement for',str(self.fp),'is being performed...')
        for i in range(3):
            os.system(COMMAND+ self.ref_node +' '+ self.fp)
