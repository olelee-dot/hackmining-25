import pandas as pd 
from scipy.signal import find_peaks
import numpy as np

def find_lin_section(Daten):
# function to subdivide a big continuous data set into smaller parts(from peak to peak, ergo one descending part and one ascending part)
# input: raw data of pit level (pandas dataframe)
# output: object (class written by Ole and Lukas) with the following attributes: 
#   start time absolute, turning point relative, end time relative, start value, turing point value, end value, slope of ascend, slope of descend
    data = Daten['Pit Level']
    traffic_light = Daten['Traffic Light']

    peaks, _ = find_peaks(data, height = 50, distance = 100) # peaks are the indices of the peaks in the data, minimum height, distance between peaks, prominence and width can be adjusted
    
    for i in range(len(peaks)-1):
        timestamp_first_peak = peaks[i]
        initial_fill_height = data[peaks[i]]
        minimum_fill_height = np.min (data[peaks[i]:peaks [i+1]])
        timestamp_min_fill = np.argmin (data[peaks[i]:peaks [i+1]])
        initial_feeder_speed = (minimum_fill_height - data[peaks[i]])/timestamp_min_fill
        seconds_to_final_peak = peaks [i+1] - timestamp_first_peak
        final_fill_height = data[peaks[i+1]]
        crusher_speed = (final_fill_height - minimum_fill_height)/(seconds_to_final_peak-timestamp_first_peak)

        seconds_to_green = None
        for i in range (seconds_to_final_peak): # find the first green light after the first peak
            if traffic_light(i) == 'red' and traffic_light (i+1) == 'green':
                seconds_to_green = i+1
                break
        
        if crusher_speed > 20 and initial_feeder_speed < 20: # filter so that only data with relevant crusher and feeder speeds are considered
            # however you want to name the object/object collection class and initialize it
            ObjectCollection.addObject (Peak_To_Peak(initial_fill_height, initial_feeder_speed, timestamp_first_peak, minimum_fill_height, seconds_to_green, seconds_to_final_peak, final_fill_height))
            ### additional properties can be added to the object here (like crusher speed)

