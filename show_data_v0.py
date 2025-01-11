import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("september_data.csv", delimiter=";", nrows=1000)

df['timestamp'] = pd.to_datetime(df['timestamp'])

print(df.head())

df['ampel_an_oder_aus'] = df['ampel_an_oder_aus'].str.replace(',', '.').astype(float)


plt.figure(figsize=(20, 10))
plt.plot(df['timestamp'], df['level'], marker='o', label='Level')


on_spans = []
is_on = False
start_time = None

for i, row in df.iterrows():
    if row['ampel_an_oder_aus'] == 1 and not is_on:
        start_time = row['timestamp']
        is_on = True
    elif row['ampel_an_oder_aus'] == 0 and is_on:
        on_spans.append((start_time, row['timestamp']))
        is_on = False

# Plot the data
plt.figure(figsize=(10, 5))
plt.plot(df['timestamp'], df['level'], marker='o', label='Level')

# Highlight regions where ampel_an_oder_aus is on
for start, end in on_spans:
    plt.axvspan(start, end, color='yellow', alpha=0.3)

plt.xticks(pd.date_range(start=df['timestamp'].min(), end=df['timestamp'].max(), freq='T'))


# Customize the plot
plt.title('115LIT12040A vs Timestamp')
plt.xlabel('Timestamp')
plt.ylabel('115LIT12040A')
#plt.grid(True)
plt.legend()

# Display the plot
plt.tight_layout()
#plt.show()
plt.savefig("plot.png", dpi=100)
