import requests

url = "https://api.upbit.com/v1/candles/minutes/1?market=KRW-BTC&count=1"

headers = {"Accept": "application/json"}

response = requests.request("GET", url, headers=headers)

# print(response.text)

bit_price = response.json()

print(bit_price[0])
print('market',bit_price[0]['market'])
print('candle_date_time_kst',bit_price[0]['candle_date_time_kst'])
print('opening_price',bit_price[0]['opening_price'])
print('high_price',bit_price[0]['high_price'])
print('low_price',bit_price[0]['low_price'])
print('trade_price',bit_price[0]['trade_price'])
print('candle_acc_trade_price',bit_price[0]['candle_acc_trade_price'])
print('candle_acc_trade_volume',bit_price[0]['candle_acc_trade_volume'])