import os
import numpy as np
import pandas as pd
import random

# Set random seed for reproducibility
np.random.seed(42)

# Parameters for the dataset
num_users = 100  # Number of users
num_movies = 50  # Number of movies
min_rating = 1  # Minimum rating value
max_rating = 5  # Maximum rating value

# Generate random user IDs
user_ids = np.arange(1, num_users + 1)

# Generate random movie IDs
movie_ids = np.arange(1, num_movies + 1)

# Create an empty list to hold the data
ratings_data = []

# Generate random ratings
for user_id in user_ids:
    num_ratings = random.randint(10, num_movies)  # Each user rates a random number of movies
    rated_movies = random.sample(list(movie_ids), num_ratings)

    for movie_id in rated_movies:
        rating = random.randint(min_rating, max_rating)
        ratings_data.append([user_id, movie_id, rating])

# Convert the list into a DataFrame
ratings_df = pd.DataFrame(ratings_data, columns=['user_id', 'movie_id', 'rating'])

# Ensure the 'data' directory exists
os.makedirs('data', exist_ok=True)

# Save the DataFrame to a CSV file in the 'data' directory
ratings_df.to_csv(os.path.join('data', 'movie_ratings.csv'), index=False)

print("movie_ratings.csv file has been generated in the 'data' folder.")
