import sys
import os
from lib.control import Control
from lib.debug import Debug

# Vars
fp_list = 'fingerprints.txt'
ref_node = '99339F3E68BCCC1391BF14C821D80766FE0C5956'
DAY_CYCLE = 1


class Main(Debug):

    def run(self):
        args = sys.argv[1:]

        # Check inputs, if not correct set default values
        if len(args) != 3:
            args = []
            args.append('60') # x_time
            args.append('10') # n_samples
            args.append('5') # t_threads
            self.show('Invalid Inputs, going to defaults')
        else:
            self.show('Inputs Valid')

        # Read list
        f = open(fp_list, 'r')
        fps = [line[:-1] for line in f]

        # Run
        control = Control(args, fps, ref_node, day_cycle=DAY_CYCLE)
        control.run()


if __name__=='__main__':
    main = Main()
    try:
        main.run()
    except KeyboardInterrupt:
        print('FUCKOFF')
        exit(0)
