import streamlit as st
import altair as alt
import pandas as pd
import os

st.title("Exploratory Data Analysis")

current_file = os.path.abspath(__file__)
project_root = os.path.abspath(os.path.join(current_file, "../../../../"))
data_folder = os.path.join(project_root, "data", "processed")

ticker = st.session_state.get("ticker")
start_date = st.session_state.get("start_date")
end_date = st.session_state.get("end_date")
interval = st.session_state.get("interval")


filename = f"{ticker}_{start_date}_to_{end_date}_{interval}_processed.csv"
data_path = os.path.join(data_folder, filename)
try:
    data = pd.read_csv(data_path)
except FileNotFoundError:
    st.markdown("### Make a query on the _homepage_ to see data here.")
    st.stop()

price_stats = data["Close"].describe()
return_stats = data["Daily_Return"].describe()

price_mean = float(price_stats["mean"])
price_med = float(data["Close"].median())
price_var = float(data["Close"].var())
price_std = float(price_stats["std"])

return_mean = float(return_stats["mean"])
return_med = float(data["Daily_Return"].median())
return_var = float(data["Daily_Return"].var())
return_std = float(return_stats["std"])


st.subheader(f'{ticker}\'s Basic Stats')
st.markdown(f"""
📊 Price
- **Mean:** `{price_mean:.4f}`
- **Median:** `{price_med:.4f}`
- **Variance:** `{price_var:.4f}`
- **Standard Deviation:** `{price_std:.4f}`
""")

st.markdown(f"""
📊 Returns
- **Mean:** `{return_mean:.4%}`
- **Median:** `{return_med:.4%}`
- **Variance:** `{return_var:.4%}`
- **Standard Deviation:** `{return_std:.4%}`
""")

def close_line():
    close_line = alt.Chart(data).mark_line(color = "red").encode(
        x = "Date:T",
        y = "Close",
    ).interactive()

    return close_line

def return_line():
    return_line = alt.Chart(data).mark_line(color = "green").encode(
        x = "Date:T",
        y = "Daily_Return",
    ).interactive()
    return return_line

def moving_avg(win):
    # Add legend
    if win == 50:
        ma_line = alt.Chart(data).mark_line(color="blue").encode(
            x="Date:T",
            y="MA_50d",
        ).interactive()
    elif win == 20:
        ma_line = alt.Chart(data).mark_line(color="blue").encode(
            x="Date:T",
            y="MA_20d",
        ).interactive()
    return ma_line

def volatility_line():
    v_line = alt.Chart(data).mark_line(color="purple").encode(
        x="Date:T",
        y="Volatility_5d",
    ).interactive()
    return v_line

st.subheader(f"Closing Price From {start_date} to {end_date}")
st.altair_chart(close_line())

st.subheader(f"Daily Returns From {start_date} to {end_date}")
st.altair_chart(return_line())

st.subheader("Moving Average Chart")
ma_win = st.selectbox("Window Size", (20, 50))
st.altair_chart(close_line() + moving_avg(ma_win))

st.subheader("Volatility Chart")
st.markdown("""
We define volatility as the standard deviation in returns on a 5 day rolling basis.
""")
st.altair_chart(volatility_line())

