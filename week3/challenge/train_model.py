
import pandas as pd
import joblib

from sklearn.naive_bayes import MultinomialNB
from sklearn.dummy import DummyClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, f1_score


# Load training and test data
train = pd.read_csv("week3/challenge/data/train.csv")
test = pd.read_csv("week3/challenge/data/test.csv")

X_train = train["text"]
y_train = train["category"]

X_test = test["text"]
y_test = test["category"]


def evaluate_model(name, model):
    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)

    # Get the three highest-confidence predictions
    top_three_indices = probabilities.argsort(axis=1)[:, -3:]
    classes = model.classes_

    top_three = classes[top_three_indices]

    top3_correct = sum(
        actual in predicted
        for actual, predicted in zip(y_test, top_three)
    )

    accuracy = accuracy_score(y_test, predictions)
    macro_f1 = f1_score(y_test, predictions, average="macro")
    top3_accuracy = top3_correct / len(y_test)

    print(f"\n{name}")
    print("-" * 40)
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Macro F1: {macro_f1:.4f}")
    print(f"Top 3 Accuracy: {top3_accuracy:.4f}")

    return accuracy, macro_f1, top3_accuracy


# BASELINE
baseline = DummyClassifier(strategy="prior")
baseline.fit(X_train, y_train)

baseline_scores = evaluate_model("BASELINE", baseline)


# MODEL 1: TF-IDF + LOGISTIC REGRESSION
logistic_model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2),
            min_df=2,
            sublinear_tf=True
        )
    ),
    (
        "classifier",
        LogisticRegression(
            max_iter=1000,
            random_state=42
        )
    )
])

logistic_model.fit(X_train, y_train)

logistic_scores = evaluate_model(
    "LOGISTIC REGRESSION",
    logistic_model
)

# Save the first trained model
joblib.dump(
    logistic_model,
    "week3/challenge/model.joblib"
)

print("\nFirst model saved successfully!")

# MODEL 2: TF-IDF + MULTINOMIAL NAIVE BAYES

nb_model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2),
            min_df=2,
            sublinear_tf=True
        )
    ),
    (
        "classifier",
        MultinomialNB(alpha=0.1)
    )
])

nb_model.fit(X_train, y_train)

nb_scores = evaluate_model(
    "MULTINOMIAL NAIVE BAYES",
    nb_model
)