import pandas as pd
import os

#print(os.getcwd())
# Load dataset
filename = 'Home_and_Kitchen.csv'
file_directory = os.path.join(os.getcwd(), 'data', filename)
data = pd.read_csv(file_directory)

# Count interactions per item and user
item_counts = data['parent_asin'].value_counts()
user_counts = data['user_id'].value_counts()

# Define thresholds
min_item_interactions = 5
min_user_interactions = 5

# Filter out items and users with fewer interactions than the thresholds
filtered_data = data[(data['parent_asin'].isin(item_counts[item_counts >= min_item_interactions].index)) &
                     (data['user_id'].isin(user_counts[user_counts >= min_user_interactions].index))]

# Save filtered dataset
filtered_data.to_csv('filtered_data.csv', index=False)