import time

import requests
import json

url = "https://api.opensea.io/api/v2/collections"
token = "db02fe579dff4febb0f41dbdac11c5f9"

headers = {
    "accept": "application/json",
    "x-api-key": token
}

response = requests.get(url, headers=headers)
data = json.loads(response.text)['collections']
new_data = []

for item in data:
    collection = item['collection']
    name = item['name']
    opensea_url = item['opensea_url']
    contracts = item['contracts']

    time.sleep(5)
    url = f"https://api.opensea.io/api/v2/collection/{collection}/nfts"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print(collection)
        list_nfts = json.loads(response.text)['nfts']
        nfts = []
        for nft in list_nfts:
            nfts.append(nft['identifier'])

        my_dict = dict(Collection=collection, Name=name, OpenSea_Url=opensea_url, Contracts=contracts,
                       NTFs=nfts)

        new_data.append(my_dict)

print(json.dumps(new_data))