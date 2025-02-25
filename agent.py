import requests
import os
import re
from dotenv import load_dotenv
from crypto_tool import get_cryptocurrency_price
from prompt_template import system_prompt, get_symbol_prompt

load_dotenv()

TOGETHER_AI_API_KEY = os.getenv("TOGETHER_AI_API_KEY")

def get_symbol_from_llm(crypto_name):
    """
    Uses the LLM to get the cryptocurrency symbol from the name.
    """
    prompt = get_symbol_prompt.format(crypto_name=crypto_name)

    response = requests.post(
        "https://api.together.xyz/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {TOGETHER_AI_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",  
            "messages": [{"role": "user", "content": prompt}],
        },
    )

    if response.status_code == 200:
        data = response.json()
        llm_response = data["choices"][0]["message"]["content"].strip()
        match = re.search(r"[A-Z]{2,5}", llm_response)
        if match:
            return match.group(0)
    print(f"Error extracting symbol: {llm_response}")
    return None

def handle_user_query(user_query):
    """
    Handles user queries, providing cryptocurrency prices if requested.
    """
    if "price of" in user_query.lower():
        crypto_name = user_query.lower().split("price of ")[-1].split(" ")[0]

        symbol = get_symbol_from_llm(crypto_name)
        if symbol:
            price = get_cryptocurrency_price(symbol=symbol)
            if price:
                return f"Price of {crypto_name.capitalize()} is {float(price):.2f} USD"
            else:
                return "Could not retrieve cryptocurrency price."
        else:
            return "Could not determine the symbol for the cryptocurrency."

    return "I can only provide cryptocurrency prices. Please ask me about a cryptocurrency price."

def react_agent(user_input):
    """
    Processes user input and returns a response.
    """
    return {"response": handle_user_query(user_input)}