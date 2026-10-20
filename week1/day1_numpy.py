
import sys
import math


def get_numbers():
    """Read numbers from command-line input or a text file."""
    if len(sys.argv) < 2:
        raise ValueError(
            "Please enter numbers or use --file followed by a file path."
        )

    if sys.argv[1] == "--file":
        if len(sys.argv) != 3:
            raise ValueError("Usage: python day1_stats_cli.py --file PATH")

        with open(sys.argv[2], "r", encoding="utf-8") as file:
            text = file.read()
    else:
        text = " ".join(sys.argv[1:])

    # Allow numbers separated by commas, spaces, or new lines.
    text = text.replace(",", " ")
    parts = text.split()

    if not parts:
        raise ValueError("No numbers were provided.")

    try:
        numbers = [float(part) for part in parts]
    except ValueError:
        raise ValueError("Invalid input. Please provide numbers only.")

    return numbers


def calculate_statistics(numbers):
    """Calculate statistics using pure Python."""
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

    # Population standard deviation: divide by n.
    variance = sum((number - mean) ** 2 for number in numbers) / count
    standard_deviation = math.sqrt(variance)

    return count, mean, median, minimum, maximum, standard_deviation


def main():
    try:
        numbers = get_numbers()
        results = calculate_statistics(numbers)

        count, mean, median, minimum, maximum, std_dev = results

        print(f"Count: {count}")
        print(f"Mean: {mean:.2f}")
        print(f"Median: {median:.2f}")
        print(f"Min: {minimum:g}")
        print(f"Max: {maximum:g}")
        print(f"Standard deviation: {std_dev:.2f}")

    except (ValueError, OSError) as error:
        print(f"Error: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
