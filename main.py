import pandas as pd
import time
import datetime

class Bin_Parameter: 
    warning_minimum_height = 53.84
    warning_maximum_height = 76.92
    emergency_stop_minimum_height = 30.77
    emergency_stop_maximum_height = 87
    feederspeed_max = -2.05267           # Feeder speed in percent/second

    def get_feederspeed(self):
        return self.feederspeed_max

class Peak_To_Peak: 
    initial_fill_height = -1
    initial_feeder_speed = -1
    error_date = datetime.datetime.now()
    error_date = error_date.replace(minute=00, hour=00, second=00, year=1970, month=1, day=1)
    timestamp_first_peak = error_date
    minimum_fill_height = -1
    seconds_to_green = -1
    seconds_to_final_peak = -1
    final_fill_height = -1
    bin_parameter = Bin_Parameter()

    def __init__(self, timestamp_first_peak, initial_fill_height, initial_feeder_speed, 
                 minimum_fill_heigt, seconds_to_green, seconds_to_final_peak, 
                 final_fill_height, bin_parameter): 
                 self.initial_fill_height = initial_fill_height
                 self.initial_feeder_speed = initial_feeder_speed
                 self.timestamp_first_peak = timestamp_first_peak
                 self.minimum_fill_height = minimum_fill_heigt
                 self.seconds_to_green = seconds_to_green
                 self.seconds_to_final_peak = seconds_to_final_peak
                 self.final_fill_height = final_fill_height
                 self.bin_parameter = bin_parameter
    
    def seconds_to_minimum(self):
        return ((self.minimum_fill_height-self.initial_fill_height)/
                (self.initial_feeder_speed*self.bin_parameter.get_feederspeed()))

king_bin = Bin_Parameter()
dt = datetime.datetime.now()
p2p_object = Peak_To_Peak(dt, 70, 0.65, 60, 60, 120, 70, king_bin)
print(p2p_object.seconds_to_minimum())