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
