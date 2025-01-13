import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

# Pfade und Daten laden
path = os.path.join(os.path.dirname(__file__), "prepaired_data")
crusher_speeds = pd.read_csv(os.path.join(path, "crusher_speeds.csv"))
feeder_speeds = pd.read_csv(os.path.join(path, "feeder_speeds.csv"))

# Anzahl der Bins
NUM_BINS = 10000

# x-Werte für die Normalverteilung berechnen (basierend auf x-Achsen-Limits)
feeder_x = np.linspace(-3, 0, 1000)
crusher_x = np.linspace(0, 3, 1000)

# Wahrscheinlichkeitsdichtefunktion (PDF) der festen Normalverteilung berechnen
fixed_pdf_feeder = norm.pdf(feeder_x, -0.135, 0.11)
fixed_pdf_crusher = norm.pdf(crusher_x, 0.18, 0.145)

# Feeder Speed Histogram und Normalverteilung plotten
plt.figure(figsize=(10, 6))
plt.hist(feeder_speeds["Feeder_Speeds"], bins=NUM_BINS, density=True, alpha=0.6, color='blue', label='Feeder Speeds Histogram')
plt.plot(feeder_x, fixed_pdf_feeder, color='red', linewidth=2, label='Normal Distribution')
plt.title('Feeder Speed')
plt.xlim(-3, 0)
plt.xlabel('Speed in pit capacity percentage/s')
plt.ylabel('Density')
plt.legend()
plt.show()

# Crusher Speed Histogram und Normalverteilung plotten
plt.figure(figsize=(10, 6))
plt.hist(crusher_speeds["Crusher_Speeds"], bins=NUM_BINS, density=True, alpha=0.6, color='green', label='Crusher Speeds Histogram')
plt.plot(crusher_x, fixed_pdf_crusher, color='red', linewidth=2, label='Normal Distribution')
plt.title('Crusher Speed')
plt.xlim(0, 3)
plt.xlabel('Speed in pit capacity percentage/s')
plt.ylabel('Density')
plt.legend()
plt.show()


import pandas as pd
import os
import matplotlib.pyplot as plt
path = os.path.join(os.path.dirname(__file__), "prepaired_data")
crusher_speeds = pd.read_csv(os.path.join(path, "crusher_speeds.csv"))
feeder_speeds = pd.read_csv(os.path.join(path, "feeder_speeds.csv"))

# Define a constant for the number of bins
NUM_BINS = 10000

# plot histogram of feeder and crusher speed
fig, axs = plt.subplots(2, 1)
axs[0].hist(feeder_speeds["Feeder_Speeds"], bins=NUM_BINS)
axs[0].set_title('Feeder Speed')
# set limit for x-axis
axs[0].set_xlim(-3, 0)
plt.xlabel('Speed in pit capacity percetage/s')
plt.ylabel('Frequency')
# add a title to the plot
axs[1].hist(crusher_speeds["Crusher_Speeds"], bins=NUM_BINS)
axs[1].set_title('Crusher Speed')
# set limit for x-axis
axs[1].set_xlim(0, 3)
fig.suptitle('Histogram of Feeder and Crusher Speeds')
# add axis labels
plt.xlabel('Speed in pit capacity percetage/s')
plt.ylabel('Frequency')
plt.show()

