
import sys
import numpy as np


def get_numbers():
    """Read numbers from command-line input or a text file."""
    if len(sys.argv) < 2:
        raise ValueError(
            "Enter numbers or use --file followed by a file path."
        )

    if sys.argv[1] == "--file":
        if len(sys.argv) != 3:
            raise ValueError(
                "Usage: python day1_numpy.py --file PATH"
            )

        with open(sys.argv[2], "r", encoding="utf-8") as file:
            text = file.read()
    else:
        text = " ".join(sys.argv[1:])

    parts = text.replace(",", " ").split()

    if not parts:
        raise ValueError("No numbers were provided.")

    try:
        numbers = np.array([float(value) for value in parts])
    except ValueError:
        raise ValueError("Invalid input. Please enter numbers only.")

    if not np.all(np.isfinite(numbers)):
        raise ValueError("Please enter finite numbers only.")

    return numbers


def main():
    try:
        numbers = get_numbers()

        mean = np.mean(numbers)
        std_dev = np.std(numbers)
        outliers = numbers[np.abs(numbers - mean) > 2 * std_dev]

        print("Count:", len(numbers))
        print(f"Mean: {mean:.2f}")
        print(f"Median: {np.median(numbers):.2f}")
        print(f"Minimum: {np.min(numbers):g}")
        print(f"Maximum: {np.max(numbers):g}")
        print(f"Population standard deviation: {std_dev:.2f}")
        print("Potential outliers:", outliers.tolist())

    except (ValueError, OSError) as error:
        print("Error:", error)
        sys.exit(1)


if __name__ == "__main__":
    main()
