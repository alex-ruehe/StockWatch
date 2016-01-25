# coding=utf-8
from StockCollection import StockCollection
import ystockquote
import datetime

my_stocks = StockCollection()

# calculate start and end date - since the script is supposed to be called on saturdays and we want
# the last week only we end at today-1 (= SA - 1 = FR) and begin 5 days earlier

end_date = datetime.datetime.today() - datetime.timedelta(days=1)
start_date = end_date - datetime.timedelta(days=5)

end_date = datetime.datetime.strftime(end_date ,'%Y-%m-%d')
start_date = datetime.datetime.strftime(start_date, '%Y-%m-%d')

# iterate over all stocks
mail_data = ""
for stock in my_stocks.get_stock_list():
    values = ystockquote.get_historical_prices(stock.symbol, start_date, end_date)

    mail_data += stock.symbol + '\n'

    # get closing prices for every day
    adj_close = []
    for d in sorted(values):
        adj_close.append(values[d]['Adj Close'])

    # calculate win/loss of the last 5 days
    diff = float(adj_close[0]) - float(adj_close[-1])

    if diff < 0.0:
        mail_data += "\t - increased by {0:4.3f} in the last {1:1d} days\n".format(-1*diff, len(adj_close))
    else:
        mail_data += "\t - decreased by {0:4.3f} in the last {1:1d} days\n".format(diff, len(adj_close))

    # calculate win/loss of stocks based on buying price for each order relative to last adj closing price
    # iterate over each order for a certain stock

    for order in stock.orders.keys():
        price = stock.orders[order]['price']

        tmp_date = datetime.datetime.strptime(order,"%Y-%m-%d")
        new_date = datetime.datetime.strftime(tmp_date, "%b %Y")

        diff = float(adj_close[-1]) - float(price)
        quant = stock.orders[order]['quantity']
        if diff >= 0.0:
            mail_data += "\t - you {0:6s} {1:7.3f} per stock since buying {2:3d} stocks in {3:10s}\n".format('gained', diff, quant, new_date)
        else:
            mail_data += "\t - you {0:6s} {1:7.3f} per stock since buying {2:3d} stocks in {3:10s}\n".format('lost', -1*diff, quant, new_date)

    mail_data += "\n"

my_stocks.send_mail(mail_data)