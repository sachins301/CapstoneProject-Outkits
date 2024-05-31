import http.client
import json
import pandas as pd

# Establish connection
conn = http.client.HTTPSConnection("poshmark.p.rapidapi.com")

# Headers required for the API request
headers = {
    'Accept-Encoding': "gzip, deflate",
    'X-RapidAPI-Key': "e68937903dmsh53a9dc44eeefef1p1b6bedjsn8e1076d22514",
    'X-RapidAPI-Host': "poshmark.p.rapidapi.com"
}

# Send GET request
conn.request("GET", "/search?query=Nike%20SB%20MF%20DOOM%20&domain=com", headers=headers)

# Get the response
res = conn.getresponse()
data = res.read()
# print(res.read())

# Decode response data
response_str = data.decode("utf-8")

# Parse JSON response
response_json = json.loads(response_str)

# Print the JSON response to understand its structure
print(json.dumps(response_json, indent=4))

# Assuming the JSON response is a dictionary with a key 'results' containing a list of products
# Adjust the key according to the actual structure of the response
items = response_json.get('data', [])

if not items:
    print("No items found in the JSON response.")
else:
    # Normalize JSON data to flat table
    df = pd.json_normalize(items)

    # Write DataFrame to CSV
    df.to_csv('output.csv', index=False)

    print("CSV file created successfully!")
