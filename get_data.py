import pandas as pd
from glob import glob


#number_of_rows = 1000

#all_excel_files = glob("Final_data_crusher_every_second/*.xlsx")
#level_data = pd.concat(pd.read_excel(excel_file, skiprows=[0], usecols=["Timestamp", "115LIT12040A"]) for excel_file in all_excel_files)
level_data = pd.read_excel("Final_data_crusher_every_second/September.xlsx")
level_data = level_data.drop([0])
level_data = level_data.filter(items=["Timestamp", "115LIT12040A"])
level_data['Timestamp'] = pd.to_datetime(level_data['Timestamp'])
level_data = level_data.rename(columns={"Timestamp": "timestamp"})
level_data = level_data.rename(columns={"115LIT12040A": "level"})

ampel_data = pd.read_csv("Final_data_crusher_customer/crusher_data_for_analysis.csv", delimiter=";", nrows=len(level_data))
ampel_data = ampel_data.filter(items=["timestamp", "115YL12013A"])
ampel_data['timestamp'] = pd.to_datetime(ampel_data['timestamp'])
ampel_data = ampel_data.rename(columns={"115YL12013A": "ampel_an_oder_aus"})





september_data_2 = pd.merge(ampel_data, level_data, left_on='timestamp', right_on='timestamp', how='inner')

september_data_2.to_csv("september_data_2.csv", sep=";", index=False)
