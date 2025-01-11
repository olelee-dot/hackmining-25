import numpy as np
from scipy.stats import shapiro
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import random
from main import Bin_Parameter, Peak_To_Peak

# To do: adjust height, distance, prominence and width in find_peaks function AND min crusher speed and max feeder speed to to fit the data and limit artifacts 
def find_lin_section(data_frame):
# function to subdivide a big continuous data set into smaller parts(from peak to peak, ergo one descending part and one ascending part)
# input: raw data of pit level (pandas dataframe)
# output: object (class written by Ole and Lukas) with attributes describing the ascend and descend of the pit level
    data = data_frame['level']
    traffic_light = data_frame['ampel_an_oder_aus']

    peaks, _ = find_peaks(data, prominence=1) # peaks are the indices of the peaks in the data, minimum height, distance between peaks, prominence and width can be adjusted
    
    # initialize empty list for Peak_To_Peak objects
    Peak_To_Peak_list = []
    king_bin = Bin_Parameter() # initialize the bin parameter object

    for i in range(len(peaks)-1):
        timestamp_first_peak = data_frame['timestamp'][peaks[i]] # absolute timestamp of the first peak
        seconds_to_final_peak = data_frame['timestamp'][peaks[i+1]] - timestamp_first_peak # relative time between start and end of segment
        Index_min_fill = np.argmin (data[peaks[i]:peaks [i+1]]) # index of the minimum fill height
        seconds_to_min_fill = data_frame['timestamp'][Index_min_fill] - timestamp_first_peak # relative time between start of segment and minimum fill height

        initial_fill_height = data[peaks[i]]
        final_fill_height = data[peaks[i+1]]
        minimum_fill_height = np.min (data[peaks[i]:peaks [i+1]])

        initial_feeder_speed = (minimum_fill_height - data[peaks[i]])/seconds_to_min_fill.total_seconds()
        
        # crusher_speed is corrected for the initial_feeder_speed under the assumption that the crusher speed is constant for this segment
        crusher_speed = (final_fill_height - minimum_fill_height)/seconds_to_final_peak.total_seconds() - initial_feeder_speed
        AUC_crusher = (minimum_fill_height + final_fill_height) * 0.5 * (seconds_to_final_peak.total_seconds() - seconds_to_min_fill.total_seconds())

        seconds_to_green = None
        for j in range(peaks [i], peaks [i+1]): # find the first green light after the first peak
            if traffic_light[j] == 0 and traffic_light[j + 1] == 1:
                seconds_to_green = data_frame['timestamp'][j] - timestamp_first_peak # relative time between start of segment and green light
                break
        
        # if crusher_speed > 0 and initial_feeder_speed < 0: # filter so that only data with relevant crusher and feeder speeds are considered
        peak_to_peak_object = Peak_To_Peak(timestamp_first_peak, initial_fill_height, initial_feeder_speed, minimum_fill_height, seconds_to_green, seconds_to_final_peak, final_fill_height, king_bin)
        peak_to_peak_object.set_crusher_speed (crusher_speed)
        peak_to_peak_object.set_AUC (AUC_crusher)
        peak_to_peak_object.set_seconds_to_minfill (seconds_to_min_fill)
        Peak_To_Peak_list.append (peak_to_peak_object)
        ### additional properties can be added to the object here (like crusher speed and corrected crusher speed)

        if i < 10:
            print(f'---------------------------------------------------')
            print(f'Peak_To_Peak object created with the following attributes:')
            print(f'Timestamp of first peak: {timestamp_first_peak}')
            print(f'Initial fill height: {initial_fill_height}')
            print(f'Initial feeder speed: {initial_feeder_speed}')
            print(f'Minimum fill height: {minimum_fill_height}')
            print(f'Seconds to min fill: {seconds_to_min_fill}')
            print(f'Seconds to final peak: {seconds_to_final_peak}')
            print(f'Final fill height: {final_fill_height}')
            print(f'Crusher speed: {crusher_speed}')
            print(f'AUC of crusher: {AUC_crusher}')
            print(f'Seconds to green light: {seconds_to_green}')
            print(f'Seconds to final peak: {seconds_to_final_peak}')
            print(f'King bin: {king_bin}')
            print(f'---------------------------------------------------')

            # plot the data of this segment
            plt.plot(data_frame['timestamp'][peaks[i]:peaks[i+1]], data[peaks[i]:peaks[i+1]])
            # plt.plot([timestamp_first_peak, timestamp_first_peak + seconds_to_min_fill, timestamp_first_peak + seconds_to_final_peak], [data[timestamp_first_peak], data[timestamp_first_peak + seconds_to_min_fill], data[timestamp_first_peak + seconds_to_final_peak]], 'ro')
            plt.xlabel('Timestamp')
            plt.ylabel('Fill Height')
            plt.title(f'Segment from Peak {i} to Peak {i+1}')
            plt.show()  # Display the plot for the current segment

    print ('A list of Peak_To_Peak objects has been created with', len (Peak_To_Peak_list), 'objects')
    return Peak_To_Peak_list


def analysis_pit_lvl_data(dataframe_pit_level):
	# function to analyse the data of the pit level
	# input: list of objects (class written by Ole and Lukas) with attributes describing the ascend and descend of the pit level
	# output: mean and std of feeder and crusher speed, check for normal distribution of feeder and crusher speed
    
    list_of_objects = find_lin_section (dataframe_pit_level)

    # initialize empty lists
    list_of_feeder_speeds = [] 
    list_of_crusher_speeds = []

    for i in range (len(list_of_objects)):
        if list_of_objects[i].initial_feeder_speed is not None:
            list_of_feeder_speeds.append(list_of_objects[i].initial_feeder_speed)
        if list_of_objects[i].crusher_speed is not None:
            list_of_crusher_speeds.append(list_of_objects[i].crusher_speed)

    # calculate mean and std of feeder and crusher speed    
    mean_feeder_speed = np.mean(list_of_feeder_speeds)
    std_feeder_speed = np.std(list_of_feeder_speeds)
    mean_crusher_speed = np.mean(list_of_crusher_speeds)
    std_crusher_speed = np.std(list_of_crusher_speeds)
    
    # check for normal distribution of feeder and crusher speed using the Shapiro-Wilk test
    shapiro_stat_feeder, shapiro_p_feeder = shapiro(list_of_feeder_speeds)
    shapiro_stat_crusher, shapiro_p_crusher = shapiro(list_of_crusher_speeds)

    print ("Mean of feeder speed:", mean_feeder_speed)
    print ("Standard deviation of feeder speed:", std_feeder_speed)
    if shapiro_p_feeder > 0.05:
        print ("Feeder speed is normally distributed")
    else:
        print ("Feeder speed is not normally distributed")
    print ("Mean of crusher speed:", mean_crusher_speed)
    print ("Standard deviation of crusher speed:", std_crusher_speed)
    if shapiro_p_crusher > 0.05:
        print ("Crusher speed is normally distributed")
    else:
        print ("Crusher speed is not normally distributed")

    # plot histogram of feeder and crusher speed
    fig, axs = plt.subplots(2)
    axs[0].hist(list_of_feeder_speeds, bins = 50)
    axs[0].set_title('Feeder Speed')
    axs[1].hist(list_of_crusher_speeds, bins = 50)
    axs[1].set_title('Crusher Speed')
    plt.show()
    

