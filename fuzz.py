# fuzz.py
import random
import statistics
import pandas as pd
import os
import traceback
import time
import logging
from unittest.mock import patch
from empirical.report import Average, Median, reportProp, reportDensity, giveTimeStamp


#All methods are found in empirical folder an look at report.

# Logging function for bugs
def log_bug(method_name, inputs, exception):
    """Logs bugs discovered during fuzzing."""
    with open("fuzzing_results.log", "a") as log_file:
        log_file.write(f"Bug in {method_name}\n")
        log_file.write(f"Inputs: {inputs}\n")
        log_file.write(f"Exception: {traceback.format_exc()}\n")
        log_file.write("-" * 80 + "\n")

# Fuzzing the `Average` method
def fuzz_Average():
    try:
        Mylist = [random.uniform(-1e6, 1e6) for _ in range(random.randint(0, 50))]  # Empty list to large list
        result = Average(Mylist)
    except Exception as e:
        log_bug("Average", Mylist, e)

# Fuzzing the `Median` method
def fuzz_Median():
    try:
        Mylist = [random.uniform(-1e6, 1e6) for _ in range(random.randint(0, 50))]
        result = Median(Mylist)
    except Exception as e:
        log_bug("Median", Mylist, e)

# Fuzzing the `reportProp` method
def fuzz_reportProp():
    try:
        # Generate a random CSV file
        filename = "test_fuzz_reportProp.csv"
        generate_random_csv(filename)
        reportProp(filename)
        os.remove(filename)
    except Exception as e:
        log_bug("reportProp", filename, e)

# Fuzzing the `reportDensity` method
def fuzz_reportDensity():
    try:
        # Generate a random CSV file
        filename = "test_fuzz_reportDensity.csv"
        generate_random_csv(filename)
        reportDensity(filename)
        os.remove(filename)
    except Exception as e:
        log_bug("reportDensity", filename, e)


def fuzz_giveTimeStamp():
    # List of test timestamps
    test_timestamps = [
        -1e10,   # Far in the past (negative epoch time)
        0,       # Epoch start
        1e10,    # Far in the future
        1e9,     # Standard large timestamp
        time.time()  # Current time
    ]

    # Test each timestamp
    for ts in test_timestamps:
        try:
            # Mock time.time() to return the test timestamp
            with patch('time.time', return_value=ts):
                result = giveTimeStamp()
                logging.info(f"giveTimeStamp() with mocked time.time()={ts} -> {result}")
        except Exception as e:
            log_bug("giveTimeStamp", ts, e)

# Generate a random CSV file for fuzzing
def generate_random_csv(filename):
    """Generates a random CSV file with appropriate columns for fuzzing."""
    categories = [
        'DATA_LOAD_COUNT', 'MODEL_LOAD_COUNT', 'DATA_DOWNLOAD_COUNT',
        'MODEL_LABEL_COUNT', 'MODEL_OUTPUT_COUNT', 'DATA_PIPELINE_COUNT',
        'ENVIRONMENT_COUNT', 'STATE_OBSERVE_COUNT', 'TOTAL_EVENT_COUNT'
    ]
    num_rows = random.randint(1, 100)
    data = {
        'CATEGORY': random.choices(categories, k=num_rows),
        'PROP_VAL': [random.uniform(0, 1e6) for _ in range(num_rows)],
        'EVENT_DENSITY': [random.uniform(0, 1e6) for _ in range(num_rows)],
    }
    pd.DataFrame(data).to_csv(filename, index=False)

# Main fuzzing loop
def main():
    fuzz_Average()
    fuzz_Median()
    fuzz_reportProp()
    fuzz_reportDensity()
    fuzz_giveTimeStamp()

if __name__ == "__main__":
    main()
