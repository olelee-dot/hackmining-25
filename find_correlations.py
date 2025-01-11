import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import import_truck_data
import correlations

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


list_of_files = ["September.xlsx", "October part 1.xlsx", "October part 2.xlsx", "October part 3.xlsx", "November part 1.xlsx", "November part 2.xlsx", "November part 3.xlsx", "December part 1.xlsx", "December part 2.xlsx", "December part 3.xlsx"]
for i in range(len(list_of_files)):
    level_data = read_df(list_of_files[i], size = 1000000)
    level_data = level_data.drop([0])
    level_data = level_data.filter(items=["Timestamp", "115FE204_02M1RUN"," CO13_V0304S01", "CO13_V0306P03", "CO13_V0304E01", "115LIT12040A"])
    level_data['Timestamp'] = pd.to_datetime(level_data['Timestamp'])
    level_data = level_data.rename(columns={"Timestamp": "timestamp"})
    level_data = level_data.rename(columns={"115FE204_02M1RUN": "feeder", "115LIT12040A": "level", "CO13_V0304S01": "crusher_speed", "CO13_V0306P03": "crusher_pressure", "CO13_V0304E01":"crusher_power"})
    print (np.size(level_data))
    if i == 0:
        combined_df = level_data  
    else:  
        combined_df = pd.concat([combined_df, level_data], ignore_index=True)

truck_data = import_truck_data()

correlations (combined_df, truck_data)