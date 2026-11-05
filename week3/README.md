# Hotel Booking Cancellation Prediction API

## Project Overview

This project serves a trained hotel booking cancellation prediction model through a REST API built with FastAPI.

The API uses the existing trained model (`booking_model.joblib`) and feature engineering function (`features.py`). The model predicts the probability that a hotel booking will be cancelled.

## Project Structure

```text
week3/
├── app.py
├── features.py
├── booking_model.joblib
├── sample_booking.json
├── create_sample.py
├── test_app.py
├── requirements.txt
└── README.md
```

## Installation

Activate the virtual environment and install dependencies:

```bash
pip install -r requirements.txt
```

## Running the API

From the repository root:

```bash
python -m uvicorn week3.app:app --reload
```

The API runs at:

`http://127.0.0.1:8000`

Interactive API documentation:

`http://127.0.0.1:8000/docs`

## API Endpoints

### 1. Health Check

**GET `/health`**

Checks whether the API is running.

Example response:

```json
{
  "status": "ok"
}
```

### 2. Single Prediction

**POST `/predict`**

Accepts one booking containing 27 input features.

Returns:

- `cancel_probability`: predicted cancellation probability.
- `risk`: cancellation risk category.

Risk categories:

- High: probability >= 0.80
- Medium: probability >= 0.50 and < 0.80
- Low: probability < 0.50

### 3. Batch Prediction

**POST `/predict_batch`**

Accepts a list of bookings and returns predictions in the same order.

## Input Validation

Pydantic validates the incoming booking data.

Validation includes:

- Hotel must be `City Hotel` or `Resort Hotel`.
- Arrival month must be a full month name.
- Counts cannot be negative.
- Children, country, agent, and company can be null.
- Invalid or missing required fields return HTTP 422.

## Model and Feature Engineering

The existing trained model is loaded once when the application starts.

The pipeline performs feature engineering using `features.py`, preprocessing, and XGBoost classification.

The model is not retrained by the API.

## Testing

Run the automated tests from the `week3` directory:

```bash
python -m pytest -v
```

The test suite checks:

1. Health endpoint.
2. Sample prediction against the expected model probability.
3. Missing required field validation.
4. Invalid month validation.
5. Negative adults validation.
6. Batch prediction.
7. Company integer and float input consistency.

**Current result: 7 tests passed.**

## Sample Prediction

The sample booking is generated from the original notebook's test split using:

- `test_size=0.2`
- `random_state=42`
- `stratify=y`

The saved model's sample cancellation probability, rounded to four decimal places, is `0.1711`.

## Technologies Used

- Python
- FastAPI
- Uvicorn
- Pandas
- Scikit-learn
- XGBoost
- Joblib
- Pydantic
- Pytest
