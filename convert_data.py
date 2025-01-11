import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

data_path = os.path.join(os.path.dirname(__file__), "original_data")

def read_file(filename: str):
    file = pd.read_excel(os.path.join(data_path, filename))
    return file
    

a = read_file("Dispatch_260924-251024.xlsx")
# Display the shape of the dataframe
print("Number of rows:", a.shape[0])
print("Number of columns:", a.shape[1])


