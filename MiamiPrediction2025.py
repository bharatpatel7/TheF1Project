import fastf1
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error

# Enable FastF1 caching
fastf1.Cache.enable_cache("f1_cache")

# Load FastF1 2024 Miami GP race session
session_2024_race = fastf1.get_session(2024, "Miami", "R")
session_2024_race.load()

# Extract race lap times
laps_2024 = session_2024_race.laps[["Driver", "LapTime"]].copy()
laps_2024.dropna(subset=["LapTime"], inplace=True)
laps_2024["LapTime (s)"] = laps_2024["LapTime"].dt.total_seconds()

# Load FastF1 2024 Miami GP qualifying session
session_2024_qualifying = fastf1.get_session(2024, "Miami", "Q")
session_2024_qualifying.load()

# Extract qualifying times
qualifying_2024 = session_2024_qualifying.laps[["Driver", "LapTime"]].copy()
qualifying_2024.dropna(subset=["LapTime"], inplace=True)
qualifying_2024["QualifyingTime (s)"] = qualifying_2024["LapTime"].dt.total_seconds()

# Merge qualifying and race data
merged_data = qualifying_2024.merge(laps_2024, on="Driver")
X_qualifying = merged_data[["QualifyingTime (s)"]]
y_race = merged_data["LapTime (s)"]

# Step 1: Predict Qualifying Times for 2025
# Use historical qualifying data to train a model
X_train_q, X_test_q, y_train_q, y_test_q = train_test_split(
    X_qualifying, merged_data["QualifyingTime (s)"], test_size=0.2, random_state=39
)
qualifying_model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, random_state=39)
qualifying_model.fit(X_train_q, y_train_q)

# Predict qualifying times for 2025
drivers_2025 = ["Lando Norris", "Oscar Piastri", "Max Verstappen", "George Russell", "Yuki Tsunoda",
                "Alexander Albon", "Charles Leclerc", "Lewis Hamilton", "Pierre Gasly", "Carlos Sainz", "Fernando Alonso", "Lance Stroll"]
qualifying_2025 = pd.DataFrame({
    "Driver": drivers_2025,
    "QualifyingTime (s)": qualifying_model.predict(X_train_q[:len(drivers_2025)])  # Use historical data for prediction
})

# Step 2: Predict Race Times for 2025
# Use predicted qualifying times to predict race times
X_race = qualifying_2025[["QualifyingTime (s)"]]
race_model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, random_state=39)
race_model.fit(X_qualifying, y_race)  # Train on historical data
predicted_race_times = race_model.predict(X_race)

qualifying_2025["PredictedRaceTime (s)"] = predicted_race_times

# Rank drivers by predicted race time
qualifying_2025 = qualifying_2025.sort_values(by="PredictedRaceTime (s)")

# Print final predictions
print("\n🏁 Predicted 2025 Miami GP Results 🏁\n")
print(qualifying_2025[["Driver", "QualifyingTime (s)", "PredictedRaceTime (s)"]])

# Evaluate Models
y_pred_q = qualifying_model.predict(X_test_q)
print(f"\n🔍 Qualifying Model Error (MAE): {mean_absolute_error(y_test_q, y_pred_q):.2f} seconds")