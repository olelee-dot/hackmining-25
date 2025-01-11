import correlations
import analysis
import os
import pandas as pd

data_path = os.path.join(os.path.dirname(__file__), "original_data")    # wenn alle dateien in origial_data sind
#path = os.path.join(data_path, filename)

number_of_rows = 100000000

ampel_data = pd.read_csv(os.path.join(data_path, "crusher_data_for_analysis.csv"), delimiter=";", nrows=number_of_rows)
ampel_data = ampel_data.filter(items=["timestamp", "115YL12013A"])
ampel_data['timestamp'] = pd.to_datetime(ampel_data['timestamp'])
ampel_data = ampel_data.rename(columns={"115YL12013A": "ampel_an_oder_aus"})

level_data = pd.read_excel(os.path.join(data_path, "September.xlsx"), nrows=number_of_rows+1)
level_data = level_data.rename(columns={"Timestamp": "timestamp"})
level_data = level_data.drop([0])
level_data = level_data.filter(items=["timestamp", "115LIT12040A"])
level_data = level_data.rename(columns={"115LIT12040A": "level"})

dataframe = pd.merge(ampel_data, level_data, left_on='timestamp', right_on='timestamp', how='inner')

print ('start of analysis of pit lvl')
analysis.analysis_pit_lvl_data(dataframe)
print ('analysis of pit lvl completed')

# print ('start of analysis of truck loads')
# dataframe_truck_loads = ...
# correlations.correlations(dataframe, dataframe_truck_loads)