from unittest import TestCase

from oop.portfolio import Portfolio
from oop.option import Option

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
        pass

    def test_liability(self):
        pass

    def test_update_data(self):
        pass

    def test_trade_summary(self):
        pass
