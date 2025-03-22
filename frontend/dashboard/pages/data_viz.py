import streamlit as st
import altair as alt
import pandas as pd
import os

st.title("Exploratory Data Analysis")

current_file = os.path.abspath(__file__)
project_root = os.path.abspath(os.path.join(current_file, "../../../../"))
data_folder = os.path.join(project_root, "data", "processed")

ticker = st.session_state.get('ticker')
start_date = st.session_state.get('start_date')
end_date = st.session_state.get('end_date')


filename = f"{ticker}_{start_date}_to_{end_date}_processed.csv"
data_path = os.path.join(data_folder, filename)
data = pd.read_csv(data_path)

close_line = alt.Chart(data).mark_line(color = "red").encode(
    x = "Date",
    y = "Close"
).interactive()

return_line = alt.Chart(data).mark_line(color = "blue").encode(
    x = "Date",
    y = "Daily_Return"
).interactive()

st.subheader(f"Closing Price From {start_date} to {end_date}")
st.altair_chart(close_line)

st.subheader(f"Daily Returns From {start_date} to {end_date}")
st.altair_chart(return_line)
