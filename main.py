import requests
import html
from twilio.rest import Client
import os

STOCK_NAME = "IBM"
COMPANY_NAME = "Tesla Inc"

stock_api_key = "DO9KJIXT90DV0BM5"
news_api_key = "381baf346dcd4248a17cf83a1a713cbe"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

stock_parameters = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK_NAME,
    "apikey": stock_api_key
}

news_parameters = {
    "apikey": news_api_key,
    "q": "ibm",
    "pageSize": 3
}

stock = requests.get(url=STOCK_ENDPOINT, params=stock_parameters)
data_stock = stock.json()

print(data_stock)
yesterday_key = list(data_stock["Time Series (Daily)"].keys())[0]
the_day_before_yesterday_key = list(data_stock["Time Series (Daily)"].keys())[1]




Time_series = data_stock["Time Series (Daily)"]
    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

stock_prices = [(k, Time_series[k]) for k in Time_series]
# print(stock_prices[0])
yesterday_closing_price = float(Time_series[yesterday_key]["4. close"])

the_day_before_yesterday_closing_price = float(Time_series[the_day_before_yesterday_key]["4. close"])

difference = yesterday_closing_price - the_day_before_yesterday_closing_price
difference = abs(difference)


percentage = (yesterday_closing_price/the_day_before_yesterday_closing_price)*100 - 100
percentage = round(percentage, 2)
# print(percentage)



    ## STEP 2: https://newsapi.org/
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
if percentage > 5:
    print("Get News")


news = requests.get(url=NEWS_ENDPOINT, params=news_parameters)
news_stories = news.json()
# print(news_stories)
urls = []
for i in range(0, 3):
    first_url = news_stories["articles"][i]["url"]
    urls.append(first_url)

# print(urls)



    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number.

headlines = [news_stories["articles"][k]["title"] for k in range(0, 3)]
# print(headlines)
description = [html.escape(news_stories["articles"][k]["description"]) for k in range(0, 3)]
# print(description)



account_sid = os.environ.get('SID')
auth_token = os.environ.get('AUTH_TOKEN')

# 92989bf95cef8ff3a7facaf70581104a
client = Client(account_sid, auth_token)
print(auth_token)
for i in range(0, 3):
    message = client.messages.create(
      from_='+16813203129',
      body=f"IBM: 🔺 {percentage}%\nHeadline: {headlines[i]}\nBrief: {description[i]}\nURL: {urls[i]}",
      to=os.environ.get('NUMBER')
    )

# print(message.sid)

# Format the message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""


