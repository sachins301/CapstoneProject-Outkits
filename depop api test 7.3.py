import http.client
import json
import pandas as pd

# Set up connection to Depop API
conn = http.client.HTTPSConnection("depop-thrift.p.rapidapi.com")

# Set up headers
headers = {
    'x-rapidapi-key': "e68937903dmsh53a9dc44eeefef1p1b6bedjsn8e1076d22514",
    'x-rapidapi-host': "depop-thrift.p.rapidapi.com"
}

# Make the request to Depop API
conn.request("GET", "/getSearch?page=100&keyword=nike%20mf%20doom&countryCode=us&sortBy=newlyListed", headers=headers)

# Get the response
res = conn.getresponse()
data = res.read()

#print(data.decode("utf-8"))

# Decode response data
response_str = data.decode("utf-8")

# Parse JSON response
response_json = json.loads(response_str)

# Print the JSON response to understand its structure
print(json.dumps(response_json, indent=4))

# Since the response is a list, use it directly
if isinstance(response_json, list):
    items = response_json
else:
    print("Unexpected JSON structure:", type(response_json))
    items = []
# Assuming the JSON response is a dictionary with a key 'results' containing a list of products
# Adjust the key according to the actual structure of the response
#items = response_json.get('results', [])

if not items:
    print("No items found in the JSON response.")

# Normalize JSON data to flat table
df = pd.json_normalize(items)

# Write DataFrame to CSV
df.to_csv('output.csv', index=False)

print("CSV file created successfully!")
