import http.client
import json
from openpyxl import Workbook
from pandas import DataFrame


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
            with open("../config/keywords.json", "r") as file:
                kwjson = json.load(file)
            # Fetch keywords list
            keywords = kwjson["keywords"]
        except Exception as ex:
            self.logger.error("Failed to read keyword config", ex)

        wb = Workbook()
        wb.remove(wb.active)

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
                        response_headers = ['Name (listing title)', 'Price', 'Size', 'Gender', 'URL']
                        ws.append(response_headers)
                        for item in decoded_data:
                            name = item.get('name', '')
                            price = item.get('price', '')
                            size_dict = item.get('itemSize', {})
                            size = size_dict.get('name', '') if isinstance(size_dict, dict) else ''
                            size = (size.split(' ')[0]
                                    .replace(',', '')
                                    .replace('(', '')
                                    .replace(')', '')
                                    .replace(" ", '0')
                                    )
                            gender = item.get('categoryTitle', '')
                            url = item.get('url', '')
                            row = [name, price, size, gender, url]
                            ws.append(row)

            except Exception as ex:
                self.logger.error(f"Error in Mercari connections", ex)

        wb.save("../resources/outputmercari.xlsx")
        self.logger.info("Search results have been saved to ../resources/outputmercari.xlsx.")

        return None
