
# Banking77 Model Score Log

| Experiment | Accuracy | Macro F1 | Top-3 Accuracy | Reason |
|---|---:|---:|---:|---|
| Dummy Baseline | 0.0130 | 0.0003 | 0.0390 | Initial baseline for comparison |
| TF-IDF + Logistic Regression | 0.8588 | 0.8581 | 0.9571 | Best overall performance |
| TF-IDF + Multinomial Naive Bayes | 0.8536 | 0.8511 | 0.9468 | Good alternative, but slightly lower scores |

## Model Selection

Logistic Regression was selected because it achieved the highest
accuracy, macro F1 and top-3 accuracy among the tested models.
