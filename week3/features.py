
import pandas as pd
import numpy as np


def add_features(df):
    """
    Add five booking-time features to the hotel booking dataset.
    Returns a copy of the original DataFrame with new columns.
    """

    df = df.copy()

    # 1. Total nights spent at the hotel
    df["total_nights"] = (
        df["stays_in_weekend_nights"]
        + df["stays_in_week_nights"]
    )

    # 2. Total number of guests
    # Missing children values are treated as zero.
    children = pd.to_numeric(df["children"], errors="coerce").fillna(0)

    df["total_guests"] = (
        df["adults"].fillna(0)
        + children
        + df["babies"].fillna(0)
    )

    # 3. Average daily rate per guest
    # Avoid division by zero when there are no guests.
    df["adr_per_guest"] = np.divide(
        df["adr"],
        df["total_guests"],
        out=np.zeros(len(df), dtype=float),
        where=df["total_guests"] != 0
    )

    # 4. Weekday of arrival
    # Convert month names into month numbers.
    month_number = pd.to_datetime(
        df["arrival_date_month"],
        format="%B",
        errors="coerce"
    ).dt.month

    arrival_date = pd.to_datetime(
        {
            "year": df["arrival_date_year"],
            "month": month_number,
            "day": df["arrival_date_day_of_month"]
        },
        errors="coerce"
    )

    # Monday = 0, Sunday = 6
    df["arrival_weekday"] = arrival_date.dt.dayofweek

    # 5. Previous cancellation rate
    # All previous bookings = previous cancellations
    # + previous bookings that were not cancelled.
    previous_total = (
        df["previous_cancellations"]
        + df["previous_bookings_not_canceled"]
    )

    df["prev_cancel_rate"] = np.divide(
        df["previous_cancellations"],
        previous_total,
        out=np.zeros(len(df), dtype=float),
        where=previous_total != 0
    )

    # Convert agent and company into text categories.
    # Missing values become "none".
    for col in ["agent", "company"]:
        df[col] = df[col].where(df[col].notna(), "none").astype(str)

    return df
