import pandas as pd
from utils import State, Action
from indicators import EMA
import matplotlib.pyplot as plt


class Simulator:
    def __init__(self, symbol) -> None:
        self.symbol = symbol
        
        self.df = pd.read_csv("data/stock_data/" + symbol + ".csv")
        # reverse order of pandas dataframe
        self.df = self.df.iloc[::-1]
        self.df = self.df.reset_index(drop=True)

        # portfolio
        self.state = State.NONE
        self.holdings = 0
        self.wallet = 10_000
        


        # indicators
        self.ema = EMA(50, ema_init=self.df["CLOSE"][0])

        # delete first row
        self.df = self.df.drop(0)

        # history
        self.trade_history = []
        self.valuation_history = []


    def current_valuation(self, price):
        return self.wallet + self.holdings * price

    
    def simulate(self):
        for index, row in self.df.iterrows():
            date = row["DATE"]
            open = row["OPEN"]
            high = row["HIGH"]
            low = row["LOW"]
            close = row["CLOSE"]
            volume = row["VOLUME"]
            vwap = row["VWAP"]
            self.strategy(date, open, high, low, close, volume, vwap)
            self.valuation_history.append(self.current_valuation(close))
        
        if self.state == State.LONG:
            self.sell(self.holdings, close, date)
        elif self.state == State.SHORT:
            self.buy(1, close, date)
        self.state = State.NONE
        self.valuation_history.append(self.current_valuation(close))

    
    def strategy(self, date, open, high, low, close, volume, vwap):
        action = self.ema(close, self.state)
        if action == Action.LONG:
            self.buy(1, close, date)
            self.state = State.LONG
        elif action == Action.SHORT:
            self.sell(1, close, date)
            self.state = State.SHORT
        elif action == Action.SQUARE_OFF:
            if self.state == State.LONG:
                self.sell(1, close, date)
            elif self.state == State.SHORT:
                self.buy(1, close, date)
            self.state = State.NONE


    def trade(self, volume, price, date):
        self.holdings += volume
        self.wallet -= price * volume
        self.trade_history.append((date, volume, price))


    def sell(self, volume, price, date):
        volume = abs(self.holdings)
        return self.trade(-volume, price, date)


    def buy(self, volume, price, date):
        volume = int(self.wallet / price)
        return self.trade(volume, price, date)


    def plot_valuation(self):
        plt.plot(self.valuation_history)
        plt.savefig("value.png")


if __name__ == "__main__":
    nifty_50 = pd.read_csv("data/ind_nifty50list.csv")
    pnl_total = 0
    for company in nifty_50["Symbol"][1:]:
        sim = Simulator(company)
        init_wallet = sim.wallet

        sim.simulate()

        print("\n" + company)
        # print("Final Wallet:", sim.wallet)
        print("PnL:", 100 * sim.wallet / init_wallet - 100)
        pnl_total += 100 * sim.wallet / init_wallet - 100
        # print("Holdings: ", sim.holdings)
        # print("Trades count: ", len(sim.trade_history))
        print()
        # sim.plot_valuation()
    print("Average PnL:", pnl_total / 50)