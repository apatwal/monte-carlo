import pandas as pd
import numpy as np
import streamlit as st
import yfinance as yf

import matplotlib.pyplot as plt
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.datasets import load_boston
from sklearn.metrics import mean_squared_error

st.title('Monte Carlo Asset Pricing Simulation')
ticker = st.text_input('Enter Stock Ticker', 'SPOT')
stock_data = yf.download(ticker, period='6mo')
st.write(stock_data)