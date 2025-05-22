def get_price(stock_symbol):
    try:
        stock = yf.Ticker(stock_symbol)
        data = stock.history(period="1d")
        if not data.empty:
            return round(data['Close'].iloc[-1], 2)
        else:
            return None
    except:
        return None

st.title("📈 Stock Alert Dashboard")

# User input
stock_symbol = st.text_input("Enter stock symbol (e.g. HONYFLOUR.LG for Honeywell):", "HONYFLOUR.LG")
buy_limit = st.number_input("Set Buy Limit (₦)", value=7.0)
sell_limit = st.number_input("Set Sell Limit (₦)", value=10.0)

if st.button("Check Stock Price"):
    price = get_price(stock_symbol)
    if price:
        st.write(f"Current price of **{stock_symbol}** is **₦{price}**")

        if price <= buy_limit:
            st.success("📉 Buy Alert: Price is below buy limit!")
        elif price >= sell_limit:
            st.warning("📈 Sell Alert: Price is above sell limit!")
        else:
            st.info("💤 Price is within normal range.")
    else:
        st.error("⚠️ Failed to fetch stock price.")
