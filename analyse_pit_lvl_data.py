import numpy as np
import pandas as pd
from scipy.stats import shapiro
import matplotlib.pyplot as plt

def analyse_pit_lvl_data(list_of_objects):
	# function to analyse the data of the pit level
	# input: list of objects (class written by Ole and Lukas) with attributes describing the ascend and descend of the pit level
	# output: mean and std of feeder and crusher speed, check for normal distribution of feeder and crusher speed
    
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
    

