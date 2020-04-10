from unittest import TestCase

from oop.option import Option
from oop.portfolio import Portfolio

EQUITY = 'TSLA'
OPTION_TYPE = 'CALL'
STRIKE = 700
DATE = '2020-06-19'


class TestPortfolioInit(TestCase):
    def test_init(self):
        with self.assertRaises(TypeError):
            p = Portfolio()


class TestPortfolio(TestCase):
    def setUp(self):
        self.portfolio = Portfolio('test')
        self.option = Option(EQUITY, OPTION_TYPE, STRIKE, DATE)

    def test_add_option(self):
        self.portfolio.add_option(self.option, 1)
        self.assertEqual(self.portfolio.options[0], self.option)

    def test_remove_option(self):
        self.portfolio.add_option(self.option, 3)
        self.portfolio.remove_option(self.option, 1)
        self.assertEqual(len(self.portfolio.options), 2)

    def test_margin(self):
        self.portfolio.add_option(self.option, 1)
        self.option.equity_price = 1000
        self.option.mark = 50
        self.assertEqual(self.portfolio.margin,40000)

    def test_strangle_margin(self):
        self.portfolio.add_option(self.option, 1)
        self.option.equity_price = 1000
        self.option.mark = 50
        put_option = Option(EQUITY, 'PUT', 300, DATE)
        put_option.equity_price = self.option.equity_price
        put_option.mark = 50
        self.portfolio.add_option(put_option, 1)
        strangle_margin = 2 * min(self.option.margin+100*put_option.mark,put_option.margin+100*self.option.mark)
        self.assertEqual(self.portfolio.margin,strangle_margin)

    def test_liability(self):
        self.portfolio.add_option(self.option, 1)
        self.option.mark = 50
        self.assertEqual(self.portfolio.liability, 5000)

    def test_update_data(self):
        self.portfolio.add_option(self.option, 1)
        self.portfolio.update_data()

    def test_trade_summary(self):
        self.assertIsInstance(self.portfolio.trade_summary, str)
