import pandas as pd
from pandas import json_normalize
import json

json_path = "../resources/ebaydata.json"

with open(json_path, "r") as file:
    json_data = json.load(file)

if 'itemSummaries' in json_data:
    item_summaries = json_data['itemSummaries']
    print(item_summaries)
else:
    print("Key 'itemSummaries' not found in the JSON data.")

df = json_normalize(item_summaries)

df.to_csv('../resources/ebaydata.csv', index=False)