import streamlit as st
import yfinance as yf
import pandas as pd
import requests

API_KEY = "baa7c13ccae94658f5ff68a9aa7f633b"  #

def convert_currency(amount, from_currency, to_currency):
    if from_currency == to_currency:
        return amount
    try:
        url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{from_currency}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data["result"] == "success":
            rates = data["conversion_rates"]
            if to_currency in rates:
                rate = rates[to_currency]
                return round(amount * rate, 2)
            else:
                st.error(f"❌ Currency {to_currency} not found in rates.")
                return amount
        else:
            st.error("Currency API returned an error.")
            st.json(data)
            return amount

    except Exception as e:
        st.error(f"Currency conversion failed: {e}")
        return amount
        rate = data['result']
        return round(amount * rate, 2)

    except Exception as e:
        st.error(f"Currency conversion failed: {e}")
        return amount


st.set_page_config(page_title="Stock Alert Dashboard", layout="centered")
st.title("Stock Alert Dashboard")

# User input
symbol = st.text_input("Enter Stock Symbol (e.g. AAPL, HONYFLOUR.LG)")
buy_limit = st.number_input("Set Buy Limit", min_value=0.0, step=0.1)
sell_limit = st.number_input("Set Sell Limit", min_value=0.0, step=0.1)

# Time range for chart
period = st.selectbox("Select Data Period", ["1d", "5d", "1mo", "3mo", "6mo", "1y"])
interval = st.selectbox("Select Interval", ["1m", "5m", "15m", "1h", "1d"])

# Default and selectable currencies
default_currency = "NGN"
currencies = ["NGN", "USD", "EUR", "GBP", "CAD", "JPY"]
display_currency = st.selectbox("Select Display Currency", currencies, index=currencies.index(default_currency))

# Currency conversion function
def convert_currency(amount, from_currency, to_currency):
    try:
        if from_currency == to_currency:
            return amount
        rate = c.get_rate(from_currency, to_currency)
        return round(amount * rate, 2)
    except:
        st.error("Currency conversion failed. Please check your internet connection or try again later.")
        return amount

# ✅ Only one button block!
if st.button("Check Stock Price"):
    if symbol:
        stock = yf.Ticker(symbol)

        try:
            data = stock.history(period=period, interval=interval)

            if not data.empty:
                current_price_usd = data["Close"].iloc[-1]
                converted_price = convert_currency(current_price_usd, "USD", display_currency)
                currency_symbol = {
                    "NGN": "₦", "USD": "$", "EUR": "€",
                    "GBP": "£", "JPY": "¥", "CAD": "C$"
                }.get(display_currency, "")

                st.subheader(f"Current Price of {symbol}: {currency_symbol}{converted_price:.2f} {display_currency}")

                if converted_price < buy_limit:
                    st.warning("🔽 Price is below your Buy Limit. Consider buying.")
                elif converted_price > sell_limit:
                    st.success("🔼 Price is above your Sell Limit. You might want to sell.")
                else:
                    st.info("ℹ️ Price is within your set range.")

                st.line_chart(data["Close"], use_container_width=True)

            else:
                st.error("❌ Could not fetch stock data. Please check the symbol and try again.")

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error("Please enter a stock symbol.")
