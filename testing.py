import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import analysis

data_path = os.path.join(os.path.dirname(__file__), "original_data")
output_path = os.path.join(os.path.dirname(__file__), "prepaired_data")

def read_df(filename: str, size=1000):
    if filename.endswith("xlsx"):
        file = pd.read_excel(os.path.join(data_path, filename), nrows=size)
    elif filename.endswith("csv"):
        file = pd.read_csv(os.path.join(data_path, filename), delimiter=";",nrows=size)
    return file

def store_df(filename:str, df):
    df.to_csv(os.path.join(output_path, filename), index=False)

def make_disp_smaller(df: pd.DataFrame):
    res = df[df["Destination"] == "CS03"]
    selected_columns = res[["Origin","Truck Discharge Date","Real Tons","Copper Grade","Soluble Copper Grade","Py","Iron","Arsenic","Deep Work Index" ,"Mo","Bond Work Index","Kao","Piro","Cp","Bn","Ill","Mus","Sulfide","PH","Sedimentation Rate"]]
    return selected_columns


level_data = read_df("September.xlsx", size=100000)
level_data = level_data.drop([0])
level_data = level_data.filter(items=["Timestamp", "115FE204_02M1RUN"," CO13_V0304S01", "CO13_V0306P03", "CO13_V0304E01", "115LIT12040A"])
level_data['Timestamp'] = pd.to_datetime(level_data['Timestamp'])
level_data = level_data.rename(columns={"Timestamp": "timestamp"})
level_data = level_data.rename(columns={"115FE204_02M1RUN": "feeder", "115LIT12040A": "level", "CO13_V0304S01": "crusher_speed", "CO13_V0306P03": "crusher_pressure", "CO13_V0304E01":"crusher_power"})

anal_data = read_df("crusher_data_for_analysis.csv",size=len(level_data))
anal_data = anal_data.filter(items=["timestamp", "115YL12011A", "115YL12013A", ])
anal_data['timestamp'] = pd.to_datetime(anal_data['timestamp'])
anal_data = anal_data.rename(columns={"115YL12013A": "ampel_n", "115YL12011A": "ampel_s"})
ampel_data = pd.merge(anal_data, level_data, left_on='timestamp', right_on='timestamp', how='inner')

ampel_data["ampel_n"] = ampel_data["ampel_n"].str.slice(0,1)
ampel_data["ampel_n"] = pd.to_numeric(ampel_data["ampel_n"], errors='coerce').dropna().astype(int)
ampel_data["ampel_s"] = ampel_data["ampel_s"].str.slice(0,1)
ampel_data["ampel_s"] = pd.to_numeric(ampel_data["ampel_s"], errors='coerce').dropna().astype(int)
#print(ampel_data["ampel_s"][300])
#print(type(ampel_data["ampel_s"][300]))
#ampel_data["ampel_n"] = ampel_data["ampel_n"].astype(int)
#ampel_data["ampel_s"] = ampel_data["ampel_s"].str.slice(0,1)
#ampel_data["ampel_s"] = ampel_data["ampel_s"].astype(int)


#print(september_data_2.dtypes)
store_df( "ampel_hohe.csv", ampel_data)

print (np.size(ampel_data["ampel_n"]))
print (np.size(ampel_data["ampel_s"]))
print (np.size(level_data))
print (ampel_data)
print (level_data)

print ('start of analysis of pit lvl')
analysis.analysis_pit_lvl_data(level_data, ampel_data)
print ('analysis of pit lvl completed')

# print ('start of analysis of truck loads')
# dataframe_truck_loads = ...
# correlations.correlations(dataframe, dataframe_truck_loads)