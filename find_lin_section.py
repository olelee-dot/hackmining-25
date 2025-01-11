import pandas as pd 
from scipy.signal import find_peaks
import numpy as np
from main import Peak_To_Peak

# To do: adjust height, distance, prominence and width in find_peaks function AND min crusher speed and max feeder speed to to fit the data and limit artifacts 

def find_lin_section(data_frame):
# function to subdivide a big continuous data set into smaller parts(from peak to peak, ergo one descending part and one ascending part)
# input: raw data of pit level (pandas dataframe)
# output: object (class written by Ole and Lukas) with attributes describing the ascend and descend of the pit level
    data = data_frame['Pit Level'] # adjust to actual column name
    traffic_light = data_frame['Traffic Light'] # adjust to actual column name

    peaks, _ = find_peaks(data, height = 50, distance = 100) # peaks are the indices of the peaks in the data, minimum height, distance between peaks, prominence and width can be adjusted
    
    # initialize empty list for Peak_To_Peak objects
    Peak_To_Peak_list = []

    for i in range(len(peaks)-1):
        timestamp_first_peak = peaks[i] # absolute timestamp of the first peak
        initial_fill_height = data[peaks[i]]
        minimum_fill_height = np.min (data[peaks[i]:peaks [i+1]])
        timestamp_min_fill = np.argmin (data[peaks[i]:peaks [i+1]]) # relative timestamp of the minimum fill height
        initial_feeder_speed = (minimum_fill_height - data[peaks[i]])/timestamp_min_fill
        seconds_to_final_peak = peaks [i+1] - timestamp_first_peak # relative time between start and end of segment
        final_fill_height = data[peaks[i+1]]
        # crusher_speed is corrected for the initial_feeder_speed under the assumption that the crusher speed is constant for this segment
        crusher_speed = (final_fill_height - minimum_fill_height)/(seconds_to_final_peak-timestamp_first_peak) - initial_feeder_speed
        AUC_crusher = (minimum_fill_height + final_fill_height) * 0.5 * (seconds_to_final_peak - timestamp_min_fill)

        seconds_to_green = None
        for i in range (seconds_to_final_peak): # find the first green light after the first peak
            if traffic_light(i) == 'red' and traffic_light (i+1) == 'green':
                seconds_to_green = i+1
                break
        
        if crusher_speed > -20 and initial_feeder_speed < 20: # filter so that only data with relevant crusher and feeder speeds are considered
            # however you want to name the object/object collection class and initialize it
            Peak_to_Peak_object = Peak_To_Peak(initial_fill_height, initial_feeder_speed, timestamp_first_peak, minimum_fill_height, seconds_to_green, seconds_to_final_peak, final_fill_height)
            Peak_to_Peak_object.crusher_speed = crusher_speed
            Peak_to_Peak_object.AUC = AUC_crusher
            Peak_to_Peak_object.timestamp_min_fill = timestamp_min_fill
            Peak_To_Peak_list.append (Peak_to_Peak_object)
            ### additional properties can be added to the object here (like crusher speed and corrected crusher speed)

        return Peak_To_Peak_list
