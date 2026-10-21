"""Task 1.5: AI Model Profile Card.

Prints a one-screen profile for an AI model (using str, int, float and bool),
asks how many tokens a chat uses, and estimates the cost per chat in PKR.
Stretch: also estimates the monthly cost from chats per day.
"""

# --- Model profile (one variable per data type) ---
model_name = "llama3.2"            # str: the model's name
context_window_tokens = 128000     # int: whole tokens, never fractional
price_per_1k_tokens_pkr = 0.5      # float: example price only, not a real quote
runs_locally = True                # bool: yes/no fact about the model

# Each value is printed with an f-string, plus its type() so we can see the type
print("--- AI Model Profile Card ---")
print(f"Model: {model_name} {type(model_name)}")
print(f"Context window: {context_window_tokens} tokens {type(context_window_tokens)}")
print(f"Price per 1K tokens: {price_per_1k_tokens_pkr} PKR {type(price_per_1k_tokens_pkr)}")
print(f"Runs locally: {runs_locally} {type(runs_locally)}")

# Why int(): input() always returns a str, and we can't do maths on text
tokens_per_chat = int(input("Tokens per chat: "))

# Why divide by 1000: the price is quoted per 1K tokens, not per single token
estimated_cost_pkr = round(tokens_per_chat / 1000 * price_per_1k_tokens_pkr, 2)

print(f"Tokens per chat: {tokens_per_chat}")
print(f"Estimated cost: {estimated_cost_pkr} PKR")

# --- Stretch: monthly cost ---
chats_per_day = int(input("Chats per day: "))
days_per_month = 30  # fixed at 30 so the estimate is simple and easy to explain
monthly_cost_pkr = round(estimated_cost_pkr * chats_per_day * days_per_month, 2)
print(f"Estimated monthly cost: {monthly_cost_pkr} PKR")