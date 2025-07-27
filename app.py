import requests
import os

api_key = os.getenv("API_KEY")
url = f"https://data.fixer.io/api/latest?access_key={api_key}"

querystring = {"base":"USD"}


response = requests.get(url, params=querystring)

print(response.json())