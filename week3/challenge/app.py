
from pathlib import Path

import joblib
import numpy as np

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


# Load the saved model
MODEL_PATH = Path(__file__).parent / "model.joblib"
model = joblib.load(MODEL_PATH)

# Confidence threshold
CONFIDENCE_THRESHOLD = 0.40

app = FastAPI(
    title="Banking77 Intent Classification API",
    description="Classifies banking customer support messages."
)


class PredictionRequest(BaseModel):
    text: str


def validate_text(text):
    if not text.strip():
        raise HTTPException(
            status_code=422,
            detail="Message cannot be empty or blank."
        )

    if len(text) > 500:
        raise HTTPException(
            status_code=422,
            detail="Message cannot exceed 500 characters."
        )


def predict_message(text):
    validate_text(text)

    probabilities = model.predict_proba([text])[0]

    # Sort intents from highest to lowest confidence
    top_indices = np.argsort(probabilities)[::-1][:3]

    top_three = [
        {
            "intent": str(model.classes_[i]),
            "confidence": round(float(probabilities[i]), 4)
        }
        for i in top_indices
    ]

    best_prediction = top_three[0]

    return {
        "intent": best_prediction["intent"],
        "confidence": best_prediction["confidence"],
        "top_3": top_three,
        "needs_human": (
            best_prediction["confidence"] < CONFIDENCE_THRESHOLD
        )
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(request: PredictionRequest):
    return predict_message(request.text)


@app.post("/predict_batch")
def predict_batch(messages: list[str]):
    results = []

    for message in messages:
        results.append(predict_message(message))

    return results
