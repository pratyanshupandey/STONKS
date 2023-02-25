from pprint import pprint
from datetime import date
from jugaad_data.nse import stock_df
import pandas as pd
import os

nifty_50 = pd.read_csv("data/ind_nifty50list.csv")
for company in nifty_50["Symbol"]:
    print(company)
    df = stock_df(symbol=company, from_date=date(2015, 1, 1),
                to_date=date(2023, 2, 25), series="EQ")
    df.to_csv("data/stock_data/" + company + ".csv")