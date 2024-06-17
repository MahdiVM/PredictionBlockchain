import csv
import datetime
import time

import requests
import json


url = "https://api.reservoir.tools/collections/v7"
token = "eadfb758-7639-51a3-8c9e-58a3af40cfbe"
collection_specification = []
daily_collection_volume = []

headers = {
    "accept": "*/*",
    "x-api-key": token
}

response = requests.get(url, headers=headers)
print(response.text)
result = json.loads(response.text)['collections']


for item in result:
    record = dict(
        ChainID=item['chainId'],
        ID=item['id'],
        Name=item['name'],
        Symbol=item['symbol'],
        TokenCount=item['tokenCount']
    )
    collection_specification.append(record)

for item in collection_specification:
    url = f"https://api.reservoir.tools/collections/daily-volumes/v1?id={item['ID']}&limit=1000"

    headers = {
        "accept": "*/*",
        "x-api-key": token
    }

    response = requests.get(url, headers=headers)
    result = json.loads(response.text)['collections']
    name = item['Name']
    with open(f'{name}.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        field = ["Date", "Price", "Volume"]
        writer.writerow(field)

        for volume in result:
            struct_time = time.localtime(int(volume['timestamp']))
            date = time.strftime("%Y-%m-%d %H:%M:%S", struct_time)
            writer.writerow([date, volume['floor_sell_value'], volume['volume']])

# record = dict(
#     DateTime=date,
#     Volume=volume['volume'],
#     FloorSellValue=volume['floor_sell_value'],
#     SalesCount=volume['sales_count']
# )
# daily_collection_volume.append(record)





# url = "https://api.reservoir.tools/collections/daily-volumes/v1?id=0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d&limit=1000"
#
# headers = {
#     "accept": "*/*",
#     "x-api-key": "eadfb758-7639-51a3-8c9e-58a3af40cfbe"
# }
#
# response = requests.get(url, headers=headers)
#
# print(response.text)