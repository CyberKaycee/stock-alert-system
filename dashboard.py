import streamlit as st
import requests

# Twelve Data API
TD_API_KEY = "e41030e68a16406988ca91f9d1b7bbce"

def get_stock_price(symbol):
    url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={TD_API_KEY}"
    response = requests.get(url)
    data = response.json()
    if "price" in data:
        return float(data["price"])
    else:
        st.error("Error fetching stock price.")
        st.json(data)
        return None

st.set_page_config(page_title="Stock Alert Dashboard", layout="centered")
st.title("Stock Alert Dashboard")

# User input
symbol = st.text_input("Enter Stock Symbol (e.g. AAPL, MSFT)")
buy_limit = st.number_input("Set Buy Limit", min_value=0.0, step=0.1)
sell_limit = st.number_input("Set Sell Limit", min_value=0.0, step=0.1)

# Currencies
default_currency = "USD"

# Currency symbols
currency_symbol = {
    "NGN": "₦", "USD": "$", "EUR": "€",
    "GBP": "£", "JPY": "¥", "CAD": "C$"
}.get(display_currency, "")

# Button to fetch and show stock price
if st.button("Check Stock Price"):
    if symbol:
        price_usd = get_stock_price(symbol)
        if price_usd:
            converted_price = convert_currency(price_usd, "USD", display_currency)

            st.subheader(f"Current Price of {symbol.upper()}: {currency_symbol}{converted_price:.2f} {display_currency}")

            if converted_price < buy_limit:
                st.warning("🔽 Price is below your Buy Limit. Consider buying.")
            elif converted_price > sell_limit:
                st.success("🔼 Price is above your Sell Limit. You might want to sell.")
            else:
                st.info("ℹ️ Price is within your set range.")
    else:
        st.error("Please enter a stock symbol.")
