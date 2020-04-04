import pandas as pd
import json
import statistics
import math

from .my_time import Time
from .utils import DATE, TIME, ANCHOR, RELAY, RTT, DATETIME

## Public method
def getTingMeasurementsFromFile(file_path=''):
    '''
    INPUTS:
        file_path  : string with the full path name to be parsed (JSON)

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
    df[DATE] = [file_date] * len(lines)
    df[TIME] = [m['time_start'] for m in objs]
    df[ANCHOR] = [m['x']['fp'] for m in objs]
    df[RELAY] = [m['y']['fp'] for m in objs]
    df[RTT] = [m['trials'][0]['rtt'] if len(m['trials'])>0 else None for m in objs]
    
    return df


## Public method
def calculateWindowInterval(times, sampling_period):
    '''
    Description:
        Takes the times and sampling period and calculates the maximum window interval which makes the variations valid
    '''
    times = list(times)
    size = len(times)
    if size < 2:
        return None
    
    # First calculate lenght of current session
    begin = Time(times[0]).toSeconds()
    end   = Time(times[-1]).toSeconds()

    # Find the limits of the valid interval, and thus calculate it
    # Var valid represents max duration that can be measured
    low   = begin + sampling_period
    high  = end   - sampling_period
    valid = high  - low

    return valid


## Public method
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
        print('Window interval was calculated as:', window_interval, 'seconds')
    
    # Calculate how many offsets we need to apply to cover all possible combinations for this sampling period
    index_window = calculateIndexLimits(times, window_interval)
    low_index = index_window[0]
    
    # Run the "getSampledVariation" for each of the sampling offsets
    variations = []
    for offset in range(low_index):
        variations.append(getSampledVariation(data, times, sampling_period, index_window, sampling_offset=offset))
    
    # Returning standard deviation
    return statistics.mean(variations), statistics.stdev(variations)
    # Returning standard error
    #return statistics.mean(variations), statistics.stdev(variations) / math.sqrt(len(variations))


#######################
### PRIVATE METHODS ###
#######################

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
def calculateIndexLimits(times, window_interval):
    '''
    Description:
        Takes the times and valid interval and calculates the number of data points before the valid interval
    '''
    times = list(times)
    # Calculate the offset in seconds
    begin  = Time(times[0]).toSeconds()
    end    = Time(times[-1]).toSeconds()
    length = end - begin
    diff   = length - window_interval
    offset_seconds = diff // 2
    
    # Convert offset to index
    low_index = 0
    high_index = len(times) - 1
    
    while(1):
        cur_time = Time(times[low_index]).toSeconds()
        if (cur_time-begin > offset_seconds): break
        low_index += 1
    
    while(1):
        cur_time = Time(times[high_index]).toSeconds()
        if (end-cur_time > offset_seconds): break
        high_index -= 1
    
    if low_index > high_index:
        return 0, 0
    
    return (low_index, high_index)
            

##
def getVariationSum(x1, x2):
    x1 = list(x1)
    x2 = list(x2)
    # Check bounds
    x1_size = len(x1)
    x2_size = len(x2)
    size = min(x1_size, x2_size)
    if(x1_size != x2_size):
        print("Dimensions of x1({}) and x2({}) are not equal. Defaulting to size of {}".format(x1_size, x2_size, size))
        
    # Get absolute differences
    total_variation = 0
    for i in range(size):
        total_variation += abs(x1[i] - x2[i])
    
    return total_variation


##
def getSampledVariation(data, times, sampling_period, index_window, sampling_offset=0):
    '''
    Description:
        Takes the data, the timestamps, the sampling period(seconds) (and the valid window_interval)
        It samples the data given the sampling period (in seconds)
        
    INPUTS:
        data            : 1st set of data
        timestamps      : 2nd set of data
        sampling_period : Sampling interval (seconds)
        index_window    : the range of indexes which will be measured (tuple) (m,n) m<=n
        sampling_offset : offset for sampling method start

    RETURNS:
        variation : sum of all absolute differences between the two curves
    '''
    # Sample the data
    times_seconds = [Time(t).toSeconds() for t in times]
    sampled_data = getSampledSignal(data, times_seconds, sampling_period, sampling_offset=sampling_offset)
    
    # Feed the correct data window into the sum calculator and return
    l = index_window[0]
    h = index_window[1] + 1
    return getVariationSum(sampled_data[l:h], data[l:h])


