import os
from dotenv import load_dotenv
import requests
import pandas as pd

load_dotenv()
apikey = os.getenv("API_KEY")

existing_files = {file.split("_")[0] for file in os.listdir("financial_data") if file.endswith("_financials.csv")}

with open("stocks.txt", "r") as file:
    stocks = [line.strip() for line in file.readlines() if line.strip() not in existing_files]

stock_data = {}
for stock in stocks:
    income_data = requests.get(f'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={stock}&apikey={apikey}').json()
    cashflow_data = requests.get(f'https://www.alphavantage.co/query?function=CASH_FLOW&symbol={stock}&apikey={apikey}').json()
    earnings_data = requests.get(f'https://www.alphavantage.co/query?function=EARNINGS&symbol={stock}&apikey={apikey}').json()
    print(income_data, cashflow_data, earnings_data)
    income_df = pd.DataFrame(income_data["annualReports"])
    cashflow_df = pd.DataFrame(cashflow_data["annualReports"])
    earnings_df = pd.DataFrame(earnings_data["quarterlyEarnings"])
    financials_df = pd.concat([income_df, cashflow_df, earnings_df], axis=1)
    financials_df = financials_df.loc[:,~financials_df.columns.duplicated()].copy()
    financials_df.to_csv(f"financial_data/{stock}_financials.csv")
