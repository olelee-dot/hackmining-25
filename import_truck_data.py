import os
import pandas as pd

def import_truck_data():
    data_path = os.path.join(os.path.dirname(__file__), "original_data")

    file1 = pd.read_excel(os.path.join(data_path, "Dispatch_260924-251024.xlsx"))
    file2 = pd.read_excel(os.path.join(data_path, "Dispatch_261024-251124.xlsx"))
    file3 = pd.read_excel(os.path.join(data_path, "Dispatch_261124-251224.xlsx"))

    if list(file1.columns) == list(file2.columns) == list(file3.columns):
        combined_df = pd.concat([file1, file2, file3], ignore_index=True)
    else:
        print("Columns of the files are not the same")
    
    combined_df['Truck Discharge Date'] = pd.to_datetime(combined_df['Truck Discharge Date'], errors='coerce')

    return combined_df