import http.client
import json
import time
import pandas as pd
from openpyxl import Workbook
import re
import requests
from pandas import json_normalize
from urllib.parse import quote
import src.ebayconnection
import base64
import json
import logging
import requests
from datetime import datetime, timedelta
from pandas import json_normalize


queries = [
    "Nike Dunk MF DOOM",
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

# Verify that headers are correct (for debugging)
print("Headers type before request:", type(headers))



# Process each query
for query in queries:
    keywords = query.split(" ")
    keyword_query = create_keyword_query(keywords)
    print(f"Requesting data for query: {query}")  # Debugging statement

    # Make the GET request with the correct headers
    conn.request("GET", f"/getSearch?page=100&keyword={keyword_query}&countryCode=us&sortBy=newlyListed", headers=headers)
    res = conn.getresponse()
    data = res.read()

    # Decode the JSON response
    decoded_data = json.loads(data.decode("utf-8"))

    # Create a new sheet for each query
    ws = wb.create_sheet(title=query[:31])  # Excel sheet names are limited to 31 characters

    # Print the JSON response to understand its structure (for debugging)
    print(json.dumps(decoded_data, indent=4))

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
                cell_value = clean_cell_value(cell_value)
                row.append(cell_value)
            ws.append(row)
    else:
        print(f"No items found for query: {query}")
    time.sleep(1.0)


#EBAY

class oAuthToken:
    def __init__(self, error=None, access_token=None, refresh_token=None, refresh_token_expiry=None, token_expiry=None):
        """
        token_expiry: datetime in UTC
        refresh_token_expiry: datetime in UTC
        """
        self.access_token = access_token
        self.token_expiry = token_expiry
        self.refresh_token = refresh_token
        self.refresh_token_expiry = refresh_token_expiry
        self.error = error

class EnvType:
    def __init__(self, config_id, web_endpoint, api_endpoint):
        self.config_id = config_id
        self.web_endpoint = web_endpoint
        self.api_endpoint = api_endpoint

class Environment:
    PRODUCTION = EnvType("api.ebay.com", "https://auth.ebay.com/oauth2/authorize",
                          "https://api.ebay.com/identity/v1/oauth2/token")
    SANDBOX = EnvType("api.sandbox.ebay.com", "https://auth.sandbox.ebay.com/oauth2/authorize",
                       "https://api.sandbox.ebay.com/identity/v1/oauth2/token")

class Credentials:
    def __init__(self, client_id, client_secret, dev_id, ru_name):
        self.client_id = client_id
        self.dev_id = dev_id
        self.client_secret = client_secret
        self.ru_name = ru_name

def generate_request_headers(credential):
    cred = f"{credential.client_id}:{credential.client_secret}"
    b64_encoded_credential = base64.b64encode(cred.encode())
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic ' + b64_encoded_credential.decode()
    }
    return headers

def generate_application_request_body(scopes):
    body = {
        'grant_type': 'client_credentials',
        'scope': scopes
    }
    return body

class EbayConnection:
    def fetch_token(self, client_id, client_secret, dev_id, ru_name):
        credential = Credentials(client_id, client_secret, dev_id, ru_name)
        app_scopes = "https://api.ebay.com/oauth/api_scope"

        headers = generate_request_headers(credential)
        body = generate_application_request_body(app_scopes)

        resp = requests.post(Environment.PRODUCTION.api_endpoint, data=body, headers=headers)
        content = json.loads(resp.content)
        token = oAuthToken()

        if resp.status_code == requests.codes.ok:
            token.access_token = content['access_token']
            # set token expiration time 5 minutes before actual expire time
            token.token_expiry = datetime.utcnow() + timedelta(seconds=int(content['expires_in'])) - timedelta(minutes=5)
        else:
            token.error = f"{resp.status_code}: {content.get('error_description', 'No description')}"
            logging.error("Unable to retrieve token. Status code: %s - %s", resp.status_code,
                          requests.status_codes._codes[resp.status_code])
            logging.error("Error: %s - %s", content.get('error', 'No error'), content.get('error_description', 'No description'))

        return token

    def connect(self):
        url = "https://api.ebay.com/buy/browse/v1/item_summary/search?q=Nike%20SB%20MF%20DOOM&limit=10"

        # app_config_path = "../config/ebay-config-sample.json"
        # with open(app_config_path, 'r') as f:
        #     content = json.loads(f.read())
        #
        # client_id = content["api.ebay.com"]['appid']
        # dev_id = content["api.ebay.com"]['devid']
        # client_secret = content["api.ebay.com"]['certid']
        # ru_name = content["api.ebay.com"]['redirecturi']
        client_id = "SachinSu-OUTKITS-PRD-0ac054617-22f59fea"
        dev_id = "57622e67-4317-4256-83c9-9a59eb0e89f8"
        client_secret = "PRD-ac0546174f59-2748-445e-8d93-4598"
        ru_name = "fnsdfasdfs"

        token = self.fetch_token(client_id, client_secret, dev_id, ru_name)
        if token.access_token is None:
            logging.error("Failed to fetch access token")
            return

        bearer_token = "Bearer " + token.access_token
        headers = {
            'Authorization': bearer_token
        }

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            logging.error("API request failed with status code %s", response.status_code)
            return

        json_content = response.json()
        if 'itemSummaries' not in json_content:
            logging.error("Key 'itemSummaries' not found in the JSON data.")
            return

        item_summaries = json_content['itemSummaries']
        df = json_normalize(item_summaries)
        # df.to_csv('../resources/ebaydata.csv', index=False)
        return df
connection = EbayConnection()
ebay_data = connection.connect()