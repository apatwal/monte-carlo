import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import pandas as pd
import numpy as np
import streamlit as st

from backend.data_collection import fetch_stock_data

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

# create a button to fetch the data
if st.button("Fetch Data"):
    if start_date >= end_date:
        st.error("End date must be after start date.")
    else:
        df = fetch_stock_data(ticker, str(start_date), str(end_date), interval)
        if df is not None:
            st.subheader(f"Stock Data for {ticker}")
            st.write(df)
            st.line_chart(df["Close"])
        else:
            st.warning("No data found. Check ticker or date range.")




