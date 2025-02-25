from agent import Agent
import sys

def main():
    """
    Run the cryptocurrency price agent in the terminal.
    """
    try:
        agent = Agent()  # Initialize the agent, loading API key from .env
        print("Welcome! Ask me the price of any cryptocurrency (e.g., 'price of Bitcoin').")
        print("Type 'exit' or 'quit' to stop.", flush=True)
        
        while True:
            user_input = input("You: ")
            print(f"Debug: Received input: '{user_input}'", flush=True)  # Debug line
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!", flush=True)
                break
            if not user_input.strip():  # Handle empty input
                print("Please enter a query.", flush=True)
                continue
            response = agent.process_input(user_input)
            print(f"Debug: Response received: '{response}'", flush=True)
            print()  # Newline for readability

    except ValueError as e:
        print(f"Error: {e}", flush=True)  # Missing API key
    except Exception as e:
        print(f"Unexpected error: {str(e)}", flush=True)
        sys.exit(1)

if __name__ == "__main__":
    main()