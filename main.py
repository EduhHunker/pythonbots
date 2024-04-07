import requests
from twilio.jwt import client
from twilio.rest import Client
Stock_Name = "BTC"
COMPANY_NAME = "BITCOIN"
stock_Endpoint = "https://www.alphavantage.co/query"
News_Endpoint = "https://newsapi.org/v2/everything"
News_Api = "a8a17030d6294bc3a562ff84058c305b"
Stock_Api_Key = "P0KGMT71LVDCK26T"
account_sid="AC459bede9198a2dd052b6d596e8f185ca"
auth_token="72dae87ae63ce43b63a28b149df69ef6"

Stock_params = {
    "function": "DIGITAL_CURRENCY_DAILY",
    "symbol": Stock_Name,
    "market": "USD",
    "Exchange":"Binance",
    "apikey": Stock_Api_Key,
    "interval": "1d",
}
response = requests.get(stock_Endpoint, params=Stock_params)
print(response)
data = response.json()['Time Series (Digital Currency Daily)']
print(data)
data_list = [Value for (key, Value) in data.items()]
yesterday_data = data_list[0]
yesterday_crosing_price = yesterday_data['4a. close (USD)']
print("Keys in yesterday_data:", yesterday_data.keys())
print(yesterday_crosing_price)

day_before_yesterday = data_list[1]
day_before_yesterday_crosing_price = day_before_yesterday['4a. close (USD)']
print(day_before_yesterday)

difference = float(yesterday_crosing_price) - float(day_before_yesterday_crosing_price)
up_down = "😂😂😂😂😂😂😂" \
    if difference > 0 \
    else "😢😢😢😢😢😢😢"

diff_percent = round((difference / float(yesterday_crosing_price)) * 100, 2)
print(diff_percent)

if abs(diff_percent) > 0.01:
    News_params = {
        "apiKey": News_Api,
        "qInTitle": Stock_Name,
    }
    news_response = requests.get(News_Endpoint, params=News_params)

    if news_response.status_code == 200:
        articles = news_response.json().get('articles')
        if articles:
            three_articles = articles[:3]
            formatted_articles = [
                f"{Stock_Name}:{up_down}{diff_percent}%\nHeadline: {article['title']}\nBrief: {article['description']}"
                for article in three_articles]
        else:
            print("No articles found.")
    else:
        print("Failed to fetch news:", news_response.status_code)
else:
    print("Price change is not significant.")


if formatted_articles:
    client = Client(account_sid, auth_token)
    for article in formatted_articles:
        message = client.messages.create(
            from_='+12405475713',
            to='+254719854780',
            body=article
        )
        print(message)

    for article in formatted_articles:
        message=client.messages.create(
            from_='whatsapp:+14155238886',
            to='whatsapp:+254719854780',
            body=article
        )




