
from pathlib import Path
import sys

import joblib
import pandas as pd

from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict, Field
from typing import Literal


# --------------------------------------------------
# 1. FIND WEEK3 DIRECTORY AND LOAD MODEL ONCE
# --------------------------------------------------

WEEK3_DIR = Path(__file__).resolve().parent

# Make features.py available when starting from either
# the repository root or the week3 directory.
if str(WEEK3_DIR) not in sys.path:
    sys.path.insert(0, str(WEEK3_DIR))

# Import required for loading the saved pipeline.
from features import add_features

MODEL_PATH = WEEK3_DIR / "booking_model.joblib"

model = joblib.load(MODEL_PATH)

INPUT_COLUMNS = list(model.feature_names_in_)

# --------------------------------------------------
# 2. CREATE FASTAPI APPLICATION
# --------------------------------------------------

app = FastAPI(
    title="Hotel Booking Cancellation Prediction API",
    description="Predicts hotel booking cancellation probability.",
    version="1.0.0"
)


# --------------------------------------------------
# 3. VALIDATE BOOKING INPUT (27 ORIGINAL COLUMNS)
# --------------------------------------------------

class Booking(BaseModel):

    model_config = ConfigDict(extra="forbid")

    hotel: Literal["City Hotel", "Resort Hotel"]

    lead_time: int = Field(ge=0)

    arrival_date_year: int = Field(ge=1)
    arrival_date_month: Literal[
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ]

    arrival_date_week_number: int = Field(ge=1, le=53)
    arrival_date_day_of_month: int = Field(ge=1, le=31)

    stays_in_weekend_nights: int = Field(ge=0)
    stays_in_week_nights: int = Field(ge=0)

    adults: int = Field(ge=0)
    children: float | None = Field(ge=0)
    babies: int = Field(ge=0)

    meal: str
    country: str | None

    market_segment: str
    distribution_channel: str

    is_repeated_guest: Literal[0, 1]

    previous_cancellations: int = Field(ge=0)
    previous_bookings_not_canceled: int = Field(ge=0)

    reserved_room_type: str
    deposit_type: str

    agent: float | None = Field(ge=0)
    company: float | None = Field(ge=0)

    days_in_waiting_list: int = Field(ge=0)
    customer_type: str

    adr: float = Field(ge=0)

    required_car_parking_spaces: int = Field(ge=0)
    total_of_special_requests: int = Field(ge=0)


# --------------------------------------------------
# 4. PREDICTION HELPER
# --------------------------------------------------

def predict_booking(booking: Booking):

    booking_data = booking.model_dump()

    # Keep the exact original model input columns and order.
    input_df = pd.DataFrame(
        [booking_data],
        columns=INPUT_COLUMNS
    )

    # Get probability of cancellation (class 1).
    probability = float(
        model.predict_proba(input_df)[0][1]
    )

    # Determine risk level.
    if probability >= 0.8:
        risk = "high"

    elif probability >= 0.5:
        risk = "medium"

    else:
        risk = "low"

    return {
        "cancel_probability": probability,
        "risk": risk
    }


# --------------------------------------------------
# 5. HEALTH ENDPOINT
# --------------------------------------------------

@app.get("/health")
def health():

    return {"status": "ok"}


# --------------------------------------------------
# 6. SINGLE BOOKING PREDICTION
# --------------------------------------------------

@app.post("/predict")
def predict(booking: Booking):

    return predict_booking(booking)


# --------------------------------------------------
# 7. BATCH BOOKING PREDICTION
# --------------------------------------------------

@app.post("/predict_batch")
def predict_batch(bookings: list[Booking]):

    return [
        predict_booking(booking)
        for booking in bookings
    ]
