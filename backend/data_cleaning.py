import pandas as pd
import numpy as np
import os

def clean_and_prepare_data(df, save_path=None):
    """
    Clean and prepare stock data for analysis.
    
    Parameters:
    df (DataFrame): Raw stock data DataFrame from yfinance
    save_path (str, optional): Path to save the processed data
    
    Returns:
    DataFrame: Cleaned and processed stock data
    """
    print("Starting...")
    

    processed_df = df.copy()
    

    

    if isinstance(processed_df.columns, pd.MultiIndex):
        print("Detected multi-level columns, printing first column to debug:")
        print(f"First column: {processed_df.columns[0]}")
        

        processed_df.columns = [col[0] for col in processed_df.columns]
        print(f"Columns after flattening: {processed_df.columns.tolist()}")
    

    if not isinstance(processed_df.index, pd.DatetimeIndex):
        processed_df.index = pd.to_datetime(processed_df.index)
    

    print(f"Missing values before imputation: {processed_df.isna().sum().sum()}")
    

    processed_df = processed_df.ffill()
    

    processed_df = processed_df.bfill()
    
    print(f"Missing values after imputation: {processed_df.isna().sum().sum()}")
    

    if 'Close' in processed_df.columns:
        price_col = 'Close'
        print(f"Using 'Close' column for price calculations")
    else:
        print(f"'Close' column not found. Searching for suitable price column...")
        

        price_cols = ['Adj Close', 'Price', 'Last', 'Last Price']
        for col in price_cols:
            if col in processed_df.columns:
                price_col = col
                print(f"Using '{price_col}' as price column")
                break
        else:

            numeric_cols = [col for col in processed_df.columns 
                          if pd.api.types.is_numeric_dtype(processed_df[col]) and 
                          col != 'Volume']
            
            if numeric_cols:
                price_col = numeric_cols[0]
                print(f"Using '{price_col}' as price column (first numeric column)")
            else:
                print("ERROR: No suitable price column found.")
                print(f"Available columns: {processed_df.columns.tolist()}")
                print(f"Sample data:\n{processed_df.head()}")

    

    processed_df['Daily_Return'] = processed_df[price_col].pct_change() * 100
    

    processed_df['Cumulative_Return'] = (1 + processed_df['Daily_Return']/100).cumprod() - 1
    processed_df['Cumulative_Return'] = processed_df['Cumulative_Return'] * 100
    

    processed_df['Volatility_5d'] = processed_df['Daily_Return'].rolling(window=5).std()
    

    processed_df['MA_5d'] = processed_df[price_col].rolling(window=5).mean()
    

    if 'Volume' in processed_df.columns:
        processed_df['Volume_Change'] = processed_df['Volume'].pct_change() * 100
        processed_df['Volume_MA_5d'] = processed_df['Volume'].rolling(window=5).mean()
    

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        processed_df.to_csv(save_path)
        print(f"Processed data saved to {save_path}")
    
    print("Data cleaning and preparation completed.")
    return processed_df

def main():
    from data_collection import fetch_stock_data
    
    ticker = 'MSFT'
    start_date = '2025-03-10'
    end_date = '2025-03-20'
    
    raw_data = fetch_stock_data(ticker, start_date, end_date)
    
    if raw_data is not None:
        processed_data_dir = os.path.join(os.path.dirname(__file__), '../data/processed')
        os.makedirs(processed_data_dir, exist_ok=True)
        processed_file_path = os.path.join(processed_data_dir, f"{ticker}_{start_date}_to_{end_date}_processed.csv")
        
        processed_data = clean_and_prepare_data(raw_data, save_path=processed_file_path)
        
        print(processed_data.head())
        
if __name__ == "__main__":
    main()