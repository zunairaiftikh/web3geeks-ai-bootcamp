
# Week 1 — Day 1: Python Essentials and NumPy

## 1. Pure Python Statistics Tool

This program calculates count, mean, median, minimum, maximum,
and population standard deviation without NumPy.

Run with numbers:

```powershell
python .\week1\day1_stats_cli.py 10 20 30 40 50
```

Run using the sample file:

```powershell
python .\week1\day1_stats_cli.py --file .\week1\sample.txt
```

## 2. NumPy Statistics Tool

This program uses NumPy to calculate the same basic statistics
and identifies potential outliers more than two standard
deviations away from the mean.

Run with numbers:

```powershell
python .\week1\day1_numpy.py 10 20 30 40 50
```

Run using the sample file:

```powershell
python .\week1\day1_numpy.py --file .\week1\sample.txt
```

## 3. Sample Data

The `sample.txt` file contains five example values:

```text
10
20
30
40
50
```

## 4. Standard Deviation

Both programs calculate population standard deviation by default.
NumPy's `np.std()` uses `ddof=0` by default. For sample standard
deviation, use `np.std(numbers, ddof=1)`.

## 5. Run Location

Run all commands from the repository root folder:

`F:\web3geeks-ai-bootcamp`
