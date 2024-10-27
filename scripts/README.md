# Recommendation System

## Overview
This project implements a recommendation system using collaborative filtering techniques, specifically Singular Value Decomposition (SVD). It processes user-item rating data to make predictions and evaluate model performance.

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Usage](#usage)
- [Logging](#logging)
- [Results](#results)

## Features
- Loads and processes user-item rating data from CSV files.
- Supports parallel processing for efficiency.
- Utilizes SVD for collaborative filtering to generate recommendations.
- Evaluates model performance using Root Mean Square Error (RMSE).
- Logs key events and results to a specified log file.
- Saves model results and mappings in a pickle file for later use.

## Technologies Used
- Python 3.x
- Pandas for data manipulation
- NumPy for numerical operations
- SciPy for sparse matrix operations
- Scikit-learn for SVD and performance metrics
- Concurrent Futures for parallel processing
- Logging for tracking the application's flow
- Pickle for saving and loading model results

## Usage
1. **Prepare your dataset** in CSV format with the following columns:
   - `user_id`: The ID of the user.
   - `parent_asin`: The ID of the item (product).
   - `rating`: The rating given by the user to the item.

2. **Place your CSV files** in the `data` directory. The expected filenames are:
   - `Home_and_Kitchen.train.csv`
   - `Home_and_Kitchen.valid.csv`
   - `Home_and_Kitchen.test.csv`

## Logging
The application logs important events and errors to a specified log file. The log file will be created in the directory you specify at runtime and will follow this naming convention:

### Key Events Logged
- **Dataset Loading**: Logs when the dataset is loaded and user/item mappings are created.
- **Data Processing**: Logs the start and completion of data processing for training, validation, and test datasets.
- **Model Fitting**: Logs when the SVD model is fitted and when data transformations occur.
- **RMSE Calculation**: Logs the calculated RMSE values for validation and test datasets.
- **Errors**: Any errors or exceptions encountered during processing are logged to aid in debugging.

This logging functionality helps track the application's flow and is useful for performance analysis and troubleshooting.

## Results
After executing the script, the results will be saved in two formats:

1. **Log File**: Contains a detailed log of the entire process, including metrics and events, located at the path you specified during execution.

2. **Pickle File**: The model and associated data will be saved in a pickle file with the naming convention:

This file includes:
- The trained SVD model.
- The sparse training matrix.
- User and item mappings (both direct and reverse).
- RMSE values for validation and test datasets.

This pickle file is used later to access the model and mappings without needing to reprocess the data.


