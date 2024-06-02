import http.client
import json
from openpyxl import Workbook

# Establish a connection to the API
conn = http.client.HTTPSConnection("mercari.p.rapidapi.com")
headers = {
    'X-RapidAPI-Key': "e68937903dmsh53a9dc44eeefef1p1b6bedjsn8e1076d22514",
    'X-RapidAPI-Host': "mercari.p.rapidapi.com"
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
    conn.request("GET", f"/Mercari/Search?page=1&query={formatted_query}", headers=headers)
    res = conn.getresponse()
    data = res.read()

    # Decode the JSON response
    decoded_data = json.loads(data.decode("utf-8"))

    # Create a new sheet for each query
    ws = wb.create_sheet(title=query[:31])  # Excel sheet names are limited to 31 characters

    if isinstance(decoded_data, list) and decoded_data:
        response_headers = decoded_data[0].keys() if decoded_data else []
        ws.append(list(response_headers))
        for item in decoded_data:
            row = []
            for header in response_headers:
                cell_value = item.get(header, '')
                # Convert complex structures to strings
                if isinstance(cell_value, (list, dict)):
                    cell_value = json.dumps(cell_value)
                row.append(cell_value)
            ws.append(row)

# Save the workbook to a file
#wb.save("search_results.xlsx")
#print("Search results have been saved to search_results.xlsx.")







