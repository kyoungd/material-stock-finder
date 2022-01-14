import requests
from study.favorites import JsonFavorite
import os

url = os.environ.get('PUSH_URL', 'https://simp-serve.herokuapp.com/symbols')
content = JsonFavorite(filename='symbols.json')
data = content.GetJson
r = requests.post(url, json=data)
print(f"Status Code: {r.status_code}, Response: {r.json()}")
