import pandas as pd
from functions import constructor_standings, get_pit_stops, get_lap_times

# Fetch data using the functions
standings = constructor_standings(2023)
lap_times = get_lap_times(2023, 1)
pit_stops = get_pit_stops(2023, 1)

# Save the data locally for inspection
standings.to_csv("data/standings.csv", index=False)
lap_times.to_csv("data/lap_times.csv", index=False)
pit_stops.to_csv("data/pit_stops.csv", index=False)

print("Data fetched and saved locally.")
