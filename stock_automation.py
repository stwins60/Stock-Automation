import smtplib
import ssl

import requests
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

import auth
import json
import random
import time


def robinhood():
    while True:

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls(context=ssl.create_default_context())

        with open('tickers.txt') as f:
            tickers = f.read().splitlines()

        ticker_data = random.choice(tickers)

        url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/v2/get-quotes"

        querystring = {"region": "US", "symbols": ticker_data}

        headers = {
            'x-rapidapi-key': auth.API_KEY,
            'x-rapidapi-host': auth.API_HOST
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        data = str(response.text)
        stock_data = json.loads(data)

        for i in stock_data:
            stock = stock_data[i]['result'][0]
            # print(stock)

        symbol = str(stock['symbol'])
        bid_price = float(stock['bid'])
        bid_size = str(stock['bidSize'])
        ask_price = str(stock['ask'])
        ask_size = str(stock['askSize'])
        shortName = str(stock['shortName'])
        regularMarketPrice = str(stock['regularMarketPrice'])
        regularMarketDayHigh = str(stock['regularMarketDayHigh'])
        regularMarketDayLow = str(stock['regularMarketDayLow'])
        quoteType = str(stock['quoteType'])
        regularMarketOpen = str(stock['regularMarketOpen'])
        exchangeTimezoneName = str(stock['exchangeTimezoneName'])

        print(bid_price, symbol)
        if bid_price <= 100.00 and bid_price is not 0:
            print(symbol + " Bid: " + str(bid_price))
            time.sleep(5)

            message = Mail(
                from_email=auth.USER_NAME,
                to_emails=auth.USER_NAME,
                subject="Automated Stock Alerts",
                html_content='<strong>The Bid price for ' + symbol + '(' + shortName + ') is $' + str(
                    bid_price) + '. The Bid size is ' + str(
                    bid_size) + ', the ask price is $' + str(ask_price) + ',the ask size is ' + str(ask_size) +
                             ',the quote type is ' + str(quoteType) + ', \nthe regular market price is $' + str(
                    regularMarketPrice) + ', \nhigh is $' + str(
                    regularMarketDayHigh) + ', \nlow is $' + str(
                    regularMarketDayLow) + '\nthe regular market open is $' + str(
                    regularMarketOpen) + ', \nand the exchange timezone is ' + str(
                    exchangeTimezoneName) + '</strong>'
            )
            sg = SendGridAPIClient(auth.EMAIL_API)
            print("connected...")
            response = sg.send(message)

            time.sleep(14400)
            print("Message sent successfully.")

    time.sleep(14400)


robinhood()
