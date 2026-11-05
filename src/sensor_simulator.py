import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Sensor simulation parameters
initial_temperature = 25.0
heating_rate = 0.05
total_time = 100

# Generate time values (stops at 100)
time = np.arange(0, total_time, 1)

# Generate random sensor noise
noise = np.random.normal(0, 0.2, len(time))

# Calculate temperature
temperature = np.round(initial_temperature + heating_rate * time + noise, 2)

# Define a starting date and time for our simulation
start_time = datetime.now().replace(microsecond=0)

# Generate timestamps using your list comprehension
timestamps = [
    start_time + timedelta(seconds=int(t))
    for t in time
]

# Create a structured dataset
data = {
    "Timestamp": timestamps,
    "Elapsed_Time": time,
    "Temperature": temperature
}

df = pd.DataFrame(data)

# --- BULLETPROOF PATH SETUP ---
# 1. Find the exact folder where this python script lives (which is 'src')
script_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Build a safe path to the 'data' folder in the root directory
data_dir = os.path.join(script_dir, "../data")

# 3. Automatically create it if it doesn't exist
os.makedirs(data_dir, exist_ok=True)

# 4. Save the file safely
csv_filename = os.path.join(data_dir, "temperature_data.csv")
df.to_csv(csv_filename, index=False)
print(f"Data successfully saved to {csv_filename}!\n")
# ------------------------------

print(df)

# Display results
print("Sensor Simulation Log")
print("=" * 65)

for ts, t, temp in zip(timestamps, time, temperature):
    print(f"{ts} |     Time: {t:3d} s |     Temperature: {temp:.2f} °C")

# Calculate summary statistics
avg_temp = np.mean(temperature)
max_temp = np.max(temperature)
min_temp = np.min(temperature)
temperature_above_29 = df[df["Temperature"] > 29]

# Display summary block
print("\n" + "=" * 65)
print("Temperature Simulation Summary")
print(f"Average Temperature: {avg_temp:.2f} °C")
print(f"Maximum Temperature: {max_temp:.2f} °C")
print(f"Minimum Temperature: {min_temp:.2f} °C")
print("=" * 65)

df.info()
print(df.describe())

print('\nTemperature above expectation == ')
print(f'\n{temperature_above_29}')