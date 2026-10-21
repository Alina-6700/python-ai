"""Task 1.8: Business Helper Bot (Module 1 Final).

A rule-based chatbot for City Care Clinic. It answers common questions
(timings, fees, location, appointments), hands complaints to a manager,
and counts the questions it cannot answer. For each of those it prints the
AI prompt we would send in Module 2. Stretch: asking for a human ends the
chat, and the summary counts complaints.
"""

BOT_NAME = "City Care Bot"
BUSINESS_NAME = "City Care Clinic"

message_count = 0
unanswered_count = 0
complaint_count = 0

print(f"{BOT_NAME}: Hi! Ask about timings, fees, location or appointments. Type 'bye' to exit.")

# Why ask the name once, before the loop: we only need it one time,
# and asking inside the loop would repeat the question on every message
name = input(f"{BOT_NAME}: What is your name? ").strip().title()

while True:
    # Why strip().lower(): "  TIMINGS " and "timings" must be treated the same
    message = input(f"{name}: ").strip().lower()

    # Why skip empty input: pressing Enter by mistake is not a real question,
    # so it should not be counted or sent to the fallback
    if message == "":
        print(f"{BOT_NAME}: Please type a question.")
        continue

    message_count += 1

    # Why the complaint rule is first: an unhappy customer must never get a
    # random keyword reply (e.g. "late" should not fall through to timings)
    if "complaint" in message or "is late" in message or "rude" in message \
            or "refund" in message or "not happy" in message or "wrong" in message:
        complaint_count += 1
        print(f"{BOT_NAME}: Sorry about that. The clinic manager will call you today.")

    # Stretch: a person asked for a human, so end the chat
    elif "human" in message or "agent" in message:
        print(f"{BOT_NAME}: Connecting you to a human...")
        break

    elif message == "bye":
        print(f"{BOT_NAME}: Take care, {name}!")
        break

    # Why == and startswith() for short words: "hi" in "which doctor" is True,
    # so using `in` would greet people who never said hello
    elif message == "hi" or message.startswith("hi ") \
            or message == "hello" or message.startswith("hello ") \
            or message.startswith("salam") or message.startswith("assalam"):
        print(f"{BOT_NAME}: Hello {name}! How can I help you?")

    elif "timing" in message or "open" in message or "hours" in message:
        print(f"{BOT_NAME}: We are open 10 am to 8 pm, Monday to Saturday.")

    elif "how much" in message or "price" in message or "cost" in message \
            or "fees" in message or "the fee" in message or "charges" in message:
        print(f"{BOT_NAME}: Consultation fee is 2,000 PKR.")

    elif "where" in message or "address" in message or "location" in message:
        print(f"{BOT_NAME}: We are at 12 Main Street, City Centre.")

    elif "appointment" in message or "book" in message:
        print(f"{BOT_NAME}: To book, call 0300-0000000 or tell me your preferred day.")

    else:
        # Why count and show the prompt: unanswered questions tell the owner what
        # to add next, and this is the exact prompt Module 2 will send to an AI
        unanswered_count += 1
        ai_prompt = (f"You are the friendly assistant of {BUSINESS_NAME}. "
                     f"Answer in 2 lines: {message}")
        print(f"{BOT_NAME}: I am not sure yet. In Module 2, an AI will answer: {ai_prompt}")

print("=" * 40)
print(f"Chat summary: {message_count} messages, {unanswered_count} unanswered.")
print(f"Complaints received: {complaint_count}")