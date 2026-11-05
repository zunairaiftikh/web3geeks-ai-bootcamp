import json
from pathlib import Path

from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

BASE_DIR = Path(__file__).resolve().parent

with open(BASE_DIR / "sample_booking.json") as f:
    SAMPLE_BOOKING = json.load(f)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_sample_prediction_matches_expected():
    response = client.post("/predict", json=SAMPLE_BOOKING)

    assert response.status_code == 200
    assert round(response.json()["cancel_probability"], 4) == 0.1711
    assert response.json()["risk"] == "low"


def test_missing_field():
    booking = SAMPLE_BOOKING.copy()
    booking.pop("hotel")

    response = client.post("/predict", json=booking)
    assert response.status_code == 422


def test_invalid_month():
    booking = SAMPLE_BOOKING.copy()
    booking["arrival_date_month"] = "Jul"

    response = client.post("/predict", json=booking)
    assert response.status_code == 422


def test_negative_adults():
    booking = SAMPLE_BOOKING.copy()
    booking["adults"] = -1

    response = client.post("/predict", json=booking)
    assert response.status_code == 422


def test_batch_prediction():
    response = client.post(
        "/predict_batch",
        json=[SAMPLE_BOOKING, SAMPLE_BOOKING, SAMPLE_BOOKING],
    )

    assert response.status_code == 200
    assert len(response.json()) == 3


def test_company_integer_and_float():
    booking_integer = SAMPLE_BOOKING.copy()
    booking_float = SAMPLE_BOOKING.copy()

    booking_integer["company"] = 174
    booking_float["company"] = 174.0

    response_integer = client.post("/predict", json=booking_integer)
    response_float = client.post("/predict", json=booking_float)

    assert response_integer.status_code == 200
    assert response_float.status_code == 200

    assert round(
        response_integer.json()["cancel_probability"], 4
    ) == round(
        response_float.json()["cancel_probability"], 4
    )