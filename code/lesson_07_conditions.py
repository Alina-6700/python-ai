"""Task 1.7: Smart Model Router.

Routes a request to the right AI model: private data to a local model,
code questions to a strong cloud model, and everything else to a cheap one.
Also estimates the cost and warns about very long requests.
Stretch: free users get a message when they send long requests.
"""

# Why strip().lower(): " Code " and "CODE" should both be treated as "code"
task_type = input("Task (code / private / chat): ").strip().lower()

# Why int(): input() returns text, and we need a number for the maths
estimated_tokens = int(input("Estimated tokens: "))

# Pick the model and an example price per 1K tokens in PKR (not real quotes)
if task_type == "code":
    chosen_model = "claude (cloud, strong at code)"
    price_per_1k_tokens_pkr = 0.8
elif task_type == "private":
    chosen_model = "llama3.2 (local, Ollama)"
    # Why 0: a local model runs on our own machine, so private data never
    # leaves it and there is no per-token charge
    price_per_1k_tokens_pkr = 0
else:
    # Why else: anything that is not code or private (including typos)
    # safely falls back to the cheapest option
    chosen_model = "small-cloud-model (cloud, cheap)"
    price_per_1k_tokens_pkr = 0.2

estimated_cost_pkr = estimated_tokens / 1000 * price_per_1k_tokens_pkr

if estimated_tokens > 4000:
    print("Warning: long request, consider shortening it.")
else:
    print("Length is fine.")

# Stretch: free users cannot send long requests
is_paid_user = input("Is this a paid user? (yes/no): ").strip().lower() == "yes"
if not is_paid_user and estimated_tokens > 2000:
    print("Upgrade to send long requests.")

print(f"Chosen model: {chosen_model}")
print(f"Estimated cost: {estimated_cost_pkr:.2f} PKR")