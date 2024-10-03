import http.client
import json


def get_amazon_product_info(asin):
    conn = http.client.HTTPSConnection("amazon-product-info2.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': "9783c08162msheaa6821dc0c7fa0p14b67djsn528e6ad3d309",
        'x-rapidapi-host': "amazon-product-info2.p.rapidapi.com"
    }

    try:
        # Make the request using the provided ASIN
        conn.request("GET", f"/amazon_product.php?asin={asin}", headers=headers)
        res = conn.getresponse()

        # Check for a successful response
        if res.status != 200:
            print(f"Error: Received status code {res.status} - {res.reason}")
            return None

        data = res.read()
        return data.decode("utf-8")

    except http.client.HTTPException as e:
        print(f"HTTP error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()  # Ensure the connection is closed

    return None


def extract_name_and_url(response_data):
    if response_data is None:
        return None, None

    # Parse the response data as JSON
    try:
        response_json = json.loads(response_data)

        # Extract the name and URL
        product_name = response_json.get('body', {}).get('name', 'N/A')
        product_url = response_json.get('body', {}).get('canonicalUrl', 'N/A')

        return product_name, product_url
    except json.JSONDecodeError:
        print("Error decoding JSON response.")
        return None, None
    except Exception as e:
        print(f"An unexpected error occurred while extracting data: {e}")
        return None, None


if __name__ == "__main__":
    target_asin = "B0CSQSNW62"  # Replace with your desired ASIN
    product_info = get_amazon_product_info(target_asin)

    # Extract the name and URL from the product info
    name, url = extract_name_and_url(product_info)

    if name is not None and url is not None:
        print(f"Product Name: {name}")
        print(f"Product URL: {url}")
    else:
        print("Failed to retrieve product information.")
