
import pandas as pd
import joblib
from sklearn.metrics import accuracy_score

model = joblib.load("week3/challenge/model.joblib")
test = pd.read_csv("week3/challenge/data/test.csv")

y_test = test["category"].to_numpy()

probabilities = model.predict_proba(test["text"])
predictions = model.classes_[probabilities.argmax(axis=1)]
confidence = probabilities.max(axis=1)

print("\nCONFIDENCE THRESHOLD ANALYSIS")
print("=" * 45)

for threshold in [0.30, 0.40, 0.50, 0.60, 0.70]:
    accepted = confidence >= threshold

    accepted_count = int(accepted.sum())
    human_count = int((~accepted).sum())

    coverage = accepted_count / len(y_test)

    if accepted_count:
        accuracy = accuracy_score(
            y_test[accepted],
            predictions[accepted]
        )
    else:
        accuracy = 0

    print(f"\nThreshold: {threshold:.2f}", flush=True)
    print(f"Accepted: {accepted_count}", flush=True)
    print(f"Human review: {human_count}", flush=True)
    print(f"Coverage: {coverage:.2%}", flush=True)
    print(f"Accepted accuracy: {accuracy:.2%}", flush=True)

print("\nAnalysis completed!", flush=True)
