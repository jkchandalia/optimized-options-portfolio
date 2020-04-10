from unittest import TestCase

from oop.option import Option

EQUITY = 'TSLA'
OPTION_TYPE = 'CALL'
STRIKE = 700
DATE = '2020-06-19'

class TestOptionInit(TestCase):
    def test_init(self):
        with self.assertRaises(Exception):
            o = Option(EQUITY, OPTION_TYPE, STRIKE, '2020-06-18')

class TestOption(TestCase):
    def setUp(self):
        self.option = Option(EQUITY, OPTION_TYPE, STRIKE, DATE)

    def test_equity(self):
        self.assertTrue(self.option.equity, EQUITY)

    def test_option_type(self):
        self.assertTrue(self.option.option_type, OPTION_TYPE)

    def test_strike(self):
        self.assertTrue(self.option.strike, STRIKE)

    def test_date(self):
        self.assertTrue(self.option.exp_date, DATE)

    def test_get_market_data(self):
        api_data = Option.get_market_data(self.option.params)
        self.assertIn('status', api_data)

    def test_parse_api_data(self):
        api_data = self.option.get_market_data(self.option.params)
        self.option.parse_api_data(api_data)

    def test_margin(self):
        self.option.equity_price = 1000
        self.option.mark = 50
        self.assertEqual(self.option.margin,20000)

    def test_update_data(self):
        pass
