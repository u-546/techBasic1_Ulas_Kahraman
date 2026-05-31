#### I've thought of keeping track of the time player takes until finishing the game, like a speedrun. It will also record the type of endings they've got.
#### PyCharm itself is quite smart with errors and anything syntax related especially, but Claude really helped out with the logic behind the save system.

import time
import os
from datetime import datetime

DEBUG = True

RECORDS_FILE = "mom_speedrun.txt"

def slow_print(text, delay=0.08):
    import sys
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write('\n')
    sys.stdout.flush()

def pause(seconds=1):
    time.sleep(seconds)

def get_number_in_range(prompt, min_val, max_val):
    while True:
        try:
            number = int(input(prompt))
            if min_val <= number <= max_val:
                return number
            else:
                print("Please enter a number between {} and {}".format(min_val, max_val))
        except ValueError:
            print("(That's not a number dude")

"""LEADER BOARD NEW CODE STARTING HERE >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"""
# speedrun record helpers, it will record the time until one finishes the game. Also will record the type of ending they achieve. IT'll also look pretty on the terminal. Not as much in txt file haha.

def load_records():
    records = []
    try:
        with open(RECORDS_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    name, seconds, outcome, timestamp = line.split("|")
                    records.append({
                        "name": name,
                        "seconds": float(seconds),
                        "outcome": outcome,
                        "timestamp": timestamp
                    })
                except ValueError:
                    print(f"[Skipping bad record line: {line}]")
        print(f"[Leaderboard loaded from '{RECORDS_FILE}']")
    except FileNotFoundError:
        print(f"[No leaderboard file found,..a new one will be created.]")
    except OSError as e:
        print(f"[Error reading leaderboard file: {e}]")
    return records


def save_records(records):
    try:
        with open(RECORDS_FILE, "w") as f:
            for r in records:
                f.write(f"{r['name']}|{r['seconds']:.2f}|{r['outcome']}|{r['timestamp']}\n")
        print(f"[Leaderboard saved to '{RECORDS_FILE}']")
    except OSError as e:
        print(f"[Error saving leaderboard: {e}]")


def add_record(records, name, seconds, outcome):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = {
        "name": name,
        "seconds": seconds,
        "outcome": outcome,
        "timestamp": timestamp
    }
    records.append(entry)
    records.sort(key=lambda r: (0 if "WIN" in r["outcome"] else 1, r["seconds"]))
    return records


def format_time(seconds):
    mins = int(seconds // 60)
    secs = seconds % 60
    if mins > 0:
        return f"{mins}m {secs:.2f}s"
    return f"{secs:.2f}s"

#draw a little "board"
def display_leaderboard(records, highlight_name=None):
    print("\n" + "=" * 60)
    print("           WHERE IS YOUR MOM — SPEEDRUN BOARD   ")
    print("=" * 60)
    if not records:
        print("  No runs yet. You're the first!")
    else:
        print(f"  {'#':<4} {'Name':<16} {'Time':<12} {'Outcome':<20} {'Date'}")
        print("  " + "-" * 56)
        for i, r in enumerate(records[:10], start=1):
            marker = " < YOU" if r["name"] == highlight_name else ""
            print(f"  {i:<4} {r['name']:<16} {format_time(r['seconds']):<12} {r['outcome']:<20} {r['timestamp']}{marker}")
    print("=" * 60 + "\n")


# game start, now defining outcomes for the final scoreboard.

slow_print("WHERE IS YOUR MOM")
pause()
name= input("What's your name?").strip() or "Lil kid"

if DEBUG:
    print(f"\n[DEBUG MODE] Skipping game. Using placeholder values.")
    elapsed = 99.00
    outcome = "DEBUG - test run"
else:
    slow_print(f"\nOkay {name}. You're in the mall right now. And you have lost your mom.")
    pause()
    #range check
    print("\nHowm many minutes ago did you last see your mom?")
    mins = get_number_in_range("Enter a number (1 to 10): ", 1, 10)
    slow_print(f"\n{mins} minutes?? {name}, she's long gone dude. Anyway we'll find her")
    pause()
    print("\nWhere do you look first?")
    print(" 1 = Scented candle store")
    print(" 2 = Food court")

    # Timer starts here, right before the real choices
    run_start = time.time()

    choice = input("Pick 1 or 2: ").strip()
    if choice == "1":
        slow_print("\nYou head to the scented candle store. It smells like your grandma's house.")
        pause()
        slow_print("You see someone with similar hair with your mom. You tap her shoudler")
        pause()
        #nest nest
        tap = input("You wanna say 'mom?' out loud. Do you? yes/no: ").strip().lower()
        if tap == "yes":
            slow_print("\nShe turns around. Not your mom. You are embarrased. Start excessively crying on the floor.")
            pause()
            slow_print("But then a voice behind you shouts! It's your mom!! She hear you crying.")
            slow_print("\nMOM FOUND YOU. YOU WIN.")
            outcome = "WIN - dramatic rescue"
        else:
            slow_print("\nYou have social anxiety and just stand there holding a candle")
            slow_print("Hours pass. You smell like the candle now.")
            slow_print("You do not know when the candle ends and where you begin anymore")
            pause()
            slow_print("\n YOU ARE A CANDLE FOR ETERNITY NOW. YOU LOST")
            outcome = "LOSE - became a candle"
    else:
        slow_print("\nYou go to the food court. You remember your mom saying she was hungry")
        pause()
        slow_print("You look around... There she is!!! She's on her phone, very calm")
        slow_print("She didn't even notice you were gone.")
        slow_print("\n MOM FOUND! YOU WIN!")
        outcome = "WIN - food court"

    elapsed = time.time() - run_start

print()
slow_print("Thanks for playing.")
slow_print(f"Your time: {format_time(elapsed)}")

# save and display the board
records = load_records()
records = add_record(records, name, elapsed, outcome)
save_records(records)
display_leaderboard(records, highlight_name=name)
