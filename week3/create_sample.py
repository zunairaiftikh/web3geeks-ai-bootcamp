import json
import pandas as pd
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split

BASE_DIR = Path(__file__).resolve().parent

DATA_URL = (
    "https://raw.githubusercontent.com/rfordatascience/"
    "tidytuesday/master/data/2020/2020-02-11/hotels.csv"
)

df = pd.read_csv(DATA_URL)

df = df.drop(
    columns=[
        "reservation_status",
        "reservation_status_date",
        "assigned_room_type",
        "booking_changes",
    ]
)

X = df.drop("is_canceled", axis=1)
y = df["is_canceled"]

_, X_test, _, _ = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)

sample = X_test.iloc[[0]]

sample_json = json.loads(sample.iloc[0].to_json())

with open(BASE_DIR / "sample_booking.json", "w") as file:
    json.dump(sample_json, file, indent=4)

model = joblib.load(BASE_DIR / "booking_model.joblib")
probability = model.predict_proba(sample)[0][1]

print("Sample booking created successfully!")
print("Notebook/model probability:", round(float(probability), 4))
print("Saved to:", BASE_DIR / "sample_booking.json")