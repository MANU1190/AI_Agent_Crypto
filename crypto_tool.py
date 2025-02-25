# crypto_tool.py
import requests
import os
from dotenv import load_dotenv

load_dotenv()

COINMARKETCAP_API_KEY = os.getenv("COINMARKETCAP_API_KEY")

def get_cryptocurrency_price(symbol="BTC", currency="USD"):
    """
    Fetches the price of a cryptocurrency from the CoinMarketCap API.

    Args:
        symbol (str): The cryptocurrency symbol (e.g., "BTC", "ETH"). Defaults to "BTC".
        currency (str): The currency to display the price in (e.g., "USD", "EUR"). Defaults to "USD".

    Returns:
        float: The price of the cryptocurrency, or None if an error occurs.
    """
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    headers = {
        "X-CMC_PRO_API_KEY": COINMARKETCAP_API_KEY,
        "Accept": "application/json"
    }
    parameters = {
        "symbol": symbol,
        "convert": currency
    }

    try:
        response = requests.get(url, headers=headers, params=parameters, timeout=10)
        response.raise_for_status()
        data = response.json()

        price = data['data'][symbol]['quote'][currency]['price']

        return price

    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return None
    except (KeyError, TypeError) as e:
        print(f"Error parsing API response: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

if __name__ == '__main__':
    btc_price = get_cryptocurrency_price(symbol="BTC", currency="USD")
    if btc_price:
        print(f"The current Bitcoin price is: ${btc_price:.2f}")
    else:
        print("Could not retrieve Bitcoin price.")

    eth_price = get_cryptocurrency_price(symbol="ETH", currency="EUR")
    if eth_price:
        print(f"The current Ethereum price in EUR is: {eth_price:.2f}")
    else:
        print("Could not retrieve Ethereum price.")