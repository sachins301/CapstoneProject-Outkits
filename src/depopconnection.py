import http.client
import json
import re
import time
from urllib.parse import quote

from openpyxl import Workbook
from pandas import DataFrame


class DepopConnection:
    def __init__(self, logger):
        self.logger = logger

    # Function to create a keyword query for multiple search terms
    def create_keyword_query(self, keywords):
        return quote(" ".join(keywords))

    def clean_cell_value(self, value):
        if isinstance(value, str):
            # Remove non-printable characters
            value = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', value)
        return value

    def connect(self):
        conn = http.client.HTTPSConnection("depop-thrift.p.rapidapi.com")

        # Set up headers
        headers = {
            'x-rapidapi-key': "e68937903dmsh53a9dc44eeefef1p1b6bedjsn8e1076d22514",
            'x-rapidapi-host': "depop-thrift.p.rapidapi.com"
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
            keywords = query.split(" ")
            keyword_query = self.create_keyword_query(keywords)
            self.logger.info(f"Requesting data for query from Depop: {query}")  # Debugging statement

            try:
                # Make the GET request with the correct headers
                conn.request("GET", f"/search?page=100&keyword={keyword_query}&countryCode=us&sortBy=newlyListed",
                             headers=headers)
                res = conn.getresponse()
                data = res.read()

                if res.status != 200:
                    self.logger.info(f"Error in Depop connections status code: {res.status}")
                else:
                    # Decode the JSON response
                    decoded_data = json.loads(data.decode("utf-8"))

                    # Create a new sheet for each query
                    ws = wb.create_sheet(title=query[:31])  # Excel sheet names are limited to 31 characters

                    # Print the JSON response to understand its structure (for debugging)
                    # print(json.dumps(decoded_data, indent=4))

                    # Check if decoded_data is a list
                    if isinstance(decoded_data, list):
                        items = decoded_data
                    else:
                        # Adjust the following key to match the actual structure of the response
                        items = decoded_data.get('products', [])

                    if items:
                        # Assuming each item in 'products' is a dictionary
                        response_headers = items[0].keys() if items else []
                        ws.append(list(response_headers))
                        for item in items:
                            row = []
                            for header in response_headers:
                                cell_value = item.get(header, '')
                                # Convert complex structures to strings
                                if isinstance(cell_value, (list, dict)):
                                    cell_value = json.dumps(cell_value)
                                # Clean the cell value
                                cell_value = self.clean_cell_value(cell_value)
                                row.append(cell_value)
                            ws.append(row)
                    else:
                        self.logger.info(f"No items found for query: {query}")

            except Exception as ex:
                self.logger.error(f"Error in Depop connections", ex)

            time.sleep(1.0)

        # Save the workbook to a file
        wb.save("../resources/outputdepop.xlsx")
        self.logger.info("Search results have been saved to ../resources/outputdepop.xlsx.")

        return None
