import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

# Find the folder where this Python file is saved.
BASE_DIR = Path(__file__).resolve().parent

# Locate the original dataset.
INPUT_FILE = BASE_DIR / "chipotle.tsv"


def main():
    # Load the tab-separated data into a DataFrame.
    df = pd.read_csv(INPUT_FILE, sep="\t")

    # Display the dataset's size.
    print("Dataset shape:", df.shape)

    # Display column types and non-missing counts.
    print("\nDataset information:")
    df.info()

    # Calculate missing values as percentages.
    print("\nMissing values (%):")
    print((df.isna().mean() * 100).round(2))

    # Count rows that duplicate earlier rows.
    print("\nDuplicate rows:", df.duplicated().sum())

    # Check how prices are written.
    print("\nExample prices:")
    print(df["item_price"].head(10).tolist())

    # Display some duplicate records.
    print("\nExample duplicate rows:")
    print(df[df.duplicated(keep=False)].head(10))

    # Remove exact duplicate rows to avoid counting repeated records twice.
    df = df.drop_duplicates()

    # Remove currency symbols and surrounding spaces before numeric conversion.
    df["item_price"] = (
        df["item_price"]
        .str.replace("$", "", regex=False)
        .str.strip()
        .astype(float)
    )

    # Check the cleaned data.
    print("\nCleaned dataset shape:", df.shape)
    print("Duplicates remaining:", df.duplicated().sum())

    # Save the cleaned dataset as a CSV file.
    output_file = BASE_DIR / "orders_clean.csv"
    df.to_csv(output_file, index=False)
    print("Cleaned data saved to:", output_file)

    # Count the most frequently ordered items.
    top_items = df.groupby("item_name")["quantity"].sum().sort_values(
        ascending=False
    )
    print("\nTop 5 items by quantity:")
    print(top_items.head(5))

    # Sum each order line's price to calculate sales per item.
    item_sales = (
        df.groupby("item_name")["item_price"]
        .sum()
        .sort_values(ascending=False)
    )

    print("\nTop 5 items by sales:")
    print(item_sales.head(5))

    # Calculate the total quantity and number of unique orders.
    print("\nTotal items ordered:", df["quantity"].sum())
    print("Unique orders:", df["order_id"].nunique())

    # Compare the quantities of the five most ordered items.
    top_items.head(5).sort_values().plot(kind="barh")

    plt.title("Top 5 Items by Quantity")
    plt.xlabel("Quantity")
    plt.ylabel("Item Name")
    plt.tight_layout()
    plt.savefig(BASE_DIR / "top_items.png")
    plt.close()

    # Compare estimated sales for the five highest-selling items.
    item_sales.head(5).sort_values().plot(kind="barh")

    plt.title("Top 5 Items by Estimated Sales")
    plt.xlabel("Estimated Sales ($)")
    plt.ylabel("Item Name")
    plt.tight_layout()
    plt.savefig(BASE_DIR / "top_sales.png")
    plt.close()
    


if __name__ == "__main__":
    main()