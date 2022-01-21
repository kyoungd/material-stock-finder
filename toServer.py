import requests
from study.favorites import JsonFavorite
import os
import time

print('start push.')
url = os.environ.get(
    'PUSH_URL', 'https://simp-admin.herokuapp.com/api/symbols/1')
content = JsonFavorite(filename='symbols.json')
data = content.GetJson
r = requests.put(url, json=data)

# print(f"Status Code: {r.status_code}, Response: {r.json()}")
print(f"Status Code: {r.status_code}")
print('complete.  exiting.')
