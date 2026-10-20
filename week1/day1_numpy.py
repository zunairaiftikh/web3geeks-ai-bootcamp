
import sys
import numpy as np


def get_numbers():
    if len(sys.argv) > 2 and sys.argv[1] == "--file":
        with open(sys.argv[2], "r") as file:
            text = file.read()
    else:
        text = " ".join(sys.argv[1:])

    numbers = [
        float(value)
        for value in text.replace(",", " ").split()
    ]

    if len(numbers) == 0:
        raise ValueError("Please provide some numbers.")

    return np.array(numbers)


def main():
    numbers = get_numbers()

    count = len(numbers)
    mean = np.mean(numbers)
    median = np.median(numbers)
    minimum = np.min(numbers)
    maximum = np.max(numbers)
    std_dev = np.std(numbers)

    outliers = numbers[np.abs(numbers - mean) > 2 * std_dev]

    print("Count:", count)
    print("Mean:", round(float(mean), 2))
    print("Median:", round(float(median), 2))
    print("Minimum:", minimum)
    print("Maximum:", maximum)
    print("Standard deviation:", round(float(std_dev), 2))
    print("Potential outliers:", outliers.tolist())


try:
    main()
except (ValueError, OSError, IndexError) as error:
    print("Error:", error)
