import http.client
import json
import re
import time
from urllib.parse import quote

import pandas as pd
from openpyxl import Workbook
from pandas import DataFrame

from src import commonutil


class PoshmarkConnection:
    def __init__(self, logger):
        self.logger = logger

    # Function to extract the number from a string and remove the last zero (only for Poshmark)
    def extract_number(self, value):
        number = ''.join(filter(str.isdigit, value))
        if number.endswith('0'):
            number = number[:-1]
        return number

    def clean_cell_value(self, value):
        if isinstance(value, str):
            # Remove non-printable characters
            value = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', value)
        return value

    def connect(self):
        conn = http.client.HTTPSConnection("poshmark.p.rapidapi.com")

        # Set the headers for the API request
        headers = {
            'X-RapidAPI-Key': "e68937903dmsh53a9dc44eeefef1p1b6bedjsn8e1076d22514",
            'X-RapidAPI-Host': "poshmark.p.rapidapi.com"
        }

        # Read JSON data from a file
        queries = []
        try:
            keyword_path = commonutil.resource_path("/config/keywords.json")
            #keyword_path = "../config/keywords.json"
            self.logger.info(f"Reading Keywords from {keyword_path}")
            with open(keyword_path, "r") as file:
                kwjson = json.load(file)
            # Fetch keywords list
            queries = kwjson["keywords"]
        except Exception as ex:
            self.logger.error("Failed to read keyword config", ex)

        # Create a new Excel workbook and a single sheet
        wb = Workbook()
        ws = wb.active
        ws.title = "All Queries"

        # Define the headers for the columns we are interested in
        dataframe_headers = ['Listing Date', 'Name', 'Price', 'Size', 'Gender', 'URL', 'Image']
        ws.append(dataframe_headers)

        # Process each query
        for query in queries:
            formatted_query = query.replace(" ", "%20")
            self.logger.info(f"Requesting data for query from Poshmark: {query}")  # Debugging statement

            try:
                # Make the GET request with the correct headers
                conn.request("GET", f"/search?query={formatted_query}&domain=com", headers=headers)
                res = conn.getresponse()
                data = res.read()

                if res.status != 200:
                    self.logger.info(f"Error in Poshmark connections status code: {res.status}")
                else:

                    # Decode the JSON response
                    decoded_data = json.loads(data.decode("utf-8"))

                    # Adjust the following key to match the actual structure of the response
                    items = decoded_data.get('data', [])

                    if items:
                        for item in items:
                            # Extract listing date and format as MM-DD-YYYY
                            listing_date = item.get('first_available_at', '')
                            formatted_listing_date = pd.to_datetime(listing_date).strftime(
                                '%m-%d-%Y') if listing_date else ''

                            title = item.get('title', '')
                            price = self.extract_number(item.get('price_amount', {}).get('val', ''))
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
                            row = [self.clean_cell_value(cell) for cell in row]
                            ws.append(row)
                    else:
                        self.logger.info(f"No items found for query: {query}")
            except Exception as ex:
                self.logger.error(f"Error in Poshmark connections", ex)
            time.sleep(1.0)

        # Save the workbook to a file
        wb.save("outputposhmark.xlsx")
        self.logger.info("Search results have been saved to outputposhmark.xlsx.")

        return None
