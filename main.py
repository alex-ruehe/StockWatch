# coding=utf-8
from StockCollection import StockCollection
from StockAnalytics import StockAnalytics

my_stocks = StockCollection()

cus_sa = StockAnalytics(my_stocks)

my_stocks.send_mail(cus_sa.generate_message())
