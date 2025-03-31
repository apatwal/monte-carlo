import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import pandas as pd
import numpy as np
import streamlit as st
from backend.data_cleaning import clean_and_prepare_data
from backend.data_collection import fetch_stock_data, save_stock_data_toCSV

# st.title('Monte Carlo Asset Pricing Simulation')
st.title('📈 Stock Data Viewer')

# Create page navigation
st.sidebar.info("Select Page")

# create input fields
ticker = st.text_input("Enter Stock Ticker (e.g., MSFT, AAPL):", value="MSFT")
start_date = st.date_input("Select Start Date")
end_date = st.date_input("Select End Date")
intervals = ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"]
interval = st.selectbox("Select Interval", intervals, index=intervals.index("1d"))

if ticker:
    st.session_state.ticker = ticker

if start_date:
    st.session_state.start_date = start_date

if end_date:
    st.session_state.end_date = end_date

if interval:
    st.session_state.interval = interval

# create a button to fetch the data
if st.button("Fetch Data"):
    if start_date >= end_date:
        st.error("End date must be after start date.")
    else:
        # Fetch data and write it to a file
        df = fetch_stock_data(ticker, str(start_date), str(end_date), interval)
        current_file = os.path.abspath(__file__)
        project_root = os.path.abspath(os.path.join(current_file, "../../../"))
        data_folder = os.path.join(project_root, "data")
        filename = f"{ticker}_{start_date}_to_{end_date}_{interval}_processed.csv"
        file_path = os.path.join(data_folder, "processed", filename)
        clean = clean_and_prepare_data(df, save_path = file_path)

        # Add query to list of queries file
        queries = pd.read_csv(os.path.join(data_folder, "queries.csv"))
        new_file = pd.DataFrame({"filenames": [filename]})
        queries = pd.concat([queries, new_file], ignore_index = True)
        queries.to_csv(os.path.join(data_folder, "queries.csv"))

        if df is not None:
            st.subheader(f"Stock Data for {ticker}")
            st.write(df)
            st.line_chart(df["Close"])
        else:
            st.warning("No data found. Check ticker or date range.")




