import requests

url = "https://api.upbit.com/v1/candles/minutes/1?market=KRW-BTC&count=1"

headers = {"Accept": "application/json"}

response = requests.request("GET", url, headers=headers)

# print(response.text)

bit_price = response.json()

print(bit_price[0])
print(bit_price[0]['market'])
print(bit_price[0]['candle_date_time_kst'])
print(bit_price[0]['opening_price'])
print(bit_price[0]['high_price'])
print(bit_price[0]['low_price'])
print(bit_price[0]['trade_price'])
print(bit_price[0]['candle_acc_trade_price'])
print(bit_price[0]['candle_acc_trade_volume'])