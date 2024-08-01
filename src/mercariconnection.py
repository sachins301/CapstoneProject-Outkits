import http.client
import json
import os
import sys
import logging
from openpyxl import Workbook
from pandas import DataFrame

from src import commonutil


class MercariConnection:
    def __init__(self, logger):
        self.logger = logger

    def connect(self):

        conn = http.client.HTTPSConnection("mercari.p.rapidapi.com")
        headers = {
            'X-RapidAPI-Key': "e68937903dmsh53a9dc44eeefef1p1b6bedjsn8e1076d22514",
            'X-RapidAPI-Host': "mercari.p.rapidapi.com"
        }

        # Read JSON data from a file
        keywords = []
        try:
            # for executable
            keyword_path = commonutil.resource_path("/config/keywords.json")
            # for local machine
            # keyword_path = "../config/keywords.json"
            self.logger.info(f"Reading Keywords from {keyword_path}")
            with open(keyword_path, "r") as file:
                kwjson = json.load(file)
            # Fetch keywords list
            keywords = kwjson["keywords"]
        except Exception as ex:
            self.logger.error("Failed to read keyword config", ex)


        # Create a new Excel workbook and a single worksheet
        wb = Workbook()
        ws = wb.active
        ws.title = "Search Results"

        # Add headers to the worksheet
        response_headers = ['Listing Date', 'Name', 'Price', 'Size', 'Gender', 'URL', 'Image']
        ws.append(response_headers)

        # Process each query
        for query in keywords:
            formatted_query = query.replace(" ", "%20")
            self.logger.info(f"Requesting data for query: {query}")

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
                    photos = item.get('photos', [])
                    first_image_url = photos[0].get('imageUrl', '') if photos else ''
                    row = ['', name, price, size, gender, url, first_image_url]  # Blank column for listing date
                    ws.append(row)


        # Save the workbook to a file
        wb.save("outputmercari.xlsx")
        self.logger.info("Search results have been saved to outputmercari.xlsx.")

        return None

# # Create a logger
# logger = logging.getLogger('MercariLogger')
# logger.setLevel(logging.INFO)
# logger.addHandler(logging.StreamHandler(sys.stdout))
#
# # Execute the connection
# mercari_conn = MercariConnection(logger)
# mercari_conn.connect()


