import pandas as pd
import json
import statistics

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
def calculateWindowInterval(times, sampling_period):
    '''
    Description:
        Takes the times and sampling period and calculates the maximum window interval which makes the variations valid
    '''
    size = len(times)
    if size < 2:
        return None
    
    # First convert sampling_period(seconds) into index_period(index)
    time_cycle = times[1] - times[0]
    index_period = sampling_period // time_cycle     # Here we convers seconds -> indexes   Eg. 20s -> 1 index
    
    # The window interval then becomes (index_period : size-index_period)
    return (index_period, size - index_period)


##
def getVariationSum(x1, x2, window_interval=None):
    if window_interval==None:
        m = 0
        n = -1
    else:
        m = window_interval[0]
        n = window_interval[1]
    
    # Get rid of offsets
    x1_off = list(x1[m:n])
    x2_off = list(x2[m:n])
    
    # Check bounds
    x1_size = len(x1_off)
    x2_size = len(x2_off)
    size = min(x1_size, x2_size)
    if(x1_size != x2_size):
        print("Dimensions of x1({}) and x2({}) are not equal. Defaulting to size of {}".format(x1_size, x2_size, size))
        
    # Get absolute differences
    total_variation = 0
    for i in range(size):
        total_variation += abs(x1_off[i] - x2_off[i])
    
    return total_variation


##
def getSampledVariation(data, times, sampling_period, window_interval=None, sampling_offset=0):
    '''
    Description:
        Takes the data, the timestamps, the sampling period(seconds) (and the valid window_interval)
        It samples the data given the sampling period (in seconds)
        
    INPUTS:
        data            : 1st set of data
        timestamps      : 2nd set of data
        sampling_period : Sampling interval (seconds)
        window_interval : the range of indexes which will be measured (tuple) (m,n) m<=n
        sampling_offset : offset for sampling method start

    RETURNS:
        variation : sum of all absolute differences between the two curves
    '''
    if window_interval==None:
        m = 0
        n = -1
    else:
        m = window_interval[0]
        n = window_interval[1]
    
    # Sample the data
    sampled_data = getSampledSignal(data, times, sampling_period, sampling_offset=sampling_offset)
    return getVariationSum(sampled_data, data, window_interval=window_interval)


##
def getVariationDistribution(data, times, sampling_period, window_interval=None):
    '''
    INPUTS:
        data            : data
        times           : times associated with the data
        sampling_period : Sampling interval (seconds)

    RETURNS:
        total_variation : A mean and std of variations across different offsets
    '''
    
    # Calculate window interval
    if window_interval==None:
        window_interval = calculateWindowInterval(times, sampling_period)
        print('Window interval was calculated as:',window_interval)
    
    # Calculate how many offsets we need to apply to cover all possible combinations for this sampling period
    # Here we assume each timing is equally spaced out
    (max_offset,_) = calculateWindowInterval(times, sampling_period)
    
    # Run the "getSampledVariation" for each of the sampling offsets
    variations = []
    for offset in range(max_offset):
        variations.append(getSampledVariation(data, times, sampling_period, window_interval=window_interval, sampling_offset=offset))
    
    return statistics.mean(variations), statistics.stdev(variations)