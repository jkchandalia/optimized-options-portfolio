import os
import requests

TD_AMERITRADE_API_KEY = os.environ['TD_AMERITRADE_API_KEY']
ENDPOINT = "https://api.tdameritrade.com/v1/marketdata/chains"

class Option:
    def __init__(self, equity, option_type, strike, exp_date):
        params={"apikey": TD_AMERITRADE_API_KEY,
                "symbol": equity,
                "contractType": option_type.upper(),
                "strike": str(strike),
                "fromDate": exp_date,
                "toDate": exp_date}
        
        validation = Option.get_market_data(params)
        if not(validation):
            raise Exception('Parameters are not a valid option.')
        else:
            self.equity = equity
            self.option_type = option_type.upper()
            self.strike = strike
            self.exp_date = exp_date
            self.params = params
            self.parse_api_data(validation)
                        
    @classmethod
    def get_market_data(cls, params):
        content = requests.get(url = ENDPOINT, params = params)
        api_data=content.json()
        if api_data['status'] == 'FAILED':
            return False
        elif api_data['status'] == 'SUCCESS':
            return api_data
    
    def parse_api_data(self, api_data):
        self.equity_price = api_data['underlyingPrice']
        if self.option_type == 'CALL':
            data=api_data['callExpDateMap']
        elif self.option_type == 'PUT':
            data=api_data['putExpDateMap']

        for date_key in data:
            for price_key in data[date_key]:
                values=data[date_key][price_key][0]
                self.symbol = values['symbol']
                self.description = values['description']
                self.bid = values['bid']
                self.ask = values['ask']
                self.mark = values['mark']
                self.delta = values['delta']
                self.theta = values['theta']
                self.gamma = values['gamma']
                self.vega = values['vega']
                self.daysToExpiration = values['daysToExpiration']
                    
    def _calculate_margin(self):
        # http://www.cboe.com/LearnCenter/pdf/margin2-00.pdf
        if self.option_type == "CALL":
            margin = max(100 * (self.mark + self.equity_price*.15 + min(0,self.equity_price - self.strike)),10*self.equity_price+self.mark*100)
        elif self.option_type == "PUT":
            margin = max(100 * (self.mark + self.equity_price*.15 + min(0,self.strike-self.equity_price)),10*self.strike+self.mark*100)
        return margin
        
    @property
    def margin(self):
        return self._calculate_margin()

    def update_data(self):
        api_data = Option.get_market_data(self.params)
        self.parse_api_data(api_data)