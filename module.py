import requests

url = "https://api.covid19api.com/"

load = {}
headers= {}

response = requests.request("GET", url, headers=headers, data = load)

print(response.text.encode('utf8'))
