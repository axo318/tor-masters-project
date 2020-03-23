import pandas as pd
import json

##
def getTingMeasurementsFromFile(file_path=''):
    '''
    INPUTS:
        x          : Anchor relay (always the same)
        y          : Variable relay
        time_start : timestamp
        trials     : y,x,xy,rtt objects

    RETURNS:
        DataFrame  : time, anchor, relay, rtt
    '''
    
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


##
def getSampledSignal(signal_y, time_x, sampling_period, sampling_offset=0):
    '''
    INPUTS:
        signal_y        : Signal values
        time_x          : Timestamp for measurements (seconds)
        sampling_period : Sampling interval (seconds)
        sampling_offset : Offset for first sample

    RETURNS:
        sampled_signal  : list containing the sampled data
    '''
    
    # Check dimensions
    if len(signal_y) != len(time_x):
        print('signal_y({}) and time_x({}) do not have similar dimensions'.format(len(signal_y), len(time_x)))
        return []
    
    # Initialize variables we need to keep track
    i              = sampling_offset        # current index
    current_sample = signal_y[i]            # current sample value
    t              = time_x[i]              # current time
    next_t         = t + sampling_period    # time of next sample
    sampled_signal = [0] * sampling_offset  # list which will hold sampled data
    
    # Iterate through datapoints in signal_y
    while(i < len(signal_y)):
        t = time_x[i]
        # If current time has passed the timeframe, update next_t, current_sample
        if t >= next_t:
            next_t += sampling_period
            current_sample = signal_y[i]
        
        # Add current sample value to sampled_signal list, and update variables
        sampled_signal.append(current_sample)
        i += 1
    
    return sampled_signal


##
def getTotalVariation(x1, x2, offset=0):
    '''
    INPUTS:
        x1              : 1st set of data
        x2              : 2nd set of data
        offset          : index from which the operation will start

    RETURNS:
        total_variation : list containing the sampled data
    '''
    
    # Get rid of offsets
    x1_ = x1[offset:]
    x2_ = x2[offset:]
    
    # Check bounds
    x1_size = len(x1_)
    x2_size = len(x2_)
    size = min(x1_size, x2_size)
    
    if(x1_size != x2_size):
        print("Dimensions of x1({}) and x2({}) are not equal. Defaulting to size of {}".format(x1_size, x2_size, size))
        
    # Get absolute differences
    total_variation = 0
    for i in range(size):
        total_variation += abs(x1_[i] - x2_[i])
    
    return total_variation