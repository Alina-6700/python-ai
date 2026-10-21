"""Module 1 Project: AI Front Desk for Sweet Crumbs bakery.

Answers common questions with rules (free), gives exact price quotes with a
bulk discount and a delivery fee, and prepares an AI-ready prompt for
everything else. Private questions go to a local model (cost 0), the rest to a
cheap cloud model with an estimated cost. Ends with a session report.
Bonus: safe quantity check and human handover.
"""

# Constants in UPPER_CASE: they never change while the program runs
BOT_NAME = "Sweet Crumbs Desk"
BUSINESS_NAME = "Sweet Crumbs bakery"
CUPCAKE_PRICE = 250
BROWNIE_PRICE = 300
CHOCOLATE_CAKE_PRICE = 1500
BULK_MIN_QUANTITY = 10
BULK_DISCOUNT = 0.10
DELIVERY_FEE = 200
FREE_DELIVERY_LIMIT = 3000
CLOUD_PRICE_PER_1K_TOKENS = 0.1  # example price in PKR, not a real quote

# Counters for the session report
message_count = 0
answered_by_rules = 0
unanswered_count = 0
quote_count = 0
quoted_value = 0
complaint_count = 0
total_ai_cost = 0

print("=" * 50)
print(f"   {BOT_NAME}: rules, quotes and AI-ready prompts")
print("=" * 50)
print("Ask anything, type /quote for a price, or bye to exit.")

# Why ask once, before the loop: the name never changes, and asking inside
# the loop would repeat the question on every message
customer_name = input(f"{BOT_NAME}: What is your name? ").strip().title()

while True:
    # Why strip().lower(): "  HOURS " and "hours" must be treated the same
    message = input(f"{customer_name}: ").strip().lower()

    # Why skip empty input: pressing Enter is not a question, so it is not
    # counted and nothing is sent to the AI
    if message == "":
        print(f"{BOT_NAME}: Please type a question.")
        continue

    message_count += 1

    # Why the complaint rule is first: an unhappy customer must always reach a
    # human. Keywords are "is late", not "late", because "late" hides inside
    # "chocolate" and would wrongly flag a cake question as a complaint
    if "complaint" in message or "refund" in message or "is late" in message \
            or "was late" in message or "not delivered" in message or "rude" in message:
        complaint_count += 1
        answered_by_rules += 1
        print(f"{BOT_NAME}: Sorry about that. A manager will call you within 1 hour.")

    # Bonus: human handover ends the chat
    elif "human" in message or "agent" in message:
        print(f"{BOT_NAME}: Connecting you to a human...")
        break

    elif message == "bye":
        print(f"{BOT_NAME}: Goodbye, {customer_name}!")
        break

    elif message == "/quote":
        item = input(f"{BOT_NAME}: Which item? ").strip().lower()
        quantity_text = input(f"{BOT_NAME}: How many? ").strip()

        # Price per item; 0 means the item is not on the menu
        if item == "cupcake":
            unit_price = CUPCAKE_PRICE
        elif item == "brownie":
            unit_price = BROWNIE_PRICE
        elif item == "chocolate cake":
            unit_price = CHOCOLATE_CAKE_PRICE
        else:
            unit_price = 0

        if unit_price == 0:
            print(f"{BOT_NAME}: Sorry, {item} is not on our menu.")
        # Why isdigit() before int(): letters would crash int() with ValueError.
        # "or" stops early, so int() only runs when the text is all digits
        elif not quantity_text.isdigit() or int(quantity_text) == 0:
            print(f"{BOT_NAME}: Please type the quantity as a whole number, like 12.")
        else:
            quantity = int(quantity_text)
            subtotal = unit_price * quantity

            if quantity >= BULK_MIN_QUANTITY:
                discount = round(subtotal * BULK_DISCOUNT)
            else:
                discount = 0

            # Why delivery is checked AFTER the discount: the customer pays the
            # discounted amount, so that is what must reach the free-delivery limit
            after_discount = subtotal - discount
            if after_discount >= FREE_DELIVERY_LIMIT:
                delivery = 0
            else:
                delivery = DELIVERY_FEE

            total = after_discount + delivery

            quote_count += 1
            quoted_value += total
            answered_by_rules += 1
            print(f"{BOT_NAME}: {quantity} x {item} = {subtotal:,} PKR")
            print(f"     Discount: -{discount:,} PKR | Delivery: {delivery:,} PKR")
            print(f"     Total: {total:,} PKR")

    # Why == and startswith() for greetings: "hi" in "which cake" is True,
    # so using `in` would greet people who never said hello
    elif message == "hi" or message.startswith("hi ") \
            or message == "hello" or message.startswith("hello ") \
            or message.startswith("salam") or message.startswith("assalam"):
        answered_by_rules += 1
        print(f"{BOT_NAME}: Hello {customer_name}! How can I help you?")

    elif "hours" in message or "timing" in message or "open" in message:
        answered_by_rules += 1
        print(f"{BOT_NAME}: We are open 9 am to 10 pm, every day.")

    elif "where are you" in message or "location" in message or "located" in message:
        answered_by_rules += 1
        print(f"{BOT_NAME}: We are at 12 Main Street, City Centre.")

    # Delivery comes before prices so "how much is delivery" gets the delivery answer
    elif "deliver" in message:
        answered_by_rules += 1
        print(f"{BOT_NAME}: We deliver for {DELIVERY_FEE:,} PKR, free from {FREE_DELIVERY_LIMIT:,} PKR.")

    elif "menu" in message or "price" in message or "how much" in message:
        answered_by_rules += 1
        print(f"{BOT_NAME}: Cupcake {CUPCAKE_PRICE:,}, brownie {BROWNIE_PRICE:,}, "
              f"chocolate cake {CHOCOLATE_CAKE_PRICE:,} PKR. Type /quote for an exact price.")

    else:
        # Smart fallback: clean, cut to 150 characters, estimate tokens, route
        unanswered_count += 1
        question = message.capitalize()[:150]
        estimated_tokens = round(len(question) / 4)

        # Why route by private words: phone numbers, CNICs and addresses must
        # never leave the shop, so a local model (cost 0) handles them
        if "phone" in message or "cnic" in message or "my address" in message:
            chosen_model = "llama3.2 (local, private)"
            ai_cost = 0
        else:
            chosen_model = "small cloud model (cheap)"
            ai_cost = estimated_tokens / 1000 * CLOUD_PRICE_PER_1K_TOKENS

        total_ai_cost += ai_cost

        print(f"{BOT_NAME}: Good question! Routed to: {chosen_model} (~{estimated_tokens} tokens)")
        print(f"""     Prompt: You are the assistant of {BUSINESS_NAME}.
     Answer {customer_name} in 2 short lines. Question: {question}""")

print("=" * 50)
print("Session report")
print(f"Messages: {message_count} | Answered by rules: {answered_by_rules} | Unanswered: {unanswered_count}")
print(f"Quotes: {quote_count} | Quoted value: {quoted_value:,} PKR")
print(f"Estimated AI cost for unanswered questions: {total_ai_cost:.4f} PKR")
print(f"Complaints received: {complaint_count}")
print("=" * 50)