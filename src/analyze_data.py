import os
import pandas as pd
import matplotlib.pyplot as plt

# Bulletproof path to load the CSV file
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "../data/temperature_data.csv")

df_loaded = pd.read_csv(csv_path)
df_loaded["Temperature_Difference"] = (
    df_loaded["Temperature"].diff()
)
df_loaded["Time_Difference"] = (
    df_loaded["Elapsed_Time"].diff()
)
df_loaded["Temperature_Rate_C_per_s"] = (
    df_loaded["Temperature_Difference"] /
    df_loaded["Time_Difference"]
)

# Calculate 5-sample moving average
df_loaded["Moving_Average"] = (
    df_loaded["Temperature"].rolling(window=5).mean()
)

df_loaded["MA_3"] = df_loaded["Temperature"].rolling(window=3).mean()

df_loaded["MA_5"] = df_loaded["Temperature"].rolling(window=5).mean()

df_loaded["MA_10"] = df_loaded["Temperature"].rolling(window=10).mean()

print("\n--- Temperature Change Analysis ---")

print(
    df_loaded[
        [
            "Elapsed_Time",
            "Temperature",
            "Temperature_Rate_C_per_s"
        ]
    ].head(15)
)

print("\n--- Temperature Rate Statistics ---")

print(
    df_loaded["Temperature_Rate_C_per_s"].describe()
)

print("--- First 5 Rows ---")
print(df_loaded.head())

print("\n--- Moving Average Analysis ---")

print(
    df_loaded[
        [
            "Elapsed_Time",
            "Temperature",
            "Moving_Average"
        ]
    ].head(15)
)

print(
    df_loaded[
        ["Temperature", "MA_3", "MA_5", "MA_10"]
    ].head(20)
)
# Define our safety engineering threshold (°C)
THRESHOLD = 29.0

# Create a boolean mask to find temperatures exceeding the threshold
anomaly_mask = df_loaded["Temperature"] > THRESHOLD

# Filter the dataframe to isolate only the abnormal readings
anomalies = df_loaded[anomaly_mask]

# Display the results
print("\n--- Task A: Anomaly Detection Results ---")
print(f"Engineering Threshold: {THRESHOLD} °C")
print(f"Total Anomalies Detected: {len(anomalies)}")
print("\nAbnormal Readings Log:")
print(anomalies[["Elapsed_Time", "Timestamp", "Temperature"]])


# --- Task B: Data Visualization ---
plt.figure(figsize=(12, 6))

# 1. Plot Raw Temperature Readings
plt.plot(
    df_loaded["Elapsed_Time"], 
    df_loaded["Temperature"], 
    label="Raw Temperature", 
    color="skyblue", 
    alpha=0.7, 
    linewidth=1.5
)

# 2. Plot Moving Average
plt.plot(
    df_loaded["Elapsed_Time"], 
    df_loaded["Moving_Average"], 
    label="5-Sample Moving Average", 
    color="blue", 
    linewidth=2
)

# 3. Plot Temperature Threshold Line
plt.axhline(
    y=THRESHOLD, 
    color="orange", 
    linestyle="--", 
    linewidth=1.5, 
    label=f"Threshold ({THRESHOLD} °C)"
)

# 4. Plot Detected Abnormal Readings (Anomalies as red scatter points)
plt.scatter(
    anomalies["Elapsed_Time"], 
    anomalies["Temperature"], 
    color="red", 
    s=50, 
    zorder=5, 
    label="Detected Anomalies"
)

# Customize graph labels and legend
plt.title("Sensor Temperature Monitoring & Anomaly Detection", fontsize=14, fontweight="bold")
plt.xlabel("Elapsed Time (seconds)", fontsize=12)
plt.ylabel("Temperature (°C)", fontsize=12)
plt.legend(loc="upper left")
plt.grid(True, linestyle=":", alpha=0.6)

# Display the interactive plot window
plt.tight_layout()
plt.show()