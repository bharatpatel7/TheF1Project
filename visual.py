import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#load csv file
standings =  pd.read_csv("data/standings.csv")
lap_times = pd.read_csv("data/lap_times.csv", encoding='utf-8')
pit_stops = pd.read_csv("data/pit_stops.csv")

constructor_colors = {
    'red_bull': '#1E41FF',
    'mercedes': '#00D2BE',
    'ferrari': '#DC0000',
    'mclaren': '#FF8700',
    'aston_martin': '#006F62',
    'alpine': '#0060A9',
    'alfa_romeo': '#9B0000',
    'williams': '#0056A0',
    'alpha_tauri': '#2A4D7C',
    'haas': '#FFFFFF', #white
}

#display rows
print("Constructor Standings:")
print(standings.head())

print("\nLap Times Data:")
print(lap_times.head())

print("\nPit Stops Data:")
print(pit_stops.head())

#plotting constructor standings
plt.figure(figsize=(10, 6))
standings_top_10 = standings.head(10)

standings_top_10.loc[:, 'color'] = standings_top_10['constructorID'].map(constructor_colors)

standings_top_10['color'].fillna('#808080', inplace=True)

sns.barplot(data=standings_top_10, x='name', y='points', hue='name', dodge=False, palette=standings_top_10['color'].tolist())
plt.title('Top 10 Constructors by points')
plt.xlabel('Constructor')
plt.ylabel('Points')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()


# Cleaning lap_times data
lap_times['time'] = lap_times['time'].astype(str)

lap_times['time'] = lap_times['time'].apply(lambda x: '00:' + x if ':' in x else '00:00:' + x)

lap_times = lap_times.dropna(subset=['time'])

##print(lap_times['time'].unique())
lap_times['time'] = pd.to_timedelta(lap_times['time'], errors='coerce') 

lap_times = lap_times.dropna(subset=['time'])

print("\nLap Times Data after cleaning:")
print(lap_times.head())

##lap_times = lap_times.dropna(subset=['time'])  # Dropping any rows with invalid times

# Average lap times per driver
avg_lap_times = lap_times.groupby('driverId')['time'].mean().reset_index()
avg_lap_times['time'] = avg_lap_times['time'].dt.total_seconds() / 60  # Converting to minutes

avg_lap_times = avg_lap_times.sort_values(by='time', ascending=True)

# Plotting average lap times
plt.figure(figsize=(10, 6))
sns.barplot(data=avg_lap_times, x='driverId', y='time', hue='driverId', palette='coolwarm')
plt.title('Average Lap Time per Driver (Minutes)')
plt.xlabel('Driver ID')
plt.ylabel('Average Lap Time (Minutes)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()


#plotting Pit Stops
plt.figure(figsize=(10, 6))
pit_stops_count = pit_stops.groupby('driverId')['stop'].nunique().reset_index()
pit_stops_count = pit_stops_count.sort_values(by='stop', ascending=True)
sns.barplot(data=pit_stops_count, x='driverId', y='stop',hue='driverId', palette='viridis')
plt.title('Total pit stops per driver')
plt.xlabel('Driver ID')
plt.ylabel('Total pit stops')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()