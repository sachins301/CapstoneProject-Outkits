import pandas as pd
from pandas import json_normalize
import json

json_path = "../resources/data.json"

with open(json_path, "r") as file:
    json_data = json.load(file)

print(json_data)

df = json_normalize(json_data)

print(df)