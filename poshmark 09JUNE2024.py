import http.client
import json
from openpyxl import Workbook
import re

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

# Verify that headers are correct (for debugging)
print("Headers type before request:", type(headers))

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

# Create a new Excel workbook
wb = Workbook()
wb.remove(wb.active)  # Remove the default sheet

# Process each query
for query in queries:
    formatted_query = query.replace(" ", "%20")
    print(f"Requesting data for query: {query}")  # Debugging statement

    # Make the GET request with the correct headers
    conn.request("GET", f"/search?query={formatted_query}&domain=com", headers=headers)
    res = conn.getresponse()
    data = res.read()

    # Decode the JSON response
    decoded_data = json.loads(data.decode("utf-8"))

    # Create a new sheet for each query
    ws = wb.create_sheet(title=query[:31])  # Excel sheet names are limited to 31 characters

    # Print the JSON response to understand its structure (for debugging)
    print(json.dumps(decoded_data, indent=4))

    # Adjust the following key to match the actual structure of the response
    items = decoded_data.get('data', [])

    if items:
        # Assuming each item in 'data' is a dictionary
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
                cell_value = clean_cell_value(cell_value)
                row.append(cell_value)
            ws.append(row)
    else:
        print(f"No items found for query: {query}")

# Save the workbook to a file
wb.save("poshmark_search_results.xlsx")
print("Search results have been saved to poshmark_search_results.xlsx.")
