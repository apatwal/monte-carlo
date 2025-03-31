import streamlit as st
import altair as alt
import pandas as pd
import os

st.title("Exploratory Data Analysis")

current_file = os.path.abspath(__file__)
project_root = os.path.abspath(os.path.join(current_file, "../../../../"))
data_folder = os.path.join(project_root, "data")

ticker = st.session_state.get("ticker")
start_date = st.session_state.get("start_date")
end_date = st.session_state.get("end_date")
interval = st.session_state.get("interval")


filename = f"{ticker}_{start_date}_to_{end_date}_{interval}_processed.csv"
data_path = os.path.join(data_folder, "processed", filename)
queries = pd.read_csv(os.path.join(data_folder, "queries.csv"))
queries = queries.drop_duplicates().reset_index()

# define session variables for files so charts stay constant through page navigation
if "stats_file" not in st.session_state:
    st.session_state.stats_file = None
if "close_file" not in st.session_state:
    st.session_state.close_file = None
if "return_file" not in st.session_state:
    st.session_state.return_file = None
if "ma_file" not in st.session_state:
    st.session_state.ma_file = None
if "vol_file" not in st.session_state:
    st.session_state.vol_file = None

st.subheader("Basic Stats")
stats_file = st.selectbox("Select File from Previously Fetched Data", queries["filename"],
                          index = st.session_state.stats_file, key = "stats")
if stats_file:
    st.session_state.stats_file = queries.index[queries["filename"] == stats_file].tolist()[0]
    stats_data = pd.read_csv(os.path.join(data_folder, "processed", stats_file))

    price_stats = stats_data["Close"].describe()
    return_stats = stats_data["Daily_Return"].describe()

    price_mean = float(price_stats["mean"])
    price_med = float(stats_data["Close"].median())
    price_var = float(stats_data["Close"].var())
    price_std = float(price_stats["std"])

    return_mean = float(return_stats["mean"])
    return_med = float(stats_data["Daily_Return"].median())
    return_var = float(stats_data["Daily_Return"].var())
    return_std = float(return_stats["std"])

    st.markdown(f"""
    📊 Price
    - **Mean:** `{price_mean:.2f}`
    - **Median:** `{price_med:.2f}`
    - **Variance:** `{price_var:.2f}`
    - **Standard Deviation:** `{price_std:.2f}`
    """)

    st.markdown(f"""
    📊 Returns
    - **Mean:** `{return_mean:.2%}`
    - **Median:** `{return_med:.2%}`
    - **Variance:** `{return_var:.2%}`
    - **Standard Deviation:** `{return_std:.2%}`
    """)
else:
    st.markdown("""Select a dataset from the menu to display data""")

def close_line(close_data):
    close_line = alt.Chart(close_data).mark_line(color = "red").encode(
        x = "Date:T",
        y = "Close",
    ).interactive()

    return close_line

def return_line(return_data):
    return_line = alt.Chart(return_data).mark_line(color = "green").encode(
        x = "Date:T",
        y = "Daily_Return",
    ).interactive()
    return return_line

def moving_avg(ma_data, win):
    # Add legend
    if win == 50:
        ma_line = alt.Chart(ma_data).mark_line(color="blue").encode(
            x="Date:T",
            y="MA_50d",
        ).interactive()
    elif win == 20:
        ma_line = alt.Chart(ma_data).mark_line(color="blue").encode(
            x="Date:T",
            y="MA_20d",
        ).interactive()
    return ma_line

def volatility_line(vol_data):
    v_line = alt.Chart(vol_data).mark_line(color="purple").encode(
        x="Date:T",
        y="Volatility_5d",
    ).interactive()
    return v_line

st.subheader(f"Closing Price")
close_file = st.selectbox("Select File from Previously Fetched Data", queries["filename"],
                          index = st.session_state.close_file, key = "close")
if close_file:
    st.session_state.close_file = queries.index[queries["filename"] == close_file].tolist()[0]
    close_chart_data = pd.read_csv(os.path.join(data_folder, "processed", close_file))
    st.altair_chart(close_line(close_chart_data))
else:
    st.markdown("""Select a dataset from the menu to display data""")

st.subheader(f"Daily Returns")
return_file = st.selectbox("Select File from Previously Fetched Data", queries["filename"],
                           index = st.session_state.return_file, key = "return")
if return_file:
    st.session_state.return_file =  queries.index[queries["filename"] == return_file].tolist()[0]
    return_chart_data = pd.read_csv(os.path.join(data_folder, "processed", return_file))
    st.altair_chart(return_line(return_chart_data))
else:
    st.markdown("""Select a dataset from the menu to display data""")

st.subheader("Moving Average Chart")
ma_win = st.selectbox("Window Size", (20, 50))
ma_file = st.selectbox("Select File from Previously Fetched Data", queries["filename"],
                       index = st.session_state.ma_file, key = "ma")
if ma_file:
    st.session_state.ma_file = queries.index[queries["filename"] == ma_file].tolist()[0]
    ma_chart_data = pd.read_csv(os.path.join(data_folder, "processed", ma_file))
    st.altair_chart(close_line(ma_chart_data) + moving_avg(ma_chart_data, ma_win))
else:
    st.markdown("""Select a dataset from the menu to display data""")

st.subheader("Volatility Chart")
vol_file = st.selectbox("Select File from Previously Fetched Data", queries["filename"],
                        index = st.session_state.vol_file, key = "vol")
st.markdown("""
We define volatility as the standard deviation in returns on a 5 day rolling basis.
""")
if vol_file:
    st.session_state.vol_file = queries.index[queries["filename"] == vol_file].tolist()[0]
    vol_chart_data = pd.read_csv(os.path.join(data_folder, "processed", vol_file))
    st.altair_chart(volatility_line(vol_chart_data))
else:
    st.markdown("""Select a dataset from the menu to display data""")

