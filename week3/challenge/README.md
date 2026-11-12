# Banking77 Intent Classification API

## 1. Project Overview

This project builds a machine learning API that classifies banking customer support messages into their corresponding intents using the Banking77 dataset.

The API uses TF-IDF for text feature extraction and Logistic Regression for intent classification.

It also provides confidence scores and flags uncertain predictions for human review.

## 2. Dataset

The project uses the Banking77 dataset, which contains banking-related customer service messages categorized into different intents.

The dataset is stored in the `data/` directory:

- `train.csv` – Training data.
- `test.csv` – Testing data.

## 3. Models Evaluated

Three approaches were evaluated:

1. Dummy Classifier (baseline)
2. TF-IDF + Logistic Regression
3. TF-IDF + Multinomial Naive Bayes

### Model Performance

| Model | Accuracy | Macro F1 | Top-3 Accuracy |
|---|---:|---:|---:|
| Dummy Baseline | 1.30% | 0.03% | 3.90% |
| TF-IDF + Logistic Regression | 85.88% | 85.81% | 95.71% |
| TF-IDF + Multinomial Naive Bayes | 85.36% | 85.11% | 94.68% |

### Model Selection

Logistic Regression was selected because it achieved the highest accuracy, macro F1 and top-3 accuracy among the evaluated models.

The model uses:

- TF-IDF vectorization
- Unigrams and bigrams
- Minimum document frequency of 2
- Sublinear term frequency scaling
- Logistic Regression with a maximum of 1,000 iterations

The selected model is saved as `model.joblib`.

## 4. API Features

The API provides the following functionality:

- Single-message intent prediction.
- Batch message prediction.
- Top-three intent predictions with confidence scores.
- Input validation.
- Confidence-based human review flag.
- Health check endpoint.

### Available Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/health` | GET | Checks API health |
| `/predict` | POST | Predicts the intent of one message |
| `/predict_batch` | POST | Predicts intents for multiple messages |
| `/docs` | GET | Interactive API documentation |

## 5. Installation and Setup

### Step 1: Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
cd web3geeks-ai-bootcamp
```

### Step 2: Create a virtual environment

```bash
python -m venv .venv
```

### Step 3: Activate the environment

For Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### Step 4: Install dependencies

```bash
pip install fastapi uvicorn pandas numpy scikit-learn joblib pytest httpx
```

### Step 5: Start the API

From the `week3/challenge` directory:

```bash
python -m uvicorn app:app --reload
```

The API will run at:

`http://127.0.0.1:8000`

Interactive documentation is available at:

`http://127.0.0.1:8000/docs`

**Note:** The trained `model.joblib` file must be present in the challenge directory before starting the API.


## 6. API Usage

### Health Check

Request:

```http
GET /health
```

Response:

```json
{
  "status": "ok"
}
```

### Single Prediction

Request:

```http
POST /predict
Content-Type: application/json
```

Example request:

```json
{
  "text": "I want to verify my identity"
}
```

Actual response:

```json
{
  "intent": "why_verify_identity",
  "confidence": 0.4345,
  "top_3": [
    {
      "intent": "why_verify_identity",
      "confidence": 0.4345
    },
    {
      "intent": "verify_my_identity",
      "confidence": 0.302
    },
    {
      "intent": "unable_to_verify_identity",
      "confidence": 0.189
    }
  ],
  "needs_human": false
}
```

The response contains:

- `intent`: Predicted intent.
- `confidence`: Confidence score of the highest prediction.
- `top_3`: Three highest-confidence intent predictions.
- `needs_human`: Indicates whether human review is required.

### Batch Prediction

Request:

```http
POST /predict_batch
Content-Type: application/json
```

Example request:

```json
[
  "I want to verify my identity",
  "My card is not working",
  "I cannot top up my account"
]
```

Actual response:

```json
[
  {
    "intent": "why_verify_identity",
    "confidence": 0.4345,
    "top_3": [
      {
        "intent": "why_verify_identity",
        "confidence": 0.4345
      },
      {
        "intent": "verify_my_identity",
        "confidence": 0.302
      },
      {
        "intent": "unable_to_verify_identity",
        "confidence": 0.189
      }
    ],
    "needs_human": false
  },
  {
    "intent": "card_not_working",
    "confidence": 0.7061,
    "top_3": [
      {
        "intent": "card_not_working",
        "confidence": 0.7061
      },
      {
        "intent": "declined_card_payment",
        "confidence": 0.0489
      },
      {
        "intent": "lost_or_stolen_card",
        "confidence": 0.0192
      }
    ],
    "needs_human": false
  },
  {
    "intent": "topping_up_by_card",
    "confidence": 0.2906,
    "top_3": [
      {
        "intent": "topping_up_by_card",
        "confidence": 0.2906
      },
      {
        "intent": "top_up_failed",
        "confidence": 0.1548
      },
      {
        "intent": "top_up_by_cash_or_cheque",
        "confidence": 0.0954
      }
    ],
    "needs_human": true
  }
]
```

The batch endpoint returns one prediction result for each input message, preserving the original input order.


## 7. Confidence Threshold and Human Review

A confidence threshold of `0.40` was selected for the API.

If the highest prediction confidence is below `0.40`, the API sets `needs_human` to `true`.

Threshold analysis:

| Threshold | Coverage | Accepted Accuracy | Human Review |
|---|---:|---:|---:|
| 0.30 | 61.88% | 95.33% | 1,174 |
| 0.40 | 48.77% | 97.14% | 1,578 |
| 0.50 | 36.30% | 98.75% | 1,962 |
| 0.60 | 25.75% | 99.12% | 2,287 |
| 0.70 | 16.75% | 99.42% | 2,564 |

### Why 0.40?

The 0.40 threshold provides a balance between automatic prediction coverage and prediction reliability.

At this threshold:

- 1,502 predictions are accepted automatically.
- 1,578 predictions are flagged for human review.
- Automatic coverage is 48.77%.
- Accepted prediction accuracy is 97.14%.

A higher threshold improves accepted accuracy but sends more messages for human review.

## 8. Input Validation

The API applies the following validation rules:

- Empty messages are rejected.
- Blank messages are rejected.
- Messages longer than 500 characters are rejected.
- Invalid inputs return HTTP 422.

## 9. Confusion Analysis

The following intent pairs were among the most frequently confused by the model on the test dataset.

### Pair 1: verify_my_identity and why_verify_identity

Total confusion: 10

Both intents discuss identity verification. However, one focuses on verifying identity, while the other asks why identity verification is necessary.

### Pair 2: top_up_failed and top_up_reverted

Total confusion: 8

Both intents involve unsuccessful top-up transactions. The model sometimes struggles to distinguish between a failed transaction and a reversed transaction.

### Pair 3: card_acceptance and card_not_working

Total confusion: 8

Both intents relate to card usage problems. However, card acceptance concerns where a card is accepted, while card not working concerns card functionality.

### Additional Observation

The model also confused `getting_virtual_card` with `virtual_card_not_working` 10 times, all in one direction.

This suggests that the model sometimes struggles to distinguish between requesting a virtual card and experiencing a problem with one.

## 10. Automated Testing

The API was tested using pytest.

Run the tests from the repository root:

```bash
python -m pytest week3/challenge/test_app.py -v
```

### Test Results

**7 tests passed successfully.**

The tests cover:

1. Health endpoint.
2. Single-message prediction.
3. Blank message validation.
4. Messages exceeding 500 characters.
5. Batch prediction.
6. Batch prediction order preservation.
7. Blank messages in batch prediction.

## 11. Project Files

```text
week3/challenge/
│
├── data/
│   ├── train.csv
│   └── test.csv
│
├── app.py
├── model.joblib
├── score_log.md
├── test_app.py
├── threshold_analysis.py
├── train_model.py
└── README.md
```

## 12. Future Improvements

- Improve classification of frequently confused intent pairs.
- Experiment with additional machine learning models.
- Improve prediction reliability for difficult messages.
- Add more comprehensive API testing.
- Explore better confidence calibration.

## 13. Conclusion

This project demonstrates how machine learning can be used to classify banking customer support messages into relevant intents.

The selected Logistic Regression model achieved 85.88% accuracy and 85.81% macro F1.

The API supports single and batch predictions, confidence-based human review, and input validation.

Automated testing confirmed that all seven implemented tests pass successfully.