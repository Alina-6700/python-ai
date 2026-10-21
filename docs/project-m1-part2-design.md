# Module 1 Project: AI Front Desk (Sweet Crumbs bakery)

File: `code/project_m1_front_desk.py`

## Intents

Rules are checked from top to bottom, and the first match wins.

| Order | Intent | Keywords | Reply |
|---|---|---|---|
| 1 | Complaint | complaint, refund, is late, was late, not delivered, rude | Sorry about that. A manager will call you within 1 hour. |
| 2 | Human handover (bonus) | human, agent | Connecting you to a human... (chat ends) |
| 3 | Exit | bye (exact match) | Goodbye, {name}! (chat ends, report printed) |
| 4 | Quote | /quote (exact match) | Asks for item and quantity, prints the price breakdown |
| 5 | Greeting | hi, hello, salam, assalam (start of message only) | Hello {name}! How can I help you? |
| 6 | Hours | hours, timing, open | We are open 9 am to 10 pm, every day. |
| 7 | Location | where are you, location, located | We are at 12 Main Street, City Centre. |
| 8 | Delivery | deliver | We deliver for 200 PKR, free from 3,000 PKR. |
| 9 | Menu and prices | menu, price, how much | Cupcake 250, brownie 300, chocolate cake 1,500 PKR. Type /quote for an exact price. |
| 10 | Fallback | (no match) | Counted as unanswered, routed to a model, AI prompt printed |

Why this order:
- Complaint is first so an unhappy customer always reaches a human.
- "late" is not a keyword on its own because it hides inside "chocolate". The bot uses "is late" instead.
- Delivery is before prices so "how much is delivery" gets the delivery answer.
- Greetings use `==` and `.startswith()` because "hi" hides inside "which".

## Business rules

| Rule | Value |
|---|---|
| Item prices | cupcake 250 PKR, brownie 300 PKR, chocolate cake 1,500 PKR |
| Bulk discount | 10% off for 10 or more items |
| Delivery | 200 PKR, free when the discounted amount is 3,000 PKR or more |
| Private words | phone, cnic, my address (routed to the local model, cost 0) |
| Cloud price (example) | 0.1 PKR per 1K tokens |
| Token estimate | characters / 4, rounded |

Rule order for quotes: subtotal, then discount, then the delivery check on the discounted amount, then total. Example: 12 cupcakes = 3,000 PKR, minus 300 discount = 2,700, which is below 3,000, so delivery of 200 PKR is still charged. Total 2,900 PKR.

How the report counts "answered by rules": FAQ replies, greetings, complaints and successful quotes. A failed quote (unknown item or bad quantity), an empty message and "bye" are not counted as answered or unanswered.

## Rule tests

Result column: my test run of the script. Re-run every row on your own copy before submitting.

| You type | Expected | Pass? |
|---|---|---|
| `  WHAT are your hours ` | Hours (capitals and spaces handled) | Yes |
| `which cake is best?` | Fallback, not a greeting | Yes |
| `do you have chocolate cake?` | Fallback, not a complaint ("late" hides in "chocolate") | Yes |
| `my order is late` | Manager reply (complaint rule first) | Yes |
| `/quote`, chocolate cake, 1 | Delivery fee charged (1,700 PKR total) | Yes |
| `/quote`, chocolate cake, 3 | Delivery free (4,500 PKR total) | Yes |
| `/quote`, brownie, 10 | Discount applied (-300 PKR, total 2,900 PKR) | Yes |
| `/quote`, sushi, 5 | "Not on our menu", no crash | Yes |
| `/quote`, brownie, `abc` | Polite quantity message, no crash (bonus) | Yes |
| `/quote`, cupcake, 0 | Polite quantity message | Yes |
| `I need to give my cnic` | Routed to the local model, cost 0 | Yes |
| (press Enter with no text) | Asks again, not counted | Yes |
| `BYE` | Goodbye + session report | Yes |