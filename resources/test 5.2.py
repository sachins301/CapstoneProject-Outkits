import http.client
import json
import pandas as pd

# Establish HTTPS connection
conn = http.client.HTTPSConnection("depop-thrift.p.rapidapi.com")

# Define request headers
headers = {
    'X-RapidAPI-Key': "e68937903dmsh53a9dc44eeefef1p1b6bedjsn8e1076d22514",
    'X-RapidAPI-Host': "depop-thrift.p.rapidapi.com"
}

# Send GET request
conn.request("GET", "/getSearch?page=100&countryCode=us&sortBy=newlyListed&keyword=Nike%20Dunk%20SB", headers=headers)

# Get response
res = conn.getresponse()
data = res.read()

# Decode response data
response_str = data.decode("utf-8")

# Parse JSON response
response_json = json.loads(response_str)

# Print the JSON response to understand its structure
print(json.dumps(response_json, indent=4))

# Assuming the JSON response is a dictionary with a key 'results' containing a list of products
# Adjust the key according to the actual structure of the response
items = response_json.get('results', [])

if not items:
    print("No items found in the JSON response.")

# Normalize JSON data to flat table
df = pd.json_normalize(items)

# Write DataFrame to CSV
df.to_csv('output.csv', index=False)

print("CSV file created successfully!")
