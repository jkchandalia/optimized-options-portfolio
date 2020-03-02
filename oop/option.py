from collections import deque
import datetime
import os
import requests

TD_AMERITRADE_API_KEY = os.environ['TD_AMERITRADE_API_KEY']
ENDPOINT = "https://api.tdameritrade.com/v1/marketdata/chains"

class Option:
    def __init__(equity, type, strike, exp_date):
        params={"apikey": TD_AMERITRADE_API_KEY,
                "symbol": equity,
                "contractType": contractType.upper(),
                "strike": str(strike),
                "fromDate": exp_date,
                "toDate": exp_date}
        
        validation = cls.get_market_data(params)
        equity = models.CharField(max_length=255)
        strike = models.IntegerField()
        exp_date = models.DateField()
        option_type = models.CharField(max_length=255)
        bid = models.FloatField()
        ask = models.FloatField()
        mark = models.FloatField()
        delta = models.FloatField()
        theta = models.FloatField()
        gamma = models.FloatField()
        vega = models.FloatField()
        equity_price = models.FloatField()
        flavor = models.CharField(max_length=255)
        desc = models.CharField(max_length=255)
        symbol = models.CharField(max_length=255)
        # daysToExpiration = models.IntegerField(default=None)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)
        objects = OptionsManager()
    
    @classmethod
    def get_market_data(cls, params):
        content = requests.get(url = data.endpoint, params = params)
        api_data=content.json()
        if api_data['status'] == 'FAILED':
            return False
        elif api_data['status'] == 'SUCCESS':
            output = parse_api_data(api_data, params)

        return output
    
    def _calculate_margin(self):
        # http://www.cboe.com/LearnCenter/pdf/margin2-00.pdf
        # print(self.equity_price)
        # print(self.mark)
        if self.option_type == "CALL":
            margin = max(100 * (self.mark + self.equity_price*.15 + min(0,self.equity_price - self.strike)),10*self.equity_price+self.mark*100)
        elif self.option_type == "PUT":
            margin = max(100 * (self.mark + self.equity_price*.15 + min(0,self.strike-self.equity_price)),10*self.strike+self.mark*100)
        return margin

    def _update_w_api_data(self):
        self.api_data = requests.get(url = ENDPOINT, params = self.query_params).json()
        self._parse_api_data()
        self.save()

    def _parse_api_data(self):
        self.equity_price = self.api_data['underlyingPrice']
        if self.option_type == 'CALL':
            data=self.api_data['callExpDateMap']
        elif self.option_type == 'PUT':
            data=self.api_data['putExpDateMap']

        for date_key in data:
            for price_key in data[date_key]:
                # print(price_key)
                values=data[date_key][price_key][0]
                # print(values.keys())
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
                    
    @property
    def margin(self):
        return self._calculate_margin()

    @property
    def query_params(self):
        params={"apikey": data.client_id,
        "symbol": self.equity,
        "contractType": self.option_type.upper(),
        "strike": self.strike,
        "fromDate": self.exp_date,
        "toDate": self.exp_date}
        return params


    def update_data(self):
        self._update_w_api_data()

        if option_exists:
            option = option_exists[0]
            option_count = QuantityOptions.objects.filter(user=user, option=option)
            if option_count:
                count = option_count[0]
                count.option_count += int(f['quantity'])
                count.save()
                return redirect("/portfolio/options")
            else:
                QuantityOptions.objects.create(
                    option_count=int(f['quantity']),
                    user=user,
                    option=option)
                return redirect("/portfolio/options")
        else:
            output = get_market_data(params)
            if output:
                new_option = Option.objects.create(
                    equity=params['symbol'],
                    strike=output['strike'],
                    exp_date=output['exp_date'],
                    option_type=output['option_type'],
                    bid=output['bid'],
                    ask=output['ask'],
                    mark=output['mark'],
                    delta=output['delta'],
                    theta=output['theta'],
                    gamma=output['gamma'],
                    vega=output['vega'],
                    equity_price=output['equity_price'],
                    flavor=output['flavor'],
                    desc=output['description'],
                    symbol=output['symbol'])
                QuantityOptions.objects.create(option_count=int(f['quantity']), user=user, option=new_option)

                return redirect("/portfolio/options")
            else:
                messages.error(request, "The option was not found")
                return redirect("/portfolio/options")


