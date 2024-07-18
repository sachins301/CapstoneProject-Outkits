import http.client
import json
import os
import sys

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
        # keywords = [
        #     "Nike Dunk MF DOOM",
        #     "Nike Dunk SB Stussy",
        #     "Nike Dunk Pushead",
        #     "Nike Dunk High SB Khaki Creed",
        #     "Nike Dunk 6.0 Hemp",
        #     "Nike Dunk SB Mocha",
        #     "Nike Dunk SB Bison",
        #     "Nike Dunk SB Mocha Choc",
        #     "Nike Dunk SB Medusa",
        #     "Nike Dunk SB Oompa Loompa",
        #     "Nike 6.0 NKE Quasar Purple",
        #     "Nike Dunk SB Crown Royal",
        #     "Nike Dunk Palm Green",
        #     "Nike Dunk Low Cargo Khaki",
        #     "Nike Dunk CL demim",
        #     "Nike Dunk Low Pro Mushroom",
        #     "Nike Dunk Low SB Tweed",
        #     "Nike Dunk Low ACG",
        #     "Dunk Low Pro Obsidian",
        #     "Dunk Low Pro Midnight Navy",
        #     "Nike Dunk Low Pro Mesa",
        #     "Dunk Low Pro B Olive",
        #     "Nike SB Dunk Trail End",
        #     "Nike SB Dunk Dusty Cactus",
        #     "Pro B Oxide"
        # ]
        keywords = []
        self.logger.info(f"Right outside the gates of keywords try")
        try:
            keyword_path = commonutil.resource_path("/config/keywords.json")
            self.logger.info(f"Reading Keywords from {keyword_path}")
            with open(keyword_path, "r") as file:
                kwjson = json.load(file)
            # Fetch keywords list
            keywords = kwjson["keywords"]
        except Exception as ex:
            self.logger.error("Failed to read keyword config", ex)

        self.logger.info(f"Keywords: {keywords}")

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
            try:
                conn.request("GET", f"/Mercari/Search?page=1&query={formatted_query}", headers=headers)
                res = conn.getresponse()
                data = res.read()

                if res.status != 200:
                    self.logger.info(f"Error in Mercari connections status code: {res.status}")

                else:
                    # Decode the JSON response
                    decoded_data = json.loads(data.decode("utf-8"))

                    # Create a new sheet for each query
                    ws = wb.create_sheet(title=query[:31])  # Excel sheet names are limited to 31 characters

                    if isinstance(decoded_data, list) and decoded_data:
                        for item in decoded_data:
                            name = item.get('name', '')
                            price = item.get('price', '')
                            size_dict = item.get('itemSize', {})
                            size = size_dict.get('name', '') if isinstance(size_dict, dict) else ''
                            size = (size.split(' ')[0]
                                    .replace(',', '')
                                    .replace('(', '')
                                    .replace(')', '')
                                    .replace(" ",'0'))
                            gender = item.get('categoryTitle', '')
                            url = item.get('url', '')
                            photos = item.get('photos', [])
                            first_image_url = photos[0].get('imageUrl', '') if photos else ''
                            row = ['', name, price, size, gender, url, first_image_url]  # Blank column for listing date
                            ws.append(row)

            except Exception as ex:
                self.logger.error(f"Error in Mercari connections", ex)

        # Save the workbook to a file
        wb.save("outputmercari.xlsx")
        self.logger.info("Search results have been saved to outputmercari.xlsx.")

        return None
