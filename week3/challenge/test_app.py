
from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict():
    response = client.post(
        "/predict",
        json={"text": "I am waiting for my new card"}
    )

    assert response.status_code == 200
    assert "intent" in response.json()
    assert "confidence" in response.json()
    assert "top_3" in response.json()
    assert "needs_human" in response.json()


def test_blank_message():
    response = client.post(
        "/predict",
        json={"text": "   "}
    )

    assert response.status_code == 422


def test_message_over_500_characters():
    response = client.post(
        "/predict",
        json={"text": "a" * 501}
    )

    assert response.status_code == 422


def test_batch_prediction():
    messages = [
        "I am waiting for my card",
        "My cash withdrawal failed",
        "I want to check my balance"
    ]

    response = client.post(
        "/predict_batch",
        json=messages
    )

    assert response.status_code == 200
    assert len(response.json()) == 3
    assert all("intent" in item for item in response.json())


def test_batch_preserves_order():
    messages = [
        "I am waiting for my card",
        "My cash withdrawal failed"
    ]

    batch = client.post("/predict_batch", json=messages).json()

    individual = [
        client.post("/predict", json={"text": message}).json()
        for message in messages
    ]

    assert [x["intent"] for x in batch] == [
        x["intent"] for x in individual
    ]


def test_batch_rejects_blank_message():
    response = client.post(
        "/predict_batch",
        json=["My card is missing", "   "]
    )

    assert response.status_code == 422
