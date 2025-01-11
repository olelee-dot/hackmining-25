import correlations
import analysis

import pandas as pd

number_of_rows = 1000

ampel_data = pd.read_csv("/Users/mariemehlfeldt/Desktop/Hackmining-25/Hackathon_2024/Final_data_crusher_customer/crusher_data_for_analysis.csv", delimiter=";", nrows=number_of_rows)
ampel_data = ampel_data.filter(items=["timestamp", "115YL12013A"])
ampel_data['timestamp'] = pd.to_datetime(ampel_data['timestamp'])
ampel_data = ampel_data.rename(columns={"115YL12013A": "ampel_an_oder_aus"})

level_data = pd.read_excel("/Users/mariemehlfeldt/Desktop/Hackmining-25/Hackathon_2024/Final_data_crusher_every_second/September.xlsx", nrows=number_of_rows+1)
level_data = level_data.rename(columns={"Timestamp": "timestamp"})
level_data = level_data.drop([0])
level_data = level_data.filter(items=["timestamp", "115LIT12040A"])
level_data = level_data.rename(columns={"115LIT12040A": "level"})

dataframe = pd.merge(ampel_data, level_data, left_on='timestamp', right_on='timestamp', how='inner')

print (dataframe)

print (type(dataframe["ampel_an_oder_aus"]))
print (type(dataframe))
print (type(dataframe["level"]))

analysis.analysis_pit_lvl_data(dataframe)

dataframe_truck_loads = ...
correlations.correlations(dataframe, dataframe_truck_loads)