import streamlit as st
import matplotlib.pyplot as plt
from backend.monte_carlo import montecarlosim

st.title("Monte Carlo Pricing Simulation")


ticker = st.session_state.get("ticker")
simulations = st.slider("Number of Simulations", min_value=100, max_value=5000, step=100, value=1000)
days = st.slider("Number of Days", min_value=30, max_value=365, step=30, value=252)

if st.button("Run Simulation"):
    simulated_prices = montecarlosim(ticker, days, simulations)
    
    fig, ax = plt.subplots()
    ax.plot(simulated_prices, alpha=0.1, color="blue")
    ax.set_title(f"Monte Carlo Simulation for {ticker}")
    ax.set_xlabel("Days")
    ax.set_ylabel("Stock Price")
    st.pyplot(fig)

    st.line_chart(simulated_prices)

