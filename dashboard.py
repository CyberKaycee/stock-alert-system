import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Stock Alert Dashboard", layout="centered")
st.title("Stock Alert Dashboard")

# User input
symbol = st.text_input("Enter Stock Symbol (e.g. AAPL, HONYFLOUR.LG)")
buy_limit = st.number_input("Set Buy Limit", min_value=0.0, step=0.1)
sell_limit = st.number_input("Set Sell Limit", min_value=0.0, step=0.1)

# Time range for chart
period = st.selectbox("Select Data Period", ["1d", "5d", "1mo", "3mo", "6mo", "1y"])
interval = st.selectbox("Select Interval", ["1m", "5m", "15m", "1h", "1d"])

if st.button("Check Stock Price"):
    if symbol:
        stock = yf.Ticker(symbol)

        try:
            data = stock.history(period=period, interval=interval)

            if not data.empty:
                current_price = data["Close"].iloc[-1]
                st.subheader(f"Current Price of {symbol}: ₦{current_price:.2f}")

                # Show alert based on price thresholds
                if current_price < buy_limit:
                    st.warning("🔽 Price is below your Buy Limit. Consider buying.")
                elif current_price > sell_limit:
                    st.success("🔼 Price is above your Sell Limit. You might want to sell.")
                else:
                    st.info("ℹ️ Price is within your set range.")

                # Show chart
                st.line_chart(data["Close"], use_container_width=True)

            else:
                st.error("❌ Could not fetch stock data. Please check the symbol and try again.")

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.error("Please enter a stock symbol.")
