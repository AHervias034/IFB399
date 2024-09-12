import os
import pandas as pd
import numpy as np
import scipy.sparse as sp
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics import mean_squared_error
from concurrent.futures import ProcessPoolExecutor
import multiprocessing


# Parallel function to process a chunk of data (mapping and sparse matrix conversion)
def process_chunk(chunk, user_mapping, item_mapping):
    # Map the chunk's user_id and parent_asin to integer indices
    chunk['user_id'] = chunk['user_id'].map(user_mapping)
    chunk['parent_asin'] = chunk['parent_asin'].map(item_mapping)

    # Create the sparse matrix for the chunk
    rows = chunk['user_id'].values
    cols = chunk['parent_asin'].values
    ratings = chunk['rating'].values

    return sp.csr_matrix((ratings, (rows, cols)), shape=(len(user_mapping), len(item_mapping)))

# Function to read and process the CSV in parallel chunks
def parallel_read_and_process(csv_file, user_mapping, item_mapping, num_rows=None, chunksize=10000, n_jobs=4):
    matrices = []
    with ProcessPoolExecutor(max_workers=n_jobs) as executor:
        futures = []
        total_rows_read = 0
        for chunk in pd.read_csv(csv_file, chunksize=chunksize):
            if num_rows is not None:
                if total_rows_read >= num_rows:
                    break
                rows_to_add = min(num_rows - total_rows_read, len(chunk))
                chunk = chunk.iloc[:rows_to_add]
                total_rows_read += rows_to_add

            future = executor.submit(process_chunk, chunk, user_mapping, item_mapping)
            futures.append(future)

        for future in futures:
            matrices.append(future.result())

    return sp.vstack(matrices)


def recommend_items(user_id, svd, train_sparse, user_mapping, item_mapping, reverse_item_mapping, top_n=10):
    if user_id not in user_mapping:
        print("User ID not found.")
        return

    user_idx = user_mapping[user_id]

    # Get the latent vector for the user
    user_latent_vector = svd.transform(train_sparse[user_idx, :])

    # Flatten user_latent_vector if it's 2D
    if user_latent_vector.ndim > 1:
        user_latent_vector = user_latent_vector.flatten()

    item_latent_vectors = svd.components_

    # Calculate predicted ratings: user_latent_vector (1x100) dot item_latent_vectors.T (100x2903)
    predicted_ratings = np.dot(user_latent_vector, item_latent_vectors)

    # Exclude already rated items
    user_ratings = train_sparse[user_idx, :].toarray().flatten()
    rated_items = np.where(user_ratings > 0)[0]
    predicted_ratings[rated_items] = -np.inf

    # Get the top N recommendations
    recommended_item_indices = np.argsort(predicted_ratings)[::-1][:top_n]
    recommended_items = [reverse_item_mapping[idx] for idx in recommended_item_indices]

    return recommended_items

def run_recommendation_system(train_file, valid_file, test_file, num_train_rows=None, num_valid_rows=None,
                              num_test_rows=None):
    # Load the dataset to build user and item mappings
    all_data = pd.concat([pd.read_csv(train_file, nrows=num_train_rows),
                          pd.read_csv(valid_file, nrows=num_valid_rows),
                          pd.read_csv(test_file, nrows=num_test_rows)])

    # Create user and item mappings
    user_mapping = {user_id: idx for idx, user_id in enumerate(all_data['user_id'].unique())}
    item_mapping = {item_id: idx for idx, item_id in enumerate(all_data['parent_asin'].unique())}

    # Reverse mappings for easy lookup
    reverse_user_mapping = {v: k for k, v in user_mapping.items()}
    reverse_item_mapping = {v: k for k, v in item_mapping.items()}

    # Parallel reading, mapping, and sparse matrix creation
    print("Processing training data...")
    train_sparse = parallel_read_and_process(train_file, user_mapping, item_mapping, num_rows=num_train_rows,
                                             chunksize=100000, n_jobs=multiprocessing.cpu_count())

    print("Processing validation data...")
    valid_sparse = parallel_read_and_process(valid_file, user_mapping, item_mapping, num_rows=num_valid_rows,
                                             chunksize=10000, n_jobs=multiprocessing.cpu_count())

    print("Processing test data...")
    test_sparse = parallel_read_and_process(test_file, user_mapping, item_mapping, num_rows=num_test_rows,
                                            chunksize=10000, n_jobs=multiprocessing.cpu_count())

    # Apply TruncatedSVD for collaborative filtering
    print("Fitting SVD model...")
    svd = TruncatedSVD(n_components=100, random_state=42)
    train_svd = svd.fit_transform(train_sparse)

    # Transform validation and test data
    print("Transforming validation data...")
    valid_svd = svd.transform(valid_sparse)

    print("Transforming test data...")
    test_svd = svd.transform(test_sparse)

    # Make predictions (inverse transform)
    print("Making predictions on validation data...")
    valid_predictions = svd.inverse_transform(valid_svd)

    print("Making predictions on test data...")
    test_predictions = svd.inverse_transform(test_svd)

    # Calculate RMSE on validation data
    valid_ground_truth = valid_sparse.toarray()  # Convert sparse matrix to dense
    valid_rmse = np.sqrt(mean_squared_error(valid_ground_truth, valid_predictions))
    print(f"Validation RMSE: {valid_rmse}")

    # Calculate RMSE on test data
    test_ground_truth = test_sparse.toarray()  # Convert sparse matrix to dense
    test_rmse = np.sqrt(mean_squared_error(test_ground_truth, test_predictions))
    print(f"Test RMSE: {test_rmse}")

    return svd, train_sparse, user_mapping, item_mapping, reverse_user_mapping, reverse_item_mapping


if __name__ == "__main__":
    # Ask user for the number of rows to use
    num_train_rows = int(input("Enter the number of training rows to use (or 0 for all): "))
    num_valid_rows = int(input("Enter the number of validation rows to use (or 0 for all): "))
    num_test_rows = int(input("Enter the number of test rows to use (or 0 for all): "))

    # Set 0 to None for reading all rows
    num_train_rows = None if num_train_rows == 0 else num_train_rows
    num_valid_rows = None if num_valid_rows == 0 else num_valid_rows
    num_test_rows = None if num_test_rows == 0 else num_test_rows

    # File paths for the train, valid, and test datasets
    directory = os.path.join(os.getcwd(), 'data')
    train_file = os.path.join(directory, 'Home_and_Kitchen.train.csv')
    valid_file = os.path.join(directory, 'Home_and_Kitchen.valid.csv')
    test_file = os.path.join(directory, 'Home_and_Kitchen.test.csv')

    # Run the recommendation system
    svd, train_sparse, user_mapping, item_mapping, reverse_user_mapping, reverse_item_mapping = \
        run_recommendation_system(train_file, valid_file, test_file, num_train_rows, num_valid_rows, num_test_rows)

    # Ask for user ID and recommend items
    user_id = input("Enter user ID for recommendations: ")
    recommendations = recommend_items(user_id, svd, train_sparse, user_mapping, item_mapping, reverse_item_mapping,
                                      top_n=5)

    print(f"Recommended items for user {user_id}: {recommendations}")
