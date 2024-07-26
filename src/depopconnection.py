import http.client
import json
import re
import time
from urllib.parse import quote

from dateutil.parser import parse
from openpyxl import Workbook
from pandas import DataFrame

from src import commonutil


class DepopConnection:
    def __init__(self, logger):
        self.logger = logger

    # Function to create a keyword query for multiple search terms
    def create_keyword_query(self, keywords):
        return quote(" ".join(keywords))

    # Function to clean the cell value
    def clean_cell_value(self, value):
        if isinstance(value, str):
            # Remove non-printable characters
            value = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', value)
        return value

    def connect(self):
        # Establish a connection to the Depop API
        conn = http.client.HTTPSConnection("depop-thrift.p.rapidapi.com")

        # Set up headers
        headers = {
            'x-rapidapi-key': "e68937903dmsh53a9dc44eeefef1p1b6bedjsn8e1076d22514",
            'x-rapidapi-host': "depop-thrift.p.rapidapi.com"
        }

        queries = []
        try:
            keyword_path = commonutil.resource_path("/config/keywords.json")
            # keyword_path = "../config/keywords.json"
            self.logger.info(f"Reading Keywords from {keyword_path}")
            with open(keyword_path, "r") as file:
                kwjson = json.load(file)
            # Fetch keywords list
            queries = kwjson["keywords"]
        except Exception as ex:
            self.logger.error("Failed to read keyword config", ex)

        self.logger.info(f"Keywords: {queries}")

        # Create a new Excel workbook and a single sheet
        wb = Workbook()
        ws = wb.active
        ws.title = "Consolidated Results"

        # Define the desired columns with the new headers and order
        desired_columns = {
            'dateCreated': 'Listing Date',
            'slug': 'Name',
            'price': 'Price',
            'sizes': 'Size',
            'url': 'URL'
        }

        # New header order with Listing Date before Name
        header_order = ['Listing Date', 'Name', 'Price', 'Size', 'Gender', 'URL', 'Image']

        # Append the headers to the sheet
        ws.append(header_order)

        # Process each query
        for query in queries:
            keywords = query.split(" ")
            keyword_query = self.create_keyword_query(keywords)
            self.logger.info(f"Requesting data for query from Depop: {query}")  # Debugging statement

            # Initialize variable to track if items were found and retry count
            items_found = False
            retries = 0
            max_retries = 3

            try:
                # Retry until items are found or max retries reached
                while not items_found and retries < max_retries:
                    # Make the GET request with the correct headers
                    conn.request("GET", f"/search?page=1&keyword={keyword_query}&countryCode=us&sortBy=newlyListed",
                    headers=headers)
                    res = conn.getresponse()
                    data = res.read()
                    time.sleep(2.0)

                    self.logger.info(f"Error in Depop connections status code: {res.status}")

                    # Decode the JSON response
                    decoded_data = json.loads(data.decode("utf-8"))

                    # Check if decoded_data is a list
                    if isinstance(decoded_data, list):
                        items = decoded_data
                    else:
                        # Adjust the following key to match the actual structure of the response
                        items = decoded_data.get('products', [])

                    # Filter items to include only those with the brand 'Nike' or 'Carhartt'
                    selected_items = [item for item in items if
                                      item.get('brand') and item.get('brand').lower() in ['nike', 'carhartt']]

                    if selected_items:
                        # Assuming each item in 'products' is a dictionary
                        items_found = True
                        self.logger.info(f"Items have been found for query: {query}")

                        for item in selected_items:
                            row = []
                            for header in header_order:
                                if header == 'Gender':
                                    cell_value = ''  # Blank column for Gender
                                elif header == 'Image':
                                    images = item.get('images', [])
                                    cell_value = images[0] if images else ''  #Get the first image URL or empty string if no images
                                elif header == 'Listing Date':
                                    date_created = item.get('dateCreated', '')
                                    if date_created:
                                        try:
                                            listing_date = parse(date_created)
                                            cell_value = listing_date.strftime("%m-%d-%Y")
                                        except ValueError:
                                            cell_value = ''
                                    else:
                                        cell_value = ''
                                else:
                                    cell_key = list(desired_columns.keys())[list(desired_columns.values()).index(header)]
                                    if cell_key == 'price':
                                        price_info = item.get('price', {})
                                        amount = float(price_info.get('amount', 0))
                                        national_shipping = float(price_info.get('nationalShipping', 0))
                                        cell_value = amount + national_shipping
                                    else:
                                        cell_value = item.get(cell_key, '')
                                    if isinstance(cell_value, (list, dict)):
                                        cell_value = json.dumps(cell_value)
                                    cell_value = self.clean_cell_value(cell_value)
                                row.append(cell_value)
                            ws.append(row)
                    else:
                        retries += 1
                        self.logger.info(f"No items found for query: {query}, retrying... (Attempt {retries}/{max_retries})")
                if not items_found:
                    print(f"Max retries reached for query: {query}. Moving on to the next keyword.")

            except Exception as ex:
                self.logger.error(f"Error in Depop connections", ex)

        # Save the workbook to a file
        wb.save("outputdepop.xlsx")
        self.logger.info("Search results have been saved to outputdepop.xlsx.")

        return None
