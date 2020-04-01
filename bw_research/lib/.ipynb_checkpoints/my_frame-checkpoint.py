import pandas as pd
from .my_time import Time
from .utils import DATE, TIME, ANCHOR, RELAY, RTT, DATETIME


## CLASS MyFrame
class MyFrame:
    def __init__(self, path_to_csv):
        self.df = pd.read_csv(path_to_csv)
        self.processTime()
    
    def getRelayData(self, relay):
        df = self.df
        return df[df[RELAY] == relay].reset_index(drop=True)
    
    def getRelays(self):
        return self.df[RELAY].unique()
    
    def processTime(self):
        self.df[DATETIME] = self.df[DATE] + " " + self.df[TIME]
        
    def getSessions(self):
        return SessionMaker(self).getSessions()
            

## CLASS Session
class Session:
    def __init__(self, relay, start, end):
        self.relay = relay
        self.start = start
        self.end = end
    
    def setData(self, df):
        self.data = df
        
    def getData(self):
        return self.data
    
    def __len__(self):
         return self.data.shape[0]
        

## CLASS SessionMaker
class SessionMaker:
    def __init__(self, myFrame, session_timeout=1200):    #Timeout default = 1200 seconds = 20 minutes
        self.timeout = session_timeout
        self.sessions = self.process(myFrame)
    
    def getSessions(self):
        return self.sessions
    
    def process(self, myFrame):
        relays = myFrame.getRelays()
        sessions = []
        
        for r in relays:
            df_r = myFrame.getRelayData(r)
            sessions += self.getRelaySessions(df_r)
        
        return sessions
    
    def timePassed(self, current_time, previous_time):# Time format: "31/12/2020 23:59:59
        cur_secs = Time(current_time).toSeconds()
        prev_secs = Time(previous_time).toSeconds()
#         cur_secs = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S').timestamp()
#         prev_secs = datetime.strptime(previous_time, '%Y-%m-%d %H:%M:%S').timestamp()
        return cur_secs - prev_secs > self.timeout
    
    def getRelaySessions(self, df):
        sessions = []
        relay = df.iloc[0][RELAY]
        cur_time = prev_time = start_time = df.iloc[0][DATETIME]
        start_ind = 0
        i = 0
        
        while(i < df.shape[0]):
            cur_time = df.iloc[i][DATETIME]
            
            # More than 20 mins from previous measurement
            if(self.timePassed(cur_time, prev_time)):             
                # Create Session object and update variables
                cur_session = Session(relay, start_time, prev_time)
                cur_session.setData(df.iloc[start_ind:i])
                sessions.append(cur_session)
                start_time = df.iloc[i][DATETIME]
                start_ind = i
                
            elif(i == df.shape[0]-1):
                cur_session = Session(relay, start_time, prev_time)
                cur_session.setData(df.iloc[start_ind:i])
                sessions.append(cur_session)
            
            prev_time = df.iloc[i][DATETIME]
            i+=1
            
        return sessions