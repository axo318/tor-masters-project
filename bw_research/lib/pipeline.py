import os
import pandas as pd

from .utils import DATE, TIME, ANCHOR, RELAY, RTT, DATETIME
from .ting_utils import calculateWindowInterval, getVariationDistribution
from .my_time import Time


## Class for outputing completion messages
class UserMsg:
    def log(self, *msg):
        name = str(self.__class__.__name__)
        n = '['+name+']:'
        print(n,*msg)


## Main class for test performing
class Pipeline(UserMsg):
    def __init__(self, path='.', file_limit=999):
        self.file_limit = file_limit
        self.path       = path
        self.files      = [f for f in os.listdir(path) if '.csv' in f]
    
    ## This executes the parsing and measurements of the specified files with the given rate list
    def run(self, sampling_period_list):
        self.holders = self.buildHolders(sampling_period_list)
        if len(self.holders) == 0: return
        
        # Calculate window interval using:
        #  -> Maximum sampling rate
        #  -> Shorter time interval
        max_sample = max(sampling_period_list)
        short_holder = self.getShortestTimeHolder()
        window_interval = calculateWindowInterval(short_holder.times, max_sample)
        self.log('Shortest time duration was found to be:',short_holder.duration,'for relay:',short_holder.relay)
        self.log('Window interval was calculated as:',window_interval,'seconds,',window_interval/60,'minutes')
        
        # Run tests
        self.log('Starting tests ...')
        for holder in self.holders:
            HolderTester(holder).runTests(window_interval)
        
    # Make holders
    def buildHolders(self, sampling_period_list):
        holders = []
        i = 0
        while(i < self.file_limit):
            file = self.files[i]
            holders.append(DataHolder(self.path + file, sampling_period_list))
            self.log('File:',file,'was parsed.')
            i += 1
        return holders
    
    # Picks the time data with the shortest duration
    def getShortestTimeHolder(self):
        h = self.holders[0]
        if len(self.holders) > 1:
            for holder in self.holders[1:]:
                if holder.duration < h.duration:
                    h = holder
        return h
    
    ## This will return the information currently saved in the data in readable format
    def printResults(self):
        for holder in self.holders:
            holder.printResults()
        
    
    
class DataHolder(UserMsg):
    def __init__(self, path, sampling_period_list):
        self.df       = pd.read_csv(path)
        self.relay    = self.df[RELAY][0]
        self.data     = self.df[RTT]
        self.times    = self.df[DATETIME]
        self.duration = Time(list(self.times)[-1]).toSeconds() - Time(list(self.times)[0]).toSeconds()
        self.sampling_period_list = sampling_period_list
        
    def saveResults(self, results):
        self.results = results
        
    def printResults(self):
        print('Relay:',self.relay)
        for i,period in enumerate(self.sampling_period_list):
            print('Sampling Period (minutes):',period/60,' Variance,Std =',self.results[i])
        print()
    
    def graph(self):
        pass
        

## Class that has responsibility for running tests and saving results in holder object
class HolderTester(UserMsg):
    def __init__(self, holder):
        self.holder = holder
        
    def runTests(self, window_interval):
        results = []
        h = self.holder
        for s_period in h.sampling_period_list:
            mean, std = getVariationDistribution(h.data, h.times, s_period, window_interval=window_interval)
            results.append((mean,std))
        h.saveResults(results)