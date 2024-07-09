#This code adds the first image url from additionalimages to the images column in xlsx. -RF 07/09/24

import base64
import json
import logging
import requests
from datetime import datetime, timedelta
from pandas import json_normalize
import pandas as pd

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
    def __init__(self, logger):
        self.logger = logger

    def fetch_token(self, client_id, client_secret, dev_id, ru_name):
        credential = Credentials(client_id, client_secret, dev_id, ru_name)
        app_scopes = "https://api.ebay.com/oauth/api_scope"

        headers = generate_request_headers(credential)
        body = generate_application_request_body(app_scopes)

        resp = requests.post(Environment.PRODUCTION.api_endpoint, data=body, headers=headers)
        content = json.loads(resp.content)
        token = oAuthToken()

        if resp.status_code == requests.codes.ok:
            self.logger.info("Ebay access token fetched.")
            token.access_token = content['access_token']
            # set token expiration time 5 minutes before actual expire time
            token.token_expiry = datetime.utcnow() + timedelta(seconds=int(content['expires_in'])) - timedelta(minutes=5)
        else:
            token.error = f"{resp.status_code}: {content.get('error_description', 'No description')}"
            self.logger.error("Unable to retrieve token. Status code: %s - %s", resp.status_code,
                          requests.status_codes._codes[resp.status_code])
            self.logger.error("Error: %s - %s", content.get('error', 'No error'), content.get('error_description', 'No description'))

        return token

    def connect(self):
        app_config_path = "../config/ebay-config-sample.json"
        keywords_path = "../config/keywords.json"

        with open(app_config_path, 'r') as f:
            ebay_config = json.loads(f.read())

        with open(keywords_path, 'r') as f:
            keywords_json = json.loads(f.read())

        keywords = keywords_json.get('keywords', [])
        if not keywords:
            self.logger.error("No keywords found in keywords.json")
            return

        combined_df = pd.DataFrame()  # Combined DataFrame for all keywords

        try:
            for keyword in keywords:
                url = f"https://api.ebay.com/buy/browse/v1/item_summary/search?q={keyword}&limit=10"

                client_id = ebay_config["api.ebay.com"]['appid']
                dev_id = ebay_config["api.ebay.com"]['devid']
                client_secret = ebay_config["api.ebay.com"]['certid']
                ru_name = ebay_config["api.ebay.com"]['redirecturi']

                token = self.fetch_token(client_id, client_secret, dev_id, ru_name)
                if token.access_token is None:
                    self.logger.error(f"Failed to fetch access token for keyword '{keyword}'")
                    continue

                bearer_token = "Bearer " + token.access_token
                headers = {
                    'Authorization': bearer_token
                }

                response = requests.get(url, headers=headers)
                if response.status_code != 200:
                    self.logger.error("API request failed with status code %s for keyword '%s'", response.status_code, keyword)
                    continue

                self.logger.info("API request successful with status code %s for keyword '%s'", response.status_code, keyword)
                json_content = response.json()
                if 'itemSummaries' not in json_content:
                    self.logger.error("Key 'itemSummaries' not found in the JSON data for keyword '%s'", keyword)
                    continue

                item_summaries = json_content['itemSummaries']
                df = json_normalize(item_summaries)

                # Rename columns and add blank columns
                df.rename(columns={'title': 'Name', 'price.value': 'Price', 'itemWebUrl': 'URL'}, inplace=True)
                df['Size'] = ''
                df['Gender'] = ''

                # Extract the first image URL from additionalImages if available
                def extract_first_image_url(images):
                    if isinstance(images, list) and images:
                        first_image = images[0].get('imageUrl', '')
                        return first_image
                    return ''

                df['Image'] = df['additionalImages'].apply(extract_first_image_url)

                # Append to combined DataFrame
                combined_df = pd.concat([combined_df, df], ignore_index=True)

                self.logger.info(f"eBay data for keyword '{keyword}' added to combined DataFrame")

            # Select only the required columns
            combined_df = combined_df[['Name', 'Price', 'Size', 'Gender', 'URL', 'Image']]

            # Write to Excel file
            with pd.ExcelWriter('../resources/outputebay.xlsx', engine='xlsxwriter') as writer:
                combined_df.to_excel(writer, index=False, sheet_name='CombinedData')

            self.logger.info("Combined eBay data written to ../resources/outputebay.xlsx")

        except Exception as ex:
            self.logger.error("Failed writing eBay data to file", exc_info=True)

if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()

    connection = EbayConnection(logger)
    connection.connect()
