import http.client
import json
import re
import time
from urllib.parse import quote

from openpyxl import Workbook
from pandas import DataFrame


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
            with open("../config/keywords.json", "r") as file:
                kwjson = json.load(file)
            # Fetch keywords list
            queries = kwjson["keywords"]
        except Exception as ex:
            self.logger.error("Failed to read keyword config", ex)

        # Create a new Excel workbook
        wb = Workbook()
        wb.remove(wb.active)  # Remove the default sheet

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

                    # Create a new sheet for each query
                    ws = wb.create_sheet(title=query[:31])  # Excel sheet names are limited to 31 characters

                    # Adjust the following key to match the actual structure of the response
                    items = decoded_data.get('data', [])

                    if items:
                        # Define the headers for the columns we are interested in
                        ws.append(['Name', 'Price', 'Size', 'Gender', 'URL'])

                        for item in items:
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

                            row = [title, price, size, department, url]
                            row = [self.clean_cell_value(cell) for cell in row]
                            ws.append(row)
                    else:
                        self.logger.info(f"No items found for query: {query}")
            except Exception as ex:
                self.logger.error(f"Error in Poshmark connections", ex)
            time.sleep(0.5)

        # Save the workbook to a file
        wb.save("../resources/outputposhmark.xlsx")
        self.logger.info("Search results have been saved to ../resources/outputposhmark.xlsx.")

        return None