import datetime
from collections import deque

class Portfolio:
    def __init__(self, name, margin_available=0):
        self.name = name
        self.options = []
        self.margin_available = margin_available

    def add_option(self, option, count):
        for i in range(count):
            self.options.append(option)
        return self
    
    def remove_option(self, option, count):
        for i in range(count):
            self.options.remove(option)
        return self

    def _calculate_strangle_margin(self, option_call, option_put):
        return min(option_call.margin+100*option_put.mark,option_put.margin+100*option_call.mark )

    def _calculate_margin(self):
        margin = 0
        calls = deque()
        puts = deque()
        counter_put = 0
        counter_call = 0
        for option in self.options:
            if option.option_type == 'CALL':
                calls.append(option)
            elif option.option_type == 'PUT':
                puts.append(option)
        for i in range(min(len(calls), len(puts))):
            margin_delta = self._calculate_strangle_margin(calls.popleft(),puts.pop())
            margin += margin_delta
        if puts:
            while puts:
                margin += puts.pop().margin
        else:
            while calls:
                margin += calls.pop().margin
        margin = margin * 2
        return int(round(margin,-2))

    @property
    def margin(self):
        return self._calculate_margin()

    @property
    def liability(self):
        return self._calculate_liability()

    def _calculate_liability(self):
        liability = 0
        for option in self.options:
            liability = liability + 100 * option.mark
        return liability

    def update_data(self):
        for option in set(self.options):
            option.update_data() 

    @property
    def trade_summary(portfolio):
        msg = []
        msg.append(f'Net portfolio liability is {portfolio.liability}')
        calls = 0
        puts = 0
        for option in portfolio.options:
            if option.option_type == 'CALL':
                calls += 1
            elif option.option_type == 'PUT':
                puts += 1
        msg.append(f'Number of calls is {calls}; number of puts is {puts}')
        
        for option in portfolio.options:
            date_delta = datetime.datetime.strptime(str(option.exp_date)  , '%Y-%m-%d') - datetime.datetime.now()
            days_to_expiry = date_delta.days
            if datetime.datetime.strptime(str(option.exp_date)  , '%Y-%m-%d') - datetime.datetime.now()<datetime.timedelta(days=7):
                msg.append(f'The option {option.symbol} needs to be rolled or closed within the next {days_to_expiry} days. It has a value of {option.mark}')
            if  datetime.datetime.now() > datetime.datetime.strptime(str(option.exp_date)  , '%Y-%m-%d'):
                msg.append(f'The option {option.symbol} has expired and portfolio needs to be updated.')
            if option.option_type=='CALL' and option.strike<option.equity_price:
                msg.append(f'For call option {option.symbol}, strike has been breached. In the money by {option.equity_price-option.strike}')
            if option.option_type=='PUT' and option.strike>(option.equity_price*0.98):
                msg.append(f'For put option {option.symbol}, strike is within danger range. Time to roll.')
            if option.equity=='$RUT.X' and option.option_type == 'PUT':
                    if 100*option.mark/days_to_expiry < 20 and days_to_expiry<90:
                        msg.append(f'The option {option.symbol} of value {option.mark} expiring {option.exp_date} has decayed and could be rolled.')
            elif option.equity=='$RUT.X' and option.option_type == 'CALL':
                    if 100*option.mark/days_to_expiry < 16 and days_to_expiry<90:
                        msg.append(f'The option {option.symbol} of value {option.mark} expiring {option.exp_date} has decayed and could be rolled.')

        trade_instructions = " ".join(msg) 
        if not(msg):
            msg.append("No changes needed.")
        print(' '.join(msg))

    