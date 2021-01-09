import robin_stocks as r
import pyotp as pt
import random
import time
import smtplib
import auth

# from pyrh import Robinhood

# r = Robinhood()

totp = pt.TOTP(auth.OTP_AUTH).now()

login = r.login(username=auth.USER_NAME, password=auth.PASSWORD,
                mfa_code=totp)
data = []

stock_result = []

# print(rand_tickers, stock_quote)
# print(historical_quotes['bid_price'])\

with open('tickers.txt') as f:
    tickers = f.read().splitlines()

# tickers = ['AAPL', 'AMZN', 'GOOG', 'NVDA', 'HPE', 'FIT',
#            'AMC', 'BAC', 'DGLY', 'TEUM']

rand_tickers = random.choice(tickers)

historical_quotes = r.get_stock_quote_by_symbol(symbol=rand_tickers)

stock_quote = r.get_latest_price(rand_tickers, includeExtendedHours=True)

data.append(historical_quotes)

# time.sleep(5)

symbol = str(historical_quotes['symbol'])
bid_price = int(float(historical_quotes['bid_price']))
bid_size = str(historical_quotes['bid_size'])
ask_price = str(historical_quotes['ask_price'])
ask_size = str(historical_quotes['ask_size'])
last_trade_price = str(historical_quotes['last_trade_price'])
last_extended_hours_trade_price = str(
    historical_quotes['last_extended_hours_trade_price'])
has_traded = str(historical_quotes['has_traded'])
last_trade_price_source = str(historical_quotes['last_trade_price_source'])
updated_at = str(historical_quotes['updated_at'])
instrument = str(historical_quotes['instrument'])

# print(historical_quotes)

# if int(float(historical_quotes['bid_price'][0])) <= 5:
#     time.sleep(5)
#     print("Symbol: " + str(historical_quotes['symbol']))
#     print("Ask Price: " + str(historical_quotes['ask_price']))
#     print("Ask Size: " + str(historical_quotes['ask_size']))
#     print("Bid Price: " + str(historical_quotes['bid_price']))
#     print("Bid Size: " + str(historical_quotes['bid_size']))
#     print("Last Trade Price: " + str(historical_quotes['last_trade_price']))
#     print("Last Extended Hours Trade Price: " + str(historical_quotes['last_extended_hours_trade_price']))
#     print("Has Traded: " + str(historical_quotes['has_traded']))
#     print("Last Trade Price Source: " + str(historical_quotes['last_trade_price_source']))
#     print("Updated At: " + str(historical_quotes['updated_at']))
#     print("Instrument: " + str(historical_quotes['instrument']))
#
# # time.sleep(300)
#
# time.sleep(5)
message = f'''The Bid price for {symbol} is {bid_price}. \n
                The Bid size is {bid_size}, the ask price is {ask_price},
        the ask size is {ask_size}, the last traded price is {last_trade_price}, and 
    it was updated at {updated_at}'''
if bid_price < 5.000000:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(auth.USER_NAME, auth.GMAIL_PASS)
    print("connected to gmail...")

    # message = f"""\n{data}"""
    time.sleep(2)
    server.sendmail(auth.USER_NAME, auth.USER_NAME, message)
    server.quit()

# if __name__ == '__main__':
#     while True:
#         stock_alert()
#         # email()
#         time.sleep(300)
