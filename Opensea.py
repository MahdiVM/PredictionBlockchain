import requests
import json

url = "https://api.opensea.io/api/v2/collections"

headers = {
    "accept": "application/json",
    "x-api-key": "db02fe579dff4febb0f41dbdac11c5f9"
}

response = requests.get(url, headers=headers)
data = json.loads(response.text)['collections']
new_data = []

for item in data:
    collection = item['collection']
    name = item['name']
    opensea_url = item['opensea_url']
    contracts = item['contracts']
    my_dict = dict(Collection=collection, Name=name, OpenSea_Url=opensea_url, Contracts=contracts)
    new_data.append(my_dict)

print(json.dumps(new_data))


url = "https://api.opensea.io/api/v2/collection/crypto-celebrity-4/nfts"

headers = {
    "accept": "application/json",
    "x-api-key": "db02fe579dff4febb0f41dbdac11c5f9"
}

response = requests.get(url, headers=headers)

print(response.text)