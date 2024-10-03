import os
import re

import pandas as pd


# Function to parse the log file and extract information
def parse_logs(log_file):
    training_status = []
    data_processing_status = []
    rmse_results = []

    with open(log_file, 'r') as file:
        for line in file:
            # Extract data processing messages
            if "Processing" in line:
                data_processing_status.append(line.strip())

            # Extract model training messages
            if "Fitting SVD model..." in line or "Model fitting completed." in line:
                training_status.append(line.strip())

            # Extract RMSE calculation results
            if "RMSE" in line:
                rmse_results.append(line.strip())

    return training_status, data_processing_status, rmse_results


# Function to display the entire log file content
def display_log_file(log_file):
    print("\n=== Complete Log File ===")
    with open(log_file, 'r') as file:
        content = file.read()
        print(content)


# Function to display parsed log information
def display_parsed_logs(training_status, data_processing_status, rmse_results, display_option):
    if display_option == 'data_processing':
        print("\n=== Data Processing Status ===")
        for status in data_processing_status:
            print(status)
    elif display_option == 'training':
        print("\n=== Training Status ===")
        for status in training_status:
            print(status)
    elif display_option == 'rmse':
        print("\n=== RMSE Results ===")
        for result in rmse_results:
            print(result)
    elif display_option == 'all':
        print("\n=== Data Processing Status ===")
        for status in data_processing_status:
            print(status)

        print("\n=== Training Status ===")
        for status in training_status:
            print(status)

        print("\n=== RMSE Results ===")
        for result in rmse_results:
            print(result)
    else:
        print("Invalid option selected.")


# Function to get the most recent log file
def get_latest_log_file(log_directory):
    # Pattern to match the log file names
    pattern = re.compile(r'recommendation_results_(\d{4}-\d{2}-\d{2})_(\d{2}-\d{2}).log')
    latest_file = None
    latest_time = None

    # List all files in the log directory
    for file_name in os.listdir(log_directory):
        match = pattern.match(file_name)
        if match:
            # Extract the date and time for comparison
            log_date_time = f"{match.group(1)} {match.group(2)}"
            log_time = pd.to_datetime(log_date_time, format='%Y-%m-%d %H-%M')

            if latest_time is None or log_time > latest_time:
                latest_time = log_time
                latest_file = file_name

    return os.path.join(log_directory, latest_file) if latest_file else None


if __name__ == "__main__":
    # Ask for the path to the log directory
    log_directory = input("Enter the directory path where the log file is stored: ")

    # Get the latest log file
    log_file = get_latest_log_file(log_directory)

    # Check if the log file exists
    if not log_file:
        print(f"No log files found in '{log_directory}'. Please check the path and try again.")
    else:
        # Display the complete log file content
        display_complete = input("Do you want to display the complete log file? (yes/no): ").strip().lower()
        if display_complete == 'yes':
            display_log_file(log_file)

        # Parse the logs
        training_status, data_processing_status, rmse_results = parse_logs(log_file)

        # Ask user which log information to display
        display_option = input(
            "Which information would you like to display? (data_processing/training/rmse/all): ").strip().lower()

        # Display the parsed log information based on user selection
        display_parsed_logs(training_status, data_processing_status, rmse_results, display_option)
