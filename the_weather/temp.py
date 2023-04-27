import requests

url = 'http://api.weatherapi.com/v1/current.json?key=4a94268a79094898b56140331233103&q=Mumbai&aqi=no'

data = requests.get(url)
data = data.json()
print(data)