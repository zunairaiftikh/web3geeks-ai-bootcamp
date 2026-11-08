
import pandas as pd

# Load only the training dataset
df = pd.read_csv("week3/challenge/data/train.csv")

print("DATASET OVERVIEW")
print("----------------")
print("Shape:", df.shape)
print("Columns:", df.columns.tolist())

print("\nMISSING VALUES")
print(df.isnull().sum())

print("\nDUPLICATE MESSAGES")
print(df.duplicated().sum())

print("\nNUMBER OF INTENTS")
print(df["category"].nunique())

print("\nMESSAGES PER INTENT")
print(df["category"].value_counts())

print("\nSAMPLE CUSTOMER MESSAGES")
for i in range(5):
    print(f"\nMessage: {df['text'].iloc[i]}")
    print(f"Intent: {df['category'].iloc[i]}")
