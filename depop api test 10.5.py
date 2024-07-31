# This code works for depop to function on it's own and has changes made to the search function and excel population - RF 07.31.24

import http.client
import json
import time
from datetime import datetime
import re
from openpyxl import Workbook
from urllib.parse import quote
from dateutil.parser import parse

# Function to clean the cell value
def clean_cell_value(value):
    if isinstance(value, str):
        # Remove non-printable characters
        value = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', value)
    return value

# Function to create a keyword query for multiple search terms
def create_keyword_query(keywords):
    return quote(" ".join(keywords))

# Establish a connection to the Depop API
conn = http.client.HTTPSConnection("depop-thrift.p.rapidapi.com")

# Set up headers
headers = {
    'x-rapidapi-key': "e68937903dmsh53a9dc44eeefef1p1b6bedjsn8e1076d22514",
    'x-rapidapi-host': "depop-thrift.p.rapidapi.com"
}

queries = [
    "Nike Dunk MF DOOM",
    "Nike SB MF DOOM",
    "Nike Dunk Low 6.0",
    "Nike SB Dunk Low Bigfoot",
    "Carhartt Hooded Jacket Red",
    "Carhartt Hooded Jacket Orange",
    "Carhartt Hooded Jacket Teal",
    "Carhartt Hooded Jacket Purple",
    "Nike SB Dunk Size 12",
    "Nike Dunk Cinder Brown",
    "Nike Dunk Light Stone Bone",
    "Nike Dunk SB Stussy",
    "Nike Dunk Pushead",
    "Nike Dunk High SB Khaki Creed",
    "Nike Dunk 6.0 Hemp",
    "Nike Dunk SB Mocha",
    "Nike Dunk SB Bison",
    "Nike Dunk SB Mocha Choc",
    "Nike Dunk SB Medusa",
    "Nike Dunk SB Oompa Loompa",
    "Nike 6.0 NKE Quasar Purple",
    "Nike Dunk SB Crown Royal",
    "Nike Dunk Palm Green",
    "Nike Dunk Low Cargo Khaki",
    "Nike Dunk CL demim",
    "Nike Dunk Low Pro Mushroom",
    "Nike Dunk Low SB Tweed",
    "Nike Dunk Low ACG",
    "Dunk Low Pro Obsidian",
    "Dunk Low Pro Midnight Navy",
    "Nike Dunk Low Pro Mesa",
    "Dunk Low Pro B Olive",
    "Nike SB Dunk Trail End",
    "Nike SB Dunk Dusty Cactus",
    "Pro B Oxide"
  ]

print("Headers type before request:", type(headers))

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
    keyword_query = create_keyword_query(keywords)
    print(f"Requesting data for query: {query}")  # Debugging statement

    # Initialize variable to track if items were found and retry count
    items_found = False
    retries = 0
    max_retries = 3

    # Retry until items are found or max retries reached
    while not items_found and retries < max_retries:
        # Make the GET request with the correct headers
        search_url = f"https://www.depop.com/search/?q={keyword_query}&scrollYOffset="
        conn.request("GET", f"/searchByURL?url={quote(search_url)}&country=us", headers=headers)
        res = conn.getresponse()
        data = res.read()

        time.sleep(2.0)

        # Decode the JSON response
        decoded_data = json.loads(data.decode("utf-8"))

        # Print the JSON response to understand its structure (for debugging)
        print(json.dumps(decoded_data, indent=4))

        # Check if decoded_data is a list
        if isinstance(decoded_data, list):
            items = decoded_data
        else:
            # Adjust the following key to match the actual structure of the response
            items = decoded_data.get('products', [])

        # Filter items to include only those with the brand 'Nike' or 'Carhartt'
        selected_items = [item for item in items if item.get('brandName') and item.get('brandName').lower() in ['nike', 'carhartt']]

        if selected_items:
            items_found = True
            print(f"Items have been found for query: {query}")
            for item in selected_items:
                row = []
                for header in header_order:
                    if header == 'Gender':
                        cell_value = ''  # Blank column for Gender
                    elif header == 'Image':
                        pictures = item.get('pictures', [])
                        cell_value = pictures[0].get('150') if pictures else ''  # Get the first picture URL or empty string if no pictures
                    elif header == 'URL':
                        slug = item.get('slug', '')
                        cell_value = f"https://www.depop.com/products/{slug}/" if slug else ''
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
                            amount = float(price_info.get('priceAmount', 0))
                            national_shipping = float(price_info.get('nationalShippingCost', 0))
                            cell_value = amount + national_shipping
                        else:
                            cell_value = item.get(cell_key, '')
                        if isinstance(cell_value, (list, dict)):
                            cell_value = json.dumps(cell_value)
                        cell_value = clean_cell_value(cell_value)
                    row.append(cell_value)
                ws.append(row)
        else:
            retries += 1
            print(f"No items found for query: {query}, retrying... (Attempt {retries}/{max_retries})")

    if not items_found:
        print(f"Max retries reached for query: {query}. Moving on to the next keyword.")
 #except Exception as ex:
 #print(f"Error in Depop connections", ex)
# Save the workbook to a file named 'outputdepop.xlsx'
filename = "outputdepop.xlsx"
wb.save(filename)
print(f"Search results have been saved to {filename}.")

