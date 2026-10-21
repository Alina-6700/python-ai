"""Task 1.6: Prompt Cleaner.

Cleans a customer's messy name and question, measures the question,
checks whether it mentions Python, and builds a safe multi-line prompt
for an AI model. Stretch: masks a bad word and estimates the prompt cost.
"""

user_name = input("Your name: ")
user_question = input("Your question: ")

# Why strip(): customers paste extra spaces that waste tokens and look messy
# Why title() for names but capitalize() for questions: a name has a capital
# on every word, while a question only needs one at the start
clean_name = user_name.strip().title()
clean_question = user_question.strip().capitalize()

# Stretch: mask a bad word before it ever reaches the AI
# (capitalize() already lowercased the text, so a lowercase match works)
safe_question = clean_question.replace("stupid", "***")

# Why divide by 4: a rough rule of thumb is that 1 token is about 4 characters
char_count = len(clean_question)
estimated_tokens = round(char_count / 4)

# Why lower(): "Python", "PYTHON" and "python" should all count as a match
mentions_python = "python" in clean_question.lower()

print("=" * 40)
print(f"Cleaned question: {clean_question}")
print(f"Characters: {char_count}, about {estimated_tokens} tokens")
print(f"Mentions Python: {mentions_python}")
print("=" * 40)

# Why [:150]: a very long question would cost too much and could swamp the prompt
prompt = f"""You are a friendly Python tutor.
Greet {clean_name} by name and answer in 3 short lines.
Question: {safe_question[:150]}"""

print(prompt)

# Stretch: estimated cost of the whole prompt (example price, not a real quote)
price_per_1k_tokens_pkr = 0.5
prompt_tokens = round(len(prompt) / 4)
prompt_cost_pkr = prompt_tokens / 1000 * price_per_1k_tokens_pkr
print(f"Estimated prompt cost: {prompt_cost_pkr:.2f} PKR")