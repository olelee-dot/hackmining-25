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
    # initialize empty DataFrame
    Data_frame_for_correlation = pd.DataFrame(columns=[
    "Timestamp", 
    "Crusher_Speed", 
    "AUC", 
    "Crusher Power",
    "Crusher Pressure",
    "Seconds_From_Min_To_Final_Peak", 
    "weight",
    "Copper Grade",
    "Soluble Copper Grade",
    "Py",
    "Iron",
    "Arsenic",
    "Deep Work Index",
    "Mo",
    "Bond Work Index",
    "Kao",
    "Piro",
    "Cp",
    "Bn",
    "Ill",
    "Mus",
    "Sulfide",
    "PH",
    "Sedimentation Rate",
    "Abrasiveness Index"
])

    # find the correlating truck of one object using the timestamp of the first peak and the last truck to unload before that timestamp
    no_truck_found = 0
    for i in range (len(List_of_Peak_To_Peak)):
        preceding_trucks = dataframe_truck_loads[dataframe_truck_loads['Truck Discharge Date'] < List_of_Peak_To_Peak[i].timestamp_first_peak] 
        if not preceding_trucks.empty:
            correlating_truck = preceding_trucks.iloc[-1] # last preceding truck
            if correlating_truck['Truck Discharge Date'] > List_of_Peak_To_Peak[i].timestamp_first_peak - pd.Timedelta(minutes=2):
                # Füge eine neue Zeile ins DataFrame ein
                Data_frame_for_correlation = Data_frame_for_correlation.append({
                    "Timestamp_first_peak": List_of_Peak_To_Peak[i].timestamp_first_peak,
                    "Timestamp_truck_discharge": correlating_truck['Truck Discharge Date'],
                    "Crusher_Speed": List_of_Peak_To_Peak[i].crusher_speed,
                    "AUC": List_of_Peak_To_Peak[i].AUC,
                    "Crusher Power": List_of_Peak_To_Peak[i].Crusher_Power,
                    "Crusher Pressure": List_of_Peak_To_Peak[i].Crusher_Pressure,
                    "Seconds_From_Min_To_Final_Peak": List_of_Peak_To_Peak[i].seconds_to_final_peak - List_of_Peak_To_Peak[i].timestamp_min_fill,
                    "weight": correlating_truck['real tons'],
                    "Copper Grade": correlating_truck['Copper Grade'],
                    "Soluble Copper Grade": correlating_truck['Soluble Copper Grade'],
                    "Py": correlating_truck['Py'],
                    "Iron": correlating_truck['Iron'],
                    "Arsenic": correlating_truck['Arsenic'],
                    "Deep Work Index": correlating_truck['Deep Work Index'],
                    "Mo": correlating_truck['Mo'],
                    "Bond Work Index": correlating_truck['Bond Work Index'],
                    "Kao": correlating_truck['Kao'],
                    "Piro": correlating_truck['Piro'],
                    "Cp": correlating_truck['Cp'],
                    "Bn": correlating_truck['Bn'],
                    "Ill": correlating_truck['Ill'],
                    "Mus": correlating_truck['Mus'],
                    "Sulfide": correlating_truck['Sulfide'],
                    "PH": correlating_truck['PH'],
                    "Sedimentation Rate": correlating_truck['Sedimentation Rate'],
                    "Abrasiveness Index": correlating_truck['Abrasiveness Index']
                }, ignore_index=True)
            else:
                print ("No correlating truck found for peak-to-peak segement at', List_of_Peak_To_Peak[i].timestamp_first_peak")
                no_truck_found = no_truck_found + 1
        else:
            print ("No correlating truck found for peak-to-peak segement at', List_of_Peak_To_Peak[i].timestamp_first_peak")
            no_truck_found = no_truck_found + 1
    print (f'No truck found for {no_truck_found} peak-to-peak segments')

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