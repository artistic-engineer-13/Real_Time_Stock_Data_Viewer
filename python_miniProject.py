# app.py
import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Page config
st.set_page_config(
    page_title="Real-Time Stock Viewer",
    page_icon="📈",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Title
st.title("📈 Real-Time Stock Data Viewer")
st.markdown("Fetch and visualize stock data in real-time using `yfinance` and `matplotlib`.")

# Sidebar
st.sidebar.header("Select Stock & Timeframe")
stock_symbol = st.sidebar.text_input("Stock Symbol (e.g., WIPRO.NS, AAPL, TSLA):", "WIPRO.NS").upper()

# Date selection
end_date = datetime.today()
start_date = st.sidebar.date_input("Start Date:", end_date - timedelta(days=30))
end_date = st.sidebar.date_input("End Date:", end_date)

try:
    # Fetch historical data
    data = yf.download(stock_symbol, start=start_date, end=end_date)
    
    # Fetch real-time price
    stock = yf.Ticker(stock_symbol)
    current_price = stock.info.get('currentPrice')  # latest price
    
    if data.empty:
        st.warning("No data found for this stock symbol. Please try another symbol.")
    else:
        st.success(f"Data fetched successfully for {stock_symbol}!")
        
        # Show real-time price
        st.subheader(f"💰 Current Price of {stock_symbol}: {current_price} INR")

        # Show raw data
        if st.checkbox("Show Raw Data"):
            st.subheader("Raw Data")
            st.dataframe(data)

        # Plotting the closing price
        st.subheader(f"{stock_symbol} Closing Price Chart")
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(data['Close'], color='blue', marker='o', linestyle='-', linewidth=2, markersize=4)
        ax.set_title(f"{stock_symbol} Closing Price", fontsize=16)
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Price (USD)", fontsize=12)
        ax.grid(True)
        plt.xticks(rotation=45)
        st.pyplot(fig)

except Exception as e:
    st.error(f"Error fetching data: {e}")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit, Matplotlib, and yfinance")
