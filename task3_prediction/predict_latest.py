import requests
import joblib
import pandas as pd

# Step 1: Fetch latest weather observation from MongoDB API endpoint
response = requests.get("http://127.0.0.1:8000/mongo/observations/")
if response.status_code != 200:
    print(f"❌ Failed to fetch data from API: {response.status_code} {response.reason}")
    exit()

json_data = response.json()

# Extract observations list from the "data" key
data = json_data.get("data", [])
if not data:
    print("❌ No observation data available.")
    exit()

# Get the latest record (assuming last one is latest)
latest = data[-1]

# Step 2: Prepare input for model
input_data = {
    "Rainfall": latest.get("rainfall", 0),
    "MaxTemp": latest.get("max_temp", 0),
    "MinTemp": latest.get("min_temp", 0),
    "Humidity9am": latest.get("humidity_9am", 0),
    "Humidity3pm": latest.get("humidity_3pm", 0),
}

input_df = pd.DataFrame([input_data])

# Step 3: Load the trained model
model = joblib.load("data/rain_predictor.pkl")

# Step 4: Make prediction
prediction = model.predict(input_df)
probability = model.predict_proba(input_df)[0][1]

# Step 5: Output result
print("🌧️ Will it rain tomorrow?", "Yes" if prediction[0] == 1 else "No")
print(f"💧 Probability of rain: {probability * 100:.2f}%")
