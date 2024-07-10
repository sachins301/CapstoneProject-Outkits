#07/10/24 RF - added column listing date before the name column 

import http.client
import json
import time
import pandas as pd
from openpyxl import Workbook
import re
import requests
from pandas import json_normalize
from urllib.parse import quote
import importlib.util
import os
import smtplib
from email.message import EmailMessage

# Function to extract the number from a string and remove the last zero (only for Poshmark)
def extract_number(value):
    number = ''.join(filter(str.isdigit, value))
    if number.endswith('0'):
        number = number[:-1]
    return number

# Function to clean the cell value
def clean_cell_value(value):
    if isinstance(value, str):
        # Remove non-printable characters
        value = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', value)
    return value

# Establish a connection to the Poshmark API
conn = http.client.HTTPSConnection("poshmark.p.rapidapi.com")

# Set the headers for the API request
headers = {
    'X-RapidAPI-Key': "e68937903dmsh53a9dc44eeefef1p1b6bedjsn8e1076d22514",
    'X-RapidAPI-Host': "poshmark.p.rapidapi.com"
}

# List of queries to process
queries = [
    "Nike Dunk Low 6.0",
    "Nike Dunk Pro B",
    "Nike Dunk Pushead",
    "Nike SB Dunk Low Bigfoot",
    "Carhartt Hooded Jacket Red",
    "Carhartt Hooded Jacket Orange",
    "Carhartt Hooded Jacket Teal",
    "Carhartt Hooded Jacket Purple",
    "Nike SB Dunk Size 12",
    "Nike Dunk Cinder Brown",
    "Nike Dunk Light Stone Bone"
]

# Create a new Excel workbook and a single sheet
wb = Workbook()
ws = wb.active
ws.title = "All Queries"

# Define the headers for the columns we are interested in
headers = ['Listing Date', 'Name', 'Price', 'Size', 'Gender', 'URL', 'Images']
ws.append(headers)

# Process each query
for query in queries:
    formatted_query = query.replace(" ", "%20")
    print(f"Requesting data for query: {query}")  # Debugging statement

    # Make the GET request with the correct headers
    conn.request("GET", f"/search?query={formatted_query}&domain=com", headers={
        'X-RapidAPI-Key': "e68937903dmsh53a9dc44eeefef1p1b6bedjsn8e1076d22514",
        'X-RapidAPI-Host': "poshmark.p.rapidapi.com"
    })
    res = conn.getresponse()
    data = res.read()

    # Decode the JSON response
    decoded_data = json.loads(data.decode("utf-8"))

    # Print the JSON response to understand its structure (for debugging)
    #print(json.dumps(decoded_data, indent=4))

    # Adjust the following key to match the actual structure of the response
    items = decoded_data.get('data', [])

    if items:
        for item in items:
            # Extract listing date and format as MM-DD-YYYY
            listing_date = item.get('first_available_at', '')
            formatted_listing_date = pd.to_datetime(listing_date).strftime('%m-%d-%Y') if listing_date else ''

            title = item.get('title', '')
            price = extract_number(item.get('price_amount', {}).get('val', ''))
            size_obj = item.get('size_obj', {}).get('display', '')

            # Handle cases where size_obj might be an empty dictionary or None
            size = size_obj if size_obj else ''

            department = item.get('department', {}).get('display', '')

            # Construct the URL
            clean_title = title.replace(' ', '-').replace('/', '-')
            item_id = item.get('id', '')
            url = f"https://poshmark.com/listing/{clean_title}-{item_id}"

            # Extract the first image URL from "pictures"
            pictures = item.get('pictures', [])
            first_image_url = pictures[0]['url'] if pictures else ''

            row = [formatted_listing_date, title, price, size, department, url, first_image_url]
            row = [clean_cell_value(cell) for cell in row]
            ws.append(row)
    else:
        print(f"No items found for query: {query}")
    time.sleep(2.0)

# Save the workbook to a file
wb.save("outputposhmark.xlsx")
print("Search results have been saved to outputposhmark.xlsx.")
