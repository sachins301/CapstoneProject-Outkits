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

# Establish a connection to the MERCARI API
conn = http.client.HTTPSConnection("mercari.p.rapidapi.com")
headers = {
    'X-RapidAPI-Key': "e68937903dmsh53a9dc44eeefef1p1b6bedjsn8e1076d22514",
    'X-RapidAPI-Host': "mercari.p.rapidapi.com"
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

# Create a new Excel workbook and a single worksheet
wb = Workbook()
ws = wb.active
ws.title = "Search Results"

# Add headers to the worksheet
response_headers = ['Name (listing title)', 'Price', 'Size', 'Gender', 'URL']
ws.append(response_headers)

# Process each query
for query in queries:
    formatted_query = query.replace(" ", "%20")
    print(f"Requesting data for query: {query}")  # Debugging statement

    # Make the GET request with the correct headers
    conn.request("GET", f"/Mercari/Search?page=1&query={formatted_query}", headers=headers)
    res = conn.getresponse()
    data = res.read()

    # Decode the JSON response
    decoded_data = json.loads(data.decode("utf-8"))

    if isinstance(decoded_data, list) and decoded_data:
        for item in decoded_data:
            name = item.get('name', '')
            price = item.get('price', '')
            size_dict = item.get('itemSize', {})
            size = size_dict.get('name', '') if isinstance(size_dict, dict) else ''
            size = size.split(' ')[0].replace(',', '').replace('(', '').replace(')', '').replace(" ", '0')
            gender = item.get('categoryTitle', '')
            url = item.get('url', '')
            row = [name, price, size, gender, url]
            ws.append(row)

# Save the workbook to a file
wb.save("outputmercari.xlsx")
print("Search results have been saved to outputmercari.xlsx.")
