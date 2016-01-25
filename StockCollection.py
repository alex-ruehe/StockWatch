from Stock import Stock
import os
import configparser
import json


class StockCollection:
    """ A collection of Stocks which are loaded from a database or file
    """
    def __init__(self, configfile="config.cfg"):
        parser = configparser.ConfigParser()
        parser.read(configfile)
        self.owner = parser['User']['name']
        self.mail = parser['User']['mail']
        self.stock_symbols = {}
        self.stocks = []

        if parser['User']['source'] == 'file':
            self.stock_db_filename = parser['File']['filename']
            self.hist_data_db_filename = "text.txt"
        else:
            # handle DB connection here
            print('using db')

        self.load_stock_db()
        self.has_run_before = os.path.isfile(self.hist_data_db_filename)
        self.old_prices = {}

    def load_stock_db(self):
        # switch between reading from file and from db
        if self.stock_db_filename:

            # load the json array from file
            with open(self.stock_db_filename) as data_file:
                stocks_db = json.load(data_file)

            # add every stock to the stocks array
            for stock in stocks_db:
                symbol = stock['symbol']
                name = stock['name']
                # check if symbol / name was already added before
                for order in stock['orders']:
                    date = order['date']
                    price = order['price']
                    amount = order['amount']
                    self.add(symbol, name, date, price, amount)

    def load_old_prices(self):
        with open(self.hist_data_db_filename, "r") as last_run:
            for line in last_run:
                if line[0] != '#' and line[0] != '\n':
                    print(line, end='')

    def store_old_prices(self, data):
        with open(self.hist_data_db_filename, "w+") as output:
            output.truncate()
            for entry in data:
                symbol = entry[0]
                # wl = win/loss
                wl_5days_last_week = entry[1]
                wl_since_bought_last_week = entry[2]
                row = symbol + ', ' + wl_5days_last_week + ', ' + wl_since_bought_last_week + '\n'
                output.write(row)

    def add(self, symbol, name, date, price, quantity):
        if symbol in self.stock_symbols:
            # stock already in collections add as new order
            for s in self.stocks:
                if s.symbol == symbol:
                    s.add(date, price, quantity)
        else:
            # new stock - add to collection
            stock = Stock(symbol, name, date, price, quantity)
            self.stocks.append(stock)
            self.add_new_stock(symbol, name)

    def add_new_stock(self, symbol, name):
        if symbol in self.stock_symbols:
            return False
        else:
            self.stock_symbols[symbol] = name
            return True

    def get_stock_list(self):
        return self.stocks

    def send_mail(self, data):
        sendmail_location = "/usr/sbin/sendmail" # sendmail location
        p = os.popen("%s -t" % sendmail_location, "w")
        p.write("From: %s\n" % "Stock Watch<hello@aruehe.io>")
        p.write("To: %s\n" % "alex@dfghj.de")
        p.write("Subject: Your weekly stock watch report\n")
        p.write("\n") # blank line separating headers from body
        p.write(data)
        status = p.close()
        if status != 0:
               print("Sendmail exit status", status)