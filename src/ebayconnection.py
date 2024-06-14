import http.client
import json
import requests

url = "https://api.ebay.com/buy/browse/v1/item_summary/search?q=Nike%20SB%20MF%20DOOM&limit=10"

payload = {}
headers = {
  'Authorization': 'Bearer v^1.1#i^1#r^0#p^1#I^3#f^0#t^H4sIAAAAAAAAAOVYbWwURRju9VqwoUgERUWIxyLEtNze7O59bnqXHNcCd5Re4a4EKljndue4be92193Ztkf5calY4g+hxi8ImjR8+YFoosaUiCAmBMGECCYGIx/BHwQCihoSQcW4uz3KtRJAeomXeH8u88477zzPM+87MzsgN66qpm9h328TLePLB3IgV26xUBNA1bjK2vut5dMqy0CBg2Ug90Suotd6vk6FmbTMLkWqLIkqsnVn0qLKmkY/oSkiK0FVUFkRZpDKYo6NBRc3sjQJWFmRsMRJacIWrvcTrqTX66YBBRnO6fMxtG4Vb8SMS36C5z0cwyR56PMwlJvh9H5V1VBYVDEUsZ+gAe20A7edcsYBYGnAMjRJA18rYVuGFFWQRN2FBETAhMuaY5UCrLeHClUVKVgPQgTCwfmxaDBc39AUr3MUxArkdYhhiDV1ZCsk8ci2DKY1dPtpVNObjWkch1SVcASGZhgZlA3eAHMP8E2pfdCTcDm90OvjKbePBkWRcr6kZCC+PQ7DIvD2pOnKIhELOHsnRXU1Eu2Iw/lWkx4iXG8z/pZoMC0kBaT4iYZ5wRXB5mYiEINcShBjmj3aEl8UjsfszUvr7QBywOV0Ux47TSddviSC+XmGguVVHjVRSBJ5wdBMtTVJeB7SQaPR0lAF0uhOUTGqBJPYAFToRw9L6Gw11nRoETWcEo1lRRldB5vZvPMCDI/GWBESGkbDEUZ3mAr5CSjLAk+M7jRTMZ893aqfSGEssw5HV1cX2cWQkrLaQQNAOZYvboxxKZSBhOFr1LrpL9x5gF0wqXBIH6kKLM7KOpZuPVV1AOJqIuD0MU4fldd9JKzAaOs/DAWcHSMLolgFAmkvn3DybpcXIg9FwWIUSCCfow4DB0rArD0DlQ6E5TTkkJ3T80zLIEXgWcaVpBlvEtl5ty9pd/qSSXvCxeuTJRECCCUSnM/7P6qTu830GOIUhIuT6sVK8/i8bi8d7gTakqZQNFSbXsp46K4Wuj6zgIo11IZr5cZFQtTRHkXzV/jvthhuST6UFnRl4vr8pVfrCyUVI35M9GKcJKNmKS1w2dJaYEbhm6GCszGUTuuGMZEMynK4SFt1sej9u13i3mgX8YT6b06nW7JSjYwtLVbGeFUPAGWBNM4fkpMyDglqRq3jlGFuM1GPibegX1tLirVOcoitwA/dN0mdMk6RaidHKkiVNEW/apNR4/4VlzqQqB9nWJHSaaQsG1sGGOWcyWgYJtKo1Oq6CAkuwBI7aykP5WVop5Ohx8SLM0/StlLbkoq0E1eE7uFO7Rj5gR8oM39Ur+UL0GvZV26xgDowm5oFZo6ztlRYq6epAkakAJOkKqwW9e9WBZEdKCtDQSmfUvbr1lcXhqY1RF+r6Ylnv95yqKy64H1hYBV4ZPiFocpKTSh4bgDTb/ZUUpMenkg7gZtyAkADhm4Fs272VlBTKx6MrN3jTUWmrqx8qnV9/8bHP4gfG3wITBx2slgqyyp6LWU9G9/7ZfHKvraPBvfu/OSxQc/PV862x+esGdz5feNK+77MAfr1DyedeP/i1U1q7ulL2a7PLnZ0Np3Z/E11b2ww4jr97Yw3T8JPP66JgA0r3p57WJ5ycPlfz7+1/vKV2X8cuUYeO31tA3nctvNcS2rquvvmVAUiEyafPSB1Hgju2nv6VHf72oETfM/0PrLHuqDmx+fevXLp2bp9jjPeZ17ZX908fdv+ydVey1Y5d906s/38o1vO1e5/48KuJwnpcvCrzjXrasen+t/ZfGR76uiaroYX3Z+fjDywyfL7rquVneDl73Yfqlr10gs/7Ll+eFu8/7gw66eDf+44E9l+SlxywfPljLlH58zd0baFWr6bPXJoaC3/BrkB8Hj5EQAA'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.json())

#
# conn = http.client.HTTPSConnection("api.ebay.com")
#
# headers = {
#     'Authorization': 'Bearer v^1.1#i^1#p^1#r^0#I^3#f^0#t^H4sIAAAAAAAAAOVYe2wURRi/64tAKVXwUashxxYkcNm72b2913p3yfUBPfu4wl1BiEj2MdsuvdtddmZpLxI5S0SDwYiGEoINSARCNAbU+CKa2GBIJEH5A4iaaIgoSogkGoMYEXe3pVwrAaSX2MT75zLffPPN7/eb75uZHZCvmLpwU/OmS1XOKSW78yBf4nRSlWBqRbl7RmlJbbkDFDg4d+fn5sv6S3+MIC6b0dilEGmqgqCrL5tREGsbo4ShK6zKIRmxCpeFiMUCm4q3tbK0B7CarmJVUDOEK9EYJcQQxcMgJ0g+fyAI+aBpVa7FTKtRgg/xDEMBIPKSJArhkNmPkAETCsKcgqMEDWiGBH6SYtIAsD4fywQ8IR+1knAtgzqSVcV08QAiZsNl7bF6AdabQ+UQgjo2gxCxRHxRKhlPNDa1pyPeglixER1SmMMGGttqUEXoWsZlDHjzaZDtzaYMQYAIEd7Y8Axjg7Lxa2DuAL4tdRjAoJ/iKT4AeTokgKJIuUjVsxy+OQ7LIoukZLuyUMEyzt1KUVMNfg0U8Eir3QyRaHRZf0sMLiNLMtSjRFN9fEW8o4OIpTihW1ZSBpnsTLck0imyY2kjCTgB+JkAFSRpWvKHJciNzDMcbETlcRM1qIooW5ohV7uK66EJGo6Xhi6QxnRKKkk9LmELUKEffU1COrjSWtPhRTRwt2ItK8yaOrjs5q0XYHQ0xrrMGxiORhjfYSsUJThNk0VifKediiPZ04eiRDfGGuv19vb2enp9HlXv8tIAUN7H2lpTQjfMcoTla9W67S/fegAp21QEaI5EMotzmomlz0xVE4DSRcSYsI8JUyO6j4UVG2/9h6GAs3dsQRSrQPggHWZCYVFkOBD2cVIxCiQ2kqNeCwfkuRyZ5fQeiLUMJ0BSMPPMyEJdFlmfX6J9IQmSYiAskUxYkkjeLwZISoIQQMjz5ub3P6qT2830FBR0iIuT6sVK83R9X4hOrAPGkvaGZIM7s9QXpHs76cbsYirV5E64tdYWOeldk4SLVkRvtxhuSL4hI5vKpM35J1+tN6sIQ3FC9FKCqsEONSMLucm1wD5d7OB0nEvBTMY0TIhkXNMSRdqqi0Xv3+0Sd0a7iCfUf3M63ZAVsjJ2crGyxiMzAKfJHuv88Qhq1qtyhlXruNsyr7ZRT4i3bF5bJxVrk+QwW1kcvm96TMq424PWCR4dItXQzau2J2ndv9JqD1TM4wzraiYD9WUTywCrnLNZA3N8Bk62ui5CgsvcJDtrqSDlDzCBEB2YEC/BPklXT7YtqUg7cVnDHdypvWM/8GMO+0f1O4dAv/PjEqcTRMA8qg7MqSjtLCudXotkDD0yJ3mQ3KWY36069PTAnMbJesksxy97tjU31DYlBxY+mc59sfOoY3rB+8LuVaBm9IVhailVWfDcAB663lNOVd9fRTPATzEA+HxMYCWou95bRt1Xds+BvWy120sdrnk71/fOsZqfHY70EKgadXI6yx1l/U5HpLNq3Zw9S57eVtd18tQ0bduOh4fIjZfP7/0r8e3JQxsSy33rj5e/eejsa7MHT/yW2vk85V770ov7B77evuXVeCQ545lpiYvVX66vWrvjaPypWPCBC1sXv/XNqg/PL+g69P7MrUZL+N4z4iOb8/UDwgcLd7wS8b+g7K/E80vOX/xkzq/bNx+csjPfeeHTwbl3z74yvwdVxdoi7VWX93m/Wv7dTHnrrBMnHnTMOxaoOdv2Obdv3uHT6y+fO8cMvOz+vWnGu6f2/dmyR/ro0TObYq18qOPK1Z+OVG85+/2xXbUbn43Pr7v6xHs/sH907bp0oHn16+7+iv2BIwePv7G2fXDDc6fdlbHawbtmD4XQgsc/G15Kx9+6FGG7+REAAA=='
# }
#
# conn.request("GET", "/buy/browse/v1/item_summary/search?q=nike&limit=10", headers=headers)
#
# res = conn.getresponse()
# data = res.read()
#
# # Decode the bytes data to a string
# data_str = data.decode("utf-8")
# print(data_str)

if response.status_code == 200:
    # Extract JSON content from the response
    json_content = response.json()

    # Save the JSON content to a file
    with open('../resources/ebaydata.json', 'w') as f:
        json.dump(json_content, f)

    print("JSON file saved successfully.")
else:
    print("Error:", response.status_code)

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
