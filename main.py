import pandas as pd
import time
import datetime

class Bin_Parameter: 
    warning_minimum_height = 53.84
    warning_maximum_height = 76.92
    emergency_stop_minimum_height = 30.77
    emergency_stop_maximum_height = 87
    feederspeed_max = -2.05267 # Feeder speed in percent/second

    def feederspeed_real(self, feederspeed_custom): 
        return self.feederspeed_max*feederspeed_custom

class Peak_To_Peak:
    initial_fill_height = None
    initial_feeder_speed = None
    error_date = datetime.datetime.now()
    error_date = error_date.replace(minute=00, hour=00, second=00, year=1970, month=1, day=1)
    timestamp_first_peak = error_date
    minimum_fill_height = None
    seconds_to_green = None
    seconds_to_final_peak = None
    final_fill_height = None
    bin_parameter = Bin_Parameter()

    # new attributes
    crusher_speed = None
    AUC = None
    timestamp_min_fill = None
    Score = None
    Crusher_Pressure = None
    Crusher_Power = None

    def __init__(self, timestamp_first_peak, initial_fill_height, initial_feeder_speed, 
                 minimum_fill_height, seconds_to_green, seconds_to_final_peak, 
                 final_fill_height, bin_parameter): 
                 self.initial_fill_height = initial_fill_height
                 self.initial_feeder_speed_pct = initial_feeder_speed
                 self.timestamp_first_peak = timestamp_first_peak
                 self.minimum_fill_height = minimum_fill_height
                 self.seconds_to_green = seconds_to_green
                 self.seconds_to_final_peak = seconds_to_final_peak
                 self.final_fill_height = final_fill_height
                 self.bin_parameter = bin_parameter
    
    def seconds_to_minimum(self):
        return (self.minimum_fill_height-self.initial_fill_height)/self.bin_parameter.feederspeed_real(self.initial_feeder_speed_pct)
   
    def set_crusher_speed(self, crusher_speed):
        self.crusher_speed = crusher_speed
    
    def set_AUC(self, AUC):
        self.AUC = AUC
    
    def set_seconds_to_minfill(self, timestamp_min_fill):
        self.timestamp_min_fill = timestamp_min_fill

    def set_crusher_pressure(self, Crusher_Pressure):
        self.Crusher_Pressure = Crusher_Pressure
    
    def set_crusher_power(self, Crusher_Power):
        self.Crusher_Power = Crusher_Power

    def calculate_score (self):
        warn_max = self.bin_parameter.warning_maximum_height
        warn_min = self.bin_parameter.warning_minimum_height
        emerg_max = self.bin_parameter.emergency_stop_maximum_height
        emerg_min = self.bin_parameter.emergency_stop_minimum_height
        Score = 0
        if self.minimum_fill_height < warn_min:
            Score = Score + 1
        if self.minimum_fill_height < emerg_min:
            Score = Score + 3
        if self.initial_fill_height > warn_max:
            Score = Score + 1
        if self.initial_fill_height > emerg_max:
            Score = Score + 3
        if self.final_fill_height > warn_max:
            Score = Score + 1
        if self.final_fill_height > emerg_max:
            Score = Score + 3
        self.Score = Score

king_bin = Bin_Parameter()
dt = datetime.datetime.now()
p2p_object = Peak_To_Peak(dt, 70, 0.65, 60, 60, 120, 70, king_bin)
print(p2p_object.seconds_to_minimum())