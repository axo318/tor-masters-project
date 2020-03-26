import pandas as pd
from .utils import DATE, TIME, ANCHOR, RELAY, RTT


## CLASS MyFrame
class MyFrame:
    def __init__(self, path_to_csv):
        self.df = pd.read_csv(path_to_csv)
    
    def getRelayData(self, relay):
        df = self.df
        return df[df[RELAY] == relay].reset_index(drop=True)
    
    def getRelays(self):
        return self.df[RELAY].unique()
    
#     def getRelaySession(self, relay):
#         pass
    

## CLASS Session
class Session:
    def __init__(self, relay, start, end):
        self.relay = relay
        self.start = start
        self.end = end
        

## CLASS SessionMaker
class SessionMaker:
    def __init__(self, myFrame, session_timeout=1200):    #Timeout default = 1200 seconds = 20 minutes
        self.sessions = self.process(myFrame)
    
    def getSessions(self):
        return self.sessions
    
    def process(self, myFrame):
        relays = myFrame.getRelays()
        sessions = []
        
        for r in relays:
            df_r = myFrame.getRelayData()
            sessions += self.getRelaySessions(df_r)
        
        return sessions
    
    def getRelaySessions(self, df):
        sessions = []
        time_holder = df.iloc[0][TIME]