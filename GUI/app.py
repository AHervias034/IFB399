import os
import random
import json
import pickle
import re
import numpy as np
import pandas as pd
from flask import Flask, render_template, request
import subprocess  # Import subprocess to run the Scrapy spider

app = Flask(__name__)

# Specify the path to the desks.json file
desks_json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'test_scrapy', 'desks.json')

# Specify the directory for the model_log
log_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts', 'model_log')

# Specify the path to the spider
spider_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'test_scrapy', 'test_scrapy', 'spiders', 'quotes_spider.py')

# Function to get the latest results file
def get_latest_results_file():
    pattern = re.compile(r'recommendation_results_(\d{4}-\d{2}-\d{2})_(\d{2}-\d{2})\.pkl')
    latest_file = None
    latest_time = None

    for file_name in os.listdir(log_directory):
        match = pattern.match(file_name)
        if match:
            log_date_time = f"{match.group(1)} {match.group(2)}"
            log_time = pd.to_datetime(log_date_time, format='%Y-%m-%d %H-%M')

            if latest_time is None or log_time > latest_time:
                latest_time = log_time
                latest_file = file_name

    return os.path.join(log_directory, latest_file) if latest_file else None


# Function to recommend items using SVD
def recommend_items(user_id, top_n=100):  # Increase top_n to ensure enough recommendations
    results_file = get_latest_results_file()

    if not results_file or not os.path.exists(results_file):
        return None

    with open(results_file, "rb") as f:
        svd, train_sparse, user_mapping, item_mapping, reverse_user_mapping, reverse_item_mapping, valid_rmse, test_rmse = pickle.load(
            f)

    if user_id not in user_mapping:
        return None

    user_idx = user_mapping[user_id]
    user_latent_vector = svd.transform(train_sparse[user_idx, :]).flatten()
    item_latent_vectors = svd.components_

    predicted_ratings = np.dot(user_latent_vector, item_latent_vectors)
    user_ratings = train_sparse[user_idx, :].toarray().flatten()
    rated_items = np.where(user_ratings > 0)[0]
    predicted_ratings[rated_items] = -np.inf

    # Recommend more items to ensure enough valid ones
    recommended_item_indices = np.argsort(predicted_ratings)[::-1][:top_n]
    recommended_items = [reverse_item_mapping[idx] for idx in recommended_item_indices]

    return recommended_items


# Function to scrape product details from Amazon using Scrapy
def scrape_product_details(product_ids):
    products_details = []

    # Create a comma-separated string of URLs
    urls = ','.join([f"https://www.amazon.com/dp/{product_id}" for product_id in product_ids])

    # Before running the spider, ensure output.json is removed if it exists
    output_json_path = 'output.json'
    if os.path.exists(output_json_path):
        os.remove(output_json_path)  # Remove the file to ensure it's recreated with fresh data

    # Call the Scrapy spider using subprocess with the URLs as an argument
    result = subprocess.run(
        ['scrapy', 'runspider', spider_path, '-a', f'urls={urls}', '-o', output_json_path],
        capture_output=True, text=True
    )

    # Load the results from the JSON output file if it was created
    if os.path.exists(output_json_path):
        with open(output_json_path) as f:
            data = json.load(f)
            products_details.extend(data)

    # Overwrite the scraped_products.json file with the new scraped data
    scraped_products_path = 'scraped_products.json'
    with open(scraped_products_path, 'w') as f:
        json.dump(products_details, f, indent=4)

    return products_details

@app.route('/', methods=['GET', 'POST'])
def index():
    products = []
    recommendations = []
    scraped_details = []  # Store scraped details

    # Load product data from desks.json
    if os.path.exists(desks_json_path):
        with open(desks_json_path) as f:
            products = json.load(f)

    # Filter products with title and jpg images
    products = [p for p in products if p.get('title') and p.get('image_url', '').endswith('.jpg')]

    # Select 6 random products or placeholders
    if products:
        random_products = random.sample(products, min(len(products), 6))
    else:
        random_products = [{'title': 'Placeholder', 'image_url': 'placeholder.jpg', 'product_url': '#'}] * 6

    # Handle form submission
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        recommendations = recommend_items(user_id, top_n=100)  # Recommend more items to ensure valid ones

        # If recommendations are found, scrape their details
        if recommendations:
            scraped_details = scrape_product_details(recommendations)

            # Filter out items without a title or non-jpg images
            valid_items = [item for item in scraped_details if item.get('title') and item.get('image_url', '').endswith('.jpg')]
            invalid_items = [item for item in scraped_details if not (item.get('title') and item.get('image_url', '').endswith('.jpg'))]

            # Prioritize valid items and fill the rest with invalid items or placeholders
            scraped_details = valid_items[:6]  # Take up to 6 valid items
            if len(scraped_details) < 6:
                scraped_details += invalid_items[:6 - len(scraped_details)]  # Add invalid items if needed
            if len(scraped_details) < 6:
                scraped_details += [{'title': 'Placeholder', 'image_url': 'placeholder.jpg', 'product_url': '#'}] * (6 - len(scraped_details))  # Add placeholders if still under 6

    return render_template('index.html', products=random_products, recommendations=recommendations, scraped_details=scraped_details)

if __name__ == '__main__':
    app.run(debug=True)
