import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

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


level_data = read_df("September.xlsx", size=2000)
level_data = level_data.drop([0])
level_data = level_data.filter(items=["Timestamp", "115FE204_02M1RUN", "CO13_V0304S01", "CO13_V0306P03", "CO13_V0304E01", "115LIT12040A"])
level_data['Timestamp'] = pd.to_datetime(level_data['Timestamp'])
level_data = level_data.rename(columns={"Timestamp": "timestamp"})
level_data = level_data.rename(columns={"115FE204_02M1RUN": "feeder", "115LIT12040A": "level", "CO13_V0304S01": "crusher_speed", "CO13_V0306P03": "crusher_pressure", "CO13_V0304E01":"crusher_power"})

ampel_data = read_df("crusher_data_for_analysis.csv",size=len(level_data))
#ampel_data = ampel_data.filter(items=["timestamp", "115YL12013A"])
ampel_data['timestamp'] = pd.to_datetime(ampel_data['timestamp'])
ampel_data = ampel_data.rename(columns={"115YL12013A": "ampel"})

#september_data_2 = pd.merge(ampel_data, level_data, left_on='timestamp', right_on='timestamp', how='inner')
#print(september_data_2.dtypes)
#store_df(september_data_2, "september_data_2.csv")
store_df("ampel_data.csv", ampel_data)


#crusher_data = read_df("crusher_data_for_analysis.csv")
#disp = read_df("Dispatch_260924-251024.xlsx")
#sep_data = read_df("September.xlsx")
#disp = make_disp_smaller(disp)
#store_df("test.csv", disp)


#store_df("test.csv", crusher_data)



