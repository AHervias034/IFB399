import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from scipy.sparse.linalg import svds
import os

# Load the movie ratings dataset from the 'data' directory
ratings_file_path = os.path.join('data', 'movie_ratings.csv')
ratings = pd.read_csv(ratings_file_path)

# Pivot the data to create a user-movie matrix
user_movie_matrix = ratings.pivot(index='user_id', columns='movie_id', values='rating').fillna(0)

# Convert the user-movie matrix to a numpy array
user_movie_matrix_np = user_movie_matrix.to_numpy()

# Normalize by subtracting the mean rating for each user
user_ratings_mean = np.mean(user_movie_matrix_np, axis=1)
user_movie_matrix_np_demeaned = user_movie_matrix_np - user_ratings_mean.reshape(-1, 1)

# Perform Singular Value Decomposition (SVD)
U, sigma, Vt = svds(user_movie_matrix_np_demeaned, k=10)  # k is the number of latent factors

# Convert sigma to a diagonal matrix
sigma = np.diag(sigma)

# Reconstruct the predicted ratings matrix
predicted_ratings = np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1, 1)

# Convert the predicted ratings into a DataFrame
predicted_ratings_df = pd.DataFrame(predicted_ratings, columns=user_movie_matrix.columns)


# Function to recommend movies for a given user
def recommend_movies(user_id, num_recommendations=5):
    # Get the user's predicted ratings
    user_row_number = user_id - 1  # Adjust for zero-indexing
    sorted_user_predictions = predicted_ratings_df.iloc[user_row_number].sort_values(ascending=False)

    # Get the user's actual data and filter out movies already rated
    user_data = ratings[ratings.user_id == user_id]
    recommendations = sorted_user_predictions[~sorted_user_predictions.index.isin(user_data.movie_id)].head(
        num_recommendations)

    return recommendations


# Example usage: Recommend 5 movies for user with ID 1
user_id = 1
recommendations = recommend_movies(user_id, num_recommendations=5)
print(f"Top 5 movie recommendations for User {user_id}:\n{recommendations}")
