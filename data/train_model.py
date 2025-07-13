import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

df = pd.read_csv("data/weatherAUS.csv")

df = df.dropna(subset=["RainTomorrow", "Rainfall", "MaxTemp", "MinTemp", "Humidity9am", "Humidity3pm"])

le = LabelEncoder()
df["RainTomorrow"] = le.fit_transform(df["RainTomorrow"])  

X = df[["Rainfall", "MaxTemp", "MinTemp", "Humidity9am", "Humidity3pm"]]
y = df["RainTomorrow"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier()
model.fit(X_train, y_train)


joblib.dump(model, "data/rain_predictor.pkl")
print("✅ Model trained and saved to data/rain_predictor.pkl")
