"""Little game about selling scented candles until you reach the goal.
an actually helpful video by Khan Academy on this was very nice: https://www.youtube.com/watch?v=TkRfRsmCquw
Claude was also used for debugging / overall polish.
"""

import random

inventory = []
MAX_ITEMS = 5

stockroom = [
    {"name": "lavender candle", "price": 6},
    {"name": "vanilla candle",  "price": 5},
    {"name": "rose candle",     "price": 7},
    {"name": "cinnamon candle", "price": 6},
]

customers = [
    {"name": "Emma",   "wants": "", "pays": 6,  "intro": "Emma walks in. She wants a [CANDLE]."},
    {"name": "Luca",   "wants": "", "pays": 5,  "intro": "Luca stops by. He wants a [CANDLE]."},
    {"name": "Sophie", "wants": "", "pays": 7,  "intro": "Sophie arrives. She wants a [CANDLE]."},
    {"name": "Mom",    "wants": "", "pays": 6,  "intro": "Your mom came in? She wants a [CANDLE]. You haven't seen her since childhood."},
]

# shuffle candle names and assign one to each customer
candle_names = [item["name"] for item in stockroom]
random.shuffle(candle_names)

for i in range(len(customers)):
    customers[i]["wants"] = candle_names[i]
    customers[i]["intro"] = customers[i]["intro"].replace("[CANDLE]", candle_names[i])

money = 0
goal = 24
current = 0


# see what you have in your hands
def show_inventory():
    if len(inventory) == 0:
        print("Your inventory is empty.")
    else:
        print("You are holding:")
        for item in inventory:
            print(" -", item["name"])


# see what you have in stock
def show_stockroom():
    if len(stockroom) == 0:
        print("The stockroom is empty.")
    else:
        print("Candles in the stockroom:")
        for item in stockroom:
            print(" -", item["name"])


# pickup candle
def pickup(name):
    if len(inventory) >= MAX_ITEMS:
        print("Your hands are full! Drop something first.")
        return
    found = None
    for item in stockroom:
        if item["name"].lower() == name.lower():
            found = item
    if found == None:
        print("That item is not in the stockroom.")
        return
    stockroom.remove(found)
    inventory.append(found)
    print("You picked up the " + found["name"] + ".")


# put back candle
def drop(name):
    found = None
    for item in inventory:
        if item["name"].lower() == name.lower():
            found = item
    if found == None:
        print("You are not holding that item.")
        return
    inventory.remove(found)
    stockroom.append(found)
    print("You put the " + found["name"] + " back.")


# sell candle
def sell(name):
    global money, current

    found = None
    for item in inventory:
        if item["name"].lower() == name.lower():
            found = item
    if found == None:
        print("You are not holding that item.")
        return

    c = customers[current]

    if found["name"].lower() == c["wants"].lower():
        money = money + c["pays"]
        inventory.remove(found)
        print(c["name"] + " loves it! You earned $" + str(cstoc["pays"]) + ". Total: $" + str(money) + "/$" + str(goal))
        current = current + 1
        if money >= goal:
            print("\nYou reached $24 -- you win! The shop is doing great!")
        elif current < len(customers):
            next_c = customers[current]
            print(next_c["intro"])
        else:
            print("No more customers today.")
    else:
        print(c["name"] + " shakes their head. They wanted a " + c["wants"] + ".")


# help menu
def show_help():
    print("Here's what you can do:")
    print("  stockroom      - see candles available to pick up")
    print("  inventory      - see what you are holding")
    print("  pickup <item>  - grab a candle from the stockroom")
    print("  drop <item>    - put a candle back")
    print("  sell <item>    - sell a candle to the current customer")
    print("  help           - show this list")
    print("  quit           - close the shop")


# game start
print("You arrive at your Scented Candle Shop. You've been a candle seller since forever.")
print("Earn $24 to win! (type help to show what you can do)")
print(customers[0]["intro"])
print("")

while True:
    user_input = input("> ").strip().lower()

    if user_input == "":
        continue

    parts = user_input.split(maxsplit=1)
    cmd = parts[0]

    if len(parts) > 1:
        arg = parts[1]
    else:
        arg = ""

    if cmd == "quit":
        print("You close the shop. Goodbye!")
        break
    elif cmd == "stockroom":
        show_stockroom()
    elif cmd == "inventory":
        show_inventory()
    elif cmd == "pickup":
        pickup(arg)
    elif cmd == "drop":
        drop(arg)
    elif cmd == "sell":
        sell(arg)
    elif cmd == "help":
        show_help()
    else:
        print("Unknown command. Type 'help' to see what you can do.")
