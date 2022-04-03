import requests

url = "https://api.upbit.com/v1/candles/minutes/1?market=KRW-BTC&count=1"

headers = {"Accept": "application/json"}

response = requests.request("GET", url, headers=headers)

# print(response.text)

bit_price = response.json()

print(bit_price[0])
print(bit_price[0]['market'])