import yfinance as yf

import os
# the format of a date is YYYY-MM-DD
# format of an interval is [1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo] defaults to 1d
# call it by setting a dataframe = fetch_stock_date()
def fetch_stock_data(ticker, start_date, end_date, interval="1d"):
    try:
        print(f'Fetching data for {ticker} from {start_date} to {end_date} at interval {interval}')

        stock_data = yf.download(ticker, start=start_date, end=end_date, interval=interval)
        if stock_data.empty:
            print("No data found. Check ticker symbol or date range.")
            return None
        
        return stock_data
    except Exception as e:
        print(f'Caught error: {e}')
        return None
    
def save_stock_data_toCSV(ticker, start_date, end_date, intervals = "1d"):
    raw_data_dir = os.path.join(os.path.dirname(__file__), '../data/raw')
    filename = f"{ticker}_{start_date}_to_{end_date}_{intervals}.csv"
    file_path = os.path.join(raw_data_dir, filename)
    stock_data = fetch_stock_data(ticker, start_date, end_date, intervals)
    stock_data.to_csv(file_path)
    print(f"Data saved to {file_path}")
    return


