import streamlit as st
import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Basic configuration and title
st.set_page_config(page_title='Friend Tech Rewards Tracker')
st.title('Friend Tech Rewards Tracker')
logging.info("Page configured and title set.")

# Input fields
current_friend = st.number_input('Current Friend Tokens', min_value=0.0, value=0.0, step=0.01)
current_eth = st.number_input('Current ETH Tokens', min_value=0.0, value=0.0, step=0.01)
initial_investment_friend = st.number_input('Initial Investment in Friend Tokens', min_value=0.0, value=0.0, step=0.01)
initial_investment_eth = st.number_input('Initial Investment in ETH Tokens', min_value=0.0, value=0.0, step=0.01)
stake_date = st.date_input('Est. Time You First Staked')
current_rewards = st.number_input('Current $Friend Rewards', min_value=0.0, value=0.0, step=0.01)
logging.info("Input fields initialized.")

# API URL
api_url = "https://api.dexscreener.com/latest/dex/pairs/base/0x7CfC830448484CDF830625373820241E61ef4acf"

# Fetch data from API
response = requests.get(api_url)
if response.status_code == 200:
    data = response.json()
    if data and 'pairs' in data and data['pairs']:
        pair_data = data['pairs'][0]
        friend_price = float(pair_data.get('priceUsd', 0))
        volume = pair_data.get('volume', {}).get('h24', 0)
        logging.info("Data successfully fetched and parsed from API.")
    else:
        st.error("No data available for the specified pair.")
        logging.error("No data available for the specified pair.")
else:
    st.error(f"Failed to fetch data from the API. Status code: {response.status_code}")
    logging.error(f"Failed to fetch data from the API. Status code: {response.status_code}")

# Calculations
hours_since_stake = (datetime.now() - datetime.combine(stake_date, datetime.min.time())).total_seconds() / 3600
friend_rewards_rate = current_rewards / hours_since_stake if hours_since_stake > 0 else 0
apy = (friend_rewards_rate * 24 * 365) / (initial_investment_friend + initial_investment_eth) * 100 if (initial_investment_friend + initial_investment_eth) > 0 else 0
logging.info("Calculations for APY and rewards rate completed.")

# Plotting
fig, ax = plt.subplots()
ax.plot([i for i in range(30)], [current_rewards * i for i in range(30)])  # Adjusted dummy data
st.pyplot(fig)
logging.info("Plot generated and displayed.")

# Display results
st.write(f"APY: {apy:.2f}%")
st.write(f"$Friend Rewards Rate: {friend_rewards_rate:.2f} FRIEND/Hour")
logging.info("Results displayed to user.")