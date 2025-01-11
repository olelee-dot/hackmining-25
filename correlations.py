import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
import analysis

def correlations (dataframe_pit_level, dataframe_truck_loads):
    # function to correlate the crusher speed, AUC of crusher, time to peak of crusher with characteristics of truck loads
    # inputs: dataframe_pit_level (pandas dataframe) with pit level data, dataframe_truck_loads (pandas dataframe) with truck load data

    List_of_Peak_To_Peak = analysis.find_lin_section(dataframe_pit_level)
    # Initialisiere ein leeres DataFrame mit Spaltennamen
    Data_frame_for_correlation = pd.DataFrame(columns=[
    "Timestamp", 
    "Crusher_Speed", 
    "AUC", 
    "Seconds_From_Min_To_Final_Peak", 
    "Correlating_Truck_Feature_1", 
    "Correlating_Truck_Feature_2"  # Füge hier weitere Truck-Eigenschaften hinzu
])

    # find the correlating truck of one object using the timestamp of the first peak and the last truck to unload before that timestamp
    for i in range (len(List_of_Peak_To_Peak)):
        preceding_trucks = dataframe_truck_loads[dataframe_truck_loads['Truck Discharge Date'] < List_of_Peak_To_Peak[i].timestamp_first_peak] 
        if not preceding_trucks.empty:
            correlating_truck = preceding_trucks.iloc[-1] # last preceding truck
            
            if correlating_truck['Truck Discharge Date'] > List_of_Peak_To_Peak[i].timestamp_first_peak - pd.Timedelta(minutes=15):
                # Füge eine neue Zeile ins DataFrame ein
                Data_frame_for_correlation = Data_frame_for_correlation.append({
                    "Timestamp": List_of_Peak_To_Peak[i].timestamp_first_peak,
                    "Crusher_Speed": List_of_Peak_To_Peak[i].crusher_speed,
                    "AUC": List_of_Peak_To_Peak[i].AUC,
                    "Seconds_From_Min_To_Final_Peak": List_of_Peak_To_Peak[i].seconds_to_final_peak - List_of_Peak_To_Peak[i].timestamp_min_fill,
                    "Correlating_Truck_Feature_1": correlating_truck['...'],  # Beispiel: Entladegewicht
                    "Correlating_Truck_Feature_2": correlating_truck['...']   # Beispiel: Truck-ID
                }, ignore_index=True)
            else:
                print ("No correlating truck found for peak-to-peak segement at', List_of_Peak_To_Peak[i].timestamp_first_peak")
        else:
            print ("No correlating truck found for peak-to-peak segement at', List_of_Peak_To_Peak[i].timestamp_first_peak")

    # drop rows with NaN values
    Data_frame_for_correlation.dropna(inplace=True)

    correlation_results = Data_frame_for_correlation.corr(method='pearson') # Pearson correlation coefficient

    # filter for correlations above a certain threshold
    significant_correlations = []
    correlation_threshold = 0.5
    for col_a in correlation_results.columns:
        for col_b in correlation_results.columns:
            if col_a != col_b:
                corr_value = correlation_results.loc[col_a, col_b]
                if abs(corr_value) >= correlation_threshold:
                    significant_correlations.append((col_a, col_b, corr_value))

    # print significant correlations
    print("correlations above the threshold of ", correlation_threshold, ")")
    for col_a, col_b, corr_value in significant_correlations:
        print(f"{col_a} vs {col_b}: {corr_value:.2f}")

    # Visualisierung aller Korrelationen als Heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_results, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title("Pearson Correlation Matrix")
    plt.show()

    # Visualisierung der signifikanten Korrelationen (Scatterplots)
    for col_a, col_b, corr_value in significant_correlations:
        plt.figure(figsize=(6, 4))
        sns.scatterplot(data=Data_frame_for_correlation, x=col_a, y=col_b)
        plt.title(f"Correlation: {col_a} vs {col_b} (r = {corr_value:.2f})")
        plt.xlabel(col_a)
        plt.ylabel(col_b)
        plt.grid(True)
        plt.show()