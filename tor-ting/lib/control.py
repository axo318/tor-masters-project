from .debug import Debug
from .nodeThread import NodeThread
from .node import Node

"""
INPUTS:
    Fingerprint list (list)
    Time to measure each node (minutes)
    Samples per measurement (int)
    Thread number (int)
"""

class Control(Debug):

    def __init__(self, args, fps, ref_node):
        self.ref_node = ref_node
        self.x_time = args[0]
        self.n_samples = int(args[1])
        self.t_threads = int(args[2])
        self.fps = fps
        self.nodes = [Node(fp=fp, ref_node=ref_node) for fp in self.fps]
        self.running = True

    ##
    def nodes_left(self, nodes_list):
        return (len(nodes_list) > 0)

    ##
    def all_threads_available(self, ts):
        for t in ts:
            if t.in_use:
                return False
        return True

    ##
    def run(self):
        # Initialize threads
        self.show("Control is starting")
        threads = [NodeThread(i) for i in range(self.t_threads)]

        # Logic vars
        remaining_nodes = self.nodes

        # LOOP
        while(self.running):
            # Check available threads
            for thread in threads:
                # If current thread not in use, and we have more nodes,
                # Pop and assign last node to current thread
                if( (not thread.in_use) and self.nodes_left(remaining_nodes)):
                    cur_node = remaining_nodes.pop(0)
                    self.show("Thread",str(thread.id),'not in use, so we assign it node',str(cur_node.fp))
                    thread.assignNode(cur_node)

            # If not more fps, terminate program
            if( (not self.nodes_left(remaining_nodes)) and self.all_threads_available(threads)):
                self.show('No more nodes left and all threads are finished')
                self.running=False

        # Loop exits
        self.show('Exiting ...')
        exit(0)
