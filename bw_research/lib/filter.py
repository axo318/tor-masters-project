import numpy as np
from scipy.signal import butter, filtfilt

## Returns filtered data
def getFilteredSignal(data):
    # Filter requirements
    cutoff = 0.5    # Desired cutoff frequency of the filter, Hz
    fs = 3          # Sample rate, Hz
    order = 5       # sin wave can be approx represented as quadratic
    nyq = 0.5 * fs  # Nyquist Frequency

    return butter_lowpass_filter(data, cutoff, fs, order, nyq)

##
def butter_lowpass_filter(data, cutoff, fs, order, nyq):
    normal_cutoff = cutoff / nyq
    # Get the filter coefficients 
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y


