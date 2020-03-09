from .debug import Debug
import threading
import time

class NodeThread(Debug):
    def __init__(self, id):
        self.id = id
        self.cur_node = None
        self.in_use = False
        self.t = None

    def assignNode(self, node):
        self.in_use = True
        self.t = threading.Thread(target=self.start, args=[])
        self.cur_node = node
        self.t.start()

    def start(self):
        self.show('Starting to measure Node:',str(self.cur_node.fp))
        self.cur_node.measure()
        self.show('Finished measuring Node:',str(self.cur_node.fp))
        self.in_use = False
