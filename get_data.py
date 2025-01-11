import pandas as pd

number_of_rows = 1000

ampel_data = pd.read_csv("Final_data_crusher_customer/crusher_data_for_analysis.csv", delimiter=";", nrows=number_of_rows)
ampel_data = ampel_data.filter(items=["timestamp", "115YL12013A"])
ampel_data['timestamp'] = pd.to_datetime(ampel_data['timestamp'])
ampel_data = ampel_data.rename(columns={"115YL12013A": "ampel_an_oder_aus"})

level_data = pd.read_excel("Final_data_crusher_every_second/September.xlsx", nrows=number_of_rows+1)
level_data = level_data.rename(columns={"Timestamp": "timestamp"})
level_data = level_data.drop([0])
level_data = level_data.filter(items=["timestamp", "115LIT12040A"])
level_data = level_data.rename(columns={"115LIT12040A": "level"})

final_data = pd.merge(ampel_data, level_data, left_on='timestamp', right_on='timestamp', how='inner')
