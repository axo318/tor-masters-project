import pandas as pd
import json

'''
Object specs:
    x          : Anchor relay (always the same)
    y          : Variable relay
    time_start : timestamp
    trials     : y,x,xy,rtt objects
    
Returns:
    DataFrame  : time, anchor, relay, rtt
'''
def getTingMeasurementsFromFile(file_path=''):
    # Check path
    if len(file_path) == 0: return None
    
    # Get name of file and use it as data
    file_date = file_path.split('/')[-1].split('.')[0]
    
    # Read file into lines
    lines = open(file_path).readlines()

    # Each line is a measurement. So place it in a JSON object
    objs = [json.loads(line.strip()) for line in lines]

    # Using the objects construct dataframe for each measurement
    # Each measurement has: time, anchor, relay, rtt
    df = pd.DataFrame()
    df['date'] = [file_date] * len(lines)
    df['time'] = [m['time_start'] for m in objs]
    df['anchor'] = [m['x']['fp'] for m in objs]
    df['relay'] = [m['y']['fp'] for m in objs]
    df['rtt'] = [m['trials'][0]['rtt'] for m in objs]
    
    return df