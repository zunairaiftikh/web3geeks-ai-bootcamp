# Chipotle Order Data Cleaning Report

## 1. Data Cleaning

- **Original dataset:** 4,622 rows and 5 columns.
- **Duplicate rows:** 59 exact duplicate rows were identified and removed, leaving 4,563 rows.
- **Price conversion:** Removed the dollar sign and surrounding spaces from `item_price` and converted it to a numeric data type.
- **Missing values:** `choice_description` has missing values. These were retained because the dataset does not provide enough information to fill them accurately.
- **Output:** The cleaned dataset was saved as `orders_clean.csv`.

## 2. Key Insights

1. **Most ordered item:** [Add the top item and its quantity from your latest output.] This shows which menu item had the highest total quantity ordered.
2. **Highest sales item:** [Add the top item and its corrected sales total.] This identifies the item contributing the greatest recorded sales.
3. **Order activity:** There were [add total quantity] units ordered across [add unique order count] unique orders. This gives an overview of the volume of orders.

## 3. Charts

- `top_items.png`: Compares the five items with the highest total quantities ordered.
- `top_sales.png`: Compares the five items with the highest recorded sales totals.

## 4. Limitations

Removing exact duplicate rows assumes those records were accidental duplicates. In real order data, repeated-looking rows can sometimes represent legitimate transactions, so this assumption should be checked before removing them.
