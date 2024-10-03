import os
import numpy as np
import pickle  # Import pickle for loading the results
import re
import pandas as pd  # Import pandas for datetime handling


# Function to recommend items using SVD
def recommend_items(user_id, svd, train_sparse, user_mapping, item_mapping, reverse_item_mapping, top_n=10):
    if user_id not in user_mapping:
        print(f"User ID {user_id} not found.")
        return None

    user_idx = user_mapping[user_id]

    # Get the latent vector for the user
    user_latent_vector = svd.transform(train_sparse[user_idx, :])

    # Flatten user_latent_vector if it's 2D
    if user_latent_vector.ndim > 1:
        user_latent_vector = user_latent_vector.flatten()

    item_latent_vectors = svd.components_

    # Calculate predicted ratings
    predicted_ratings = np.dot(user_latent_vector, item_latent_vectors)

    # Exclude already rated items
    user_ratings = train_sparse[user_idx, :].toarray().flatten()
    rated_items = np.where(user_ratings > 0)[0]
    predicted_ratings[rated_items] = -np.inf

    # Get the top N recommendations
    recommended_item_indices = np.argsort(predicted_ratings)[::-1][:top_n]
    recommended_items = [reverse_item_mapping[idx] for idx in recommended_item_indices]

    return recommended_items


# Function to get the most recent results file
def get_latest_results_file(log_directory):
    pattern = re.compile(r'recommendation_results_(\d{4}-\d{2}-\d{2})_(\d{2}-\d{2})\.pkl')
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
    # Specify the directory for the pickle file
    log_directory = 'model_log'

    # Get the latest results file
    results_file = get_latest_results_file(log_directory)

    # Load the results from the pickle file
    if not results_file or not os.path.exists(results_file):
        print(f"Pickle file '{results_file}' not found. Please check the path.")
    else:
        with open(results_file, "rb") as f:
            svd, train_sparse, user_mapping, item_mapping, reverse_user_mapping, reverse_item_mapping, valid_rmse, test_rmse = pickle.load(
                f)

        # Ask the user for a user ID and the number of recommendations to display
        user_id = input("Enter user ID to get recommendations: ")

        # Determine the maximum number of items available for recommendation
        max_items = len(item_mapping)  # Get the total number of items

        # Set top_n to 20 if max_items is greater than 20, else use max_items
        top_n = min(max_items, 20)

        user_input_top_n = int(input(
            f"Enter the number of recommended items to display (max {top_n}): "))  # Specify number of recommendations
        top_n = min(user_input_top_n, top_n)  # Ensure top_n does not exceed max_items or 20

        # Call the recommend_items function
        user_recommendations = recommend_items(user_id, svd, train_sparse, user_mapping, item_mapping,
                                               reverse_item_mapping, top_n)

        # Display recommendations
        if isinstance(user_recommendations, list):
            print(f"Recommended items for user {user_id}: {user_recommendations}")
        else:
            print(user_recommendations)
