import base64
from datetime import datetime, timedelta
import json
import requests
import logging


class oAuth_token(object):

    def __init__(self, error=None, access_token=None, refresh_token=None, refresh_token_expiry=None, token_expiry=None):
        '''
            token_expiry: datetime in UTC
            refresh_token_expiry: datetime in UTC
        '''
        self.access_token = access_token
        self.token_expiry = token_expiry
        self.refresh_token = refresh_token
        self.refresh_token_expiry = refresh_token_expiry
        self.error = error


class env_type(object):
    def __init__(self, config_id, web_endpoint, api_endpoint):
        self.config_id = config_id
        self.web_endpoint = web_endpoint
        self.api_endpoint = api_endpoint


class environment(object):
    PRODUCTION = env_type("api.ebay.com", "https://auth.ebay.com/oauth2/authorize",
                          "https://api.ebay.com/identity/v1/oauth2/token")
    SANDBOX = env_type("api.sandbox.ebay.com", "https://auth.sandbox.ebay.com/oauth2/authorize",
                       "https://api.sandbox.ebay.com/identity/v1/oauth2/token")


def _generate_request_headers(credential):
    cred = credential.client_id + ':' + credential.client_secret
    b64_encoded_credential = base64.b64encode(str.encode(cred))
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic ' + b64_encoded_credential.decode()
    }

    return headers


def _generate_application_request_body(scopes):
    body = {
        'grant_type': 'client_credentials',
        'scope': scopes
    }

    return body


app_config_path = "../config/ebay-config-sample.json"
with open(app_config_path, 'r') as f:
    content = json.loads(f.read())

client_id = content["api.ebay.com"]['appid']
dev_id = content["api.ebay.com"]['devid']
client_secret = content["api.ebay.com"]['certid']
ru_name = content["api.ebay.com"]['redirecturi']


class Credentials(object):
    def __init__(self, client_id, client_secret, dev_id, ru_name):
        self.client_id = client_id
        self.dev_id = dev_id
        self.client_secret = client_secret
        self.ru_name = ru_name


credential = Credentials(client_id, client_secret, dev_id, ru_name)

app_scopes = "https://api.ebay.com/oauth/api_scope"


headers = _generate_request_headers(credential)
body = _generate_application_request_body(app_scopes)

resp = requests.post(environment.PRODUCTION.api_endpoint, data=body, headers=headers)
content = json.loads(resp.content)
token = oAuth_token()

if resp.status_code == requests.codes.ok:
    token.access_token = content['access_token']
    # set token expiration time 5 minutes before actual expire time
    token.token_expiry = datetime.utcnow() + timedelta(seconds=int(content['expires_in'])) - timedelta(minutes=5)

else:
    token.error = str(resp.status_code) + ': ' + content['error_description']
    logging.error("Unable to retrieve token.  Status code: %s - %s", resp.status_code,
                  requests.status_codes._codes[resp.status_code])
    logging.error("Error: %s - %s", content['error'], content['error_description'])

url = "https://api.ebay.com/buy/browse/v1/item_summary/search?q=Nike%20SB%20MF%20DOOM&limit=10"

bearer_token = "Bearer "+token.access_token
payload = {}
headers = {
    'Authorization': bearer_token
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.json())

if response.status_code == 200:
    # Extract JSON content from the response
    json_content = response.json()

#     # Save the JSON content to a file
#     with open('../resources/ebaydata.json', 'w') as f:
#         json.dump(json_content, f)
#
#     print("JSON file saved successfully.")
# else:
#     print("Error:", response.status_code)
#
import pandas as pd
from pandas import json_normalize
import json
#
# json_path = "../resources/ebaydata.json"
#
# with open(json_path, "r") as file:
#     json_data = json.load(file)

if 'itemSummaries' in json_content:
    item_summaries = json_content['itemSummaries']
    print(item_summaries)
else:
    print("Key 'itemSummaries' not found in the JSON data.")

df = json_normalize(item_summaries)

df.to_csv('../resources/ebaydata.csv', index=False)
