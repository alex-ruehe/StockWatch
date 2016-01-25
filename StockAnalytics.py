from StockCollection import StockCollection
import datetime
import ystockquote
from typing import Dict, List


class StockAnalytics:

    def __init__(self, collection: StockCollection) -> None:
        """
        :param collection: a collection of stocks
        :type collection: StockCollection
        :return: None
        :rtype: None
        """

        self.stock_collection = collection

        # calculate start and end date & format

        self.end_date = datetime.datetime.today() - datetime.timedelta(days=1)  # type: date
        self.start_date = self.end_date - datetime.timedelta(days=5)  # type: date

        self.end_date = datetime.datetime.strftime(self.end_date,'%Y-%m-%d')
        self.start_date = datetime.datetime.strftime(self.start_date, '%Y-%m-%d')

    def get_data_for_last_week(self) -> Dict[str, List[float]]:
        """ Get adjusted closing prices for stocks in the last 5 days
        :return: dictionary containing adj. closing prices
        :rtype:
        """

        adj_close_prices = {}

        for stock in self.stock_collection.get_stock_list():
            values = ystockquote.get_historical_prices(stock.symbol, self.start_date, self.end_date)

            adj_close = []
            for d in sorted(values):
                adj_close.append(values[d]['Adj Close'])

            adj_close_prices[stock.symbol] = adj_close

        return adj_close_prices

    def generate_message(self):
        msg = ''  # type: str
        adj_close = self.get_data_for_last_week()
        for stock in self.stock_collection.get_stock_list():
            msg += stock.symbol + '\n'

            diff = float(adj_close[stock.symbol][0]) - float(adj_close[stock.symbol][-1])

            if diff < 0.0:
                msg += "\t - increased by {0:4.3f} in the last {1:1d} days\n".format(-1*diff, len(adj_close[stock.symbol]))
            else:
                msg += "\t - decreased by {0:4.3f} in the last {1:1d} days\n".format(diff, len(adj_close[stock.symbol]))

            for order in stock.orders.keys():
                price = stock.orders[order]['price']

                tmp_date = datetime.datetime.strptime(order,"%Y-%m-%d")
                new_date = datetime.datetime.strftime(tmp_date, "%b %Y")

                diff = float(adj_close[stock.symbol][-1]) - float(price)
                quant = stock.orders[order]['quantity']
                if diff >= 0.0:
                    msg += "\t - you {0:6s} {1:7.3f} per stock since buying {2:3d} stocks in {3:10s}\n".format('gained', diff, quant,
                                                                                                             new_date)
                else:
                    msg += "\t - you {0:6s} {1:7.3f} per stock since buying {2:3d} stocks in {3:10s}\n".format('lost', -1*diff, quant,
                                                                                                            new_date)

        msg += "\n"
        return msg

    def mail_data(self, msg):
        self.stock_collection.send_mail(msg)