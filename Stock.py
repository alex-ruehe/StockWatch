
class Stock:
    """
    Represents one stock. Each stock can have multiple orders (at least one)
    """
    def __init__(self, symbol, name, date, price, quantity):
        """ Create new stock
        :param symbol: stock symbol e.g. GOOG
        :param name: name of the company behind the stock symbol - choose what you want
        :param date: when was the order placed
        :param price: price per stock in this order
        :param quantity: number of stocks
        :return: nothing
        """
        self.symbol = symbol
        self.name = name
        self.orders = {date: {'quantity': quantity, 'price': price}}

    def add(self, date, price, quantity):
        """ Add new order to a stock
        :param date: when was the order placed
        :param price: price per stock in this order
        :param quantity: number of stocks
        :return: nothing
        """
        self.orders.update({date: {'quantity': quantity, 'price': price}})