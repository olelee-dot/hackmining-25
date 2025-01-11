import pandas as pd
import matplotlib.pyplot as plt


import numpy
#import tensorflow

df = pd.read_excel("Final_data_crusher_every_second/September.xlsx")
df = df.drop([0])
df = df[(df['Timestamp'] >= '2024-09-26') & (df['Timestamp'] < '2024-09-27')]
print(df.head(10))


# Ensure the "Timestamps" column is in datetime format
df['Timestamp'] = pd.to_datetime(df['Timestamp'])



# Plot the graph
plt.figure(figsize=(int(df.shape[0]/60), 6))
plt.plot(df['Timestamp'], df['115LIT12040A'], marker='o', linestyle='-', linewidth=0.01, label='115LIT12040A')

# Customize the plot
plt.title('115LIT12040A vs Timestamp')
plt.xlabel('Timestamp')
plt.ylabel('115LIT12040A')
plt.grid(True)
plt.legend()

# Display the plot
plt.tight_layout()
plt.show()