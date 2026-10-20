
import sys


def get_numbers():
    if len(sys.argv) > 2 and sys.argv[1] == "--file":
        with open(sys.argv[2], "r") as file:
            text = file.read()
    else:
        text = " ".join(sys.argv[1:])

    if text.startswith("--file"):
        text = text.replace("--file", "", 1).strip()

    numbers = [
        float(value)
        for value in text.replace(",", " ").split()
    ]

    if len(numbers) == 0:
        raise ValueError("Please provide some numbers.")

    return numbers


def main():
    numbers = get_numbers()

    count = len(numbers)
    mean = sum(numbers) / count

    sorted_numbers = sorted(numbers)
    middle = count // 2

    if count % 2 == 1:
        median = sorted_numbers[middle]
    else:
        median = (
            sorted_numbers[middle - 1] + sorted_numbers[middle]
        ) / 2

    minimum = min(numbers)
    maximum = max(numbers)

    variance = sum((x - mean) ** 2 for x in numbers) / count
    std_dev = variance ** 0.5

    print("Count:", count)
    print("Mean:", round(mean, 2))
    print("Median:", round(median, 2))
    print("Minimum:", minimum)
    print("Maximum:", maximum)
    print("Standard deviation:", round(std_dev, 2))


try:
    main()
except (ValueError, OSError, IndexError) as error:
    print("Error:", error)
