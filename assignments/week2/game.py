import time

#defining functions

#fix for this via AI by using the sys to print smoothly. because apparently pycharm has problems with printing stuff sometimes. Before this each char was a new line.
def slow_print(text,delay=0.08):
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


#game starts here

slow_print("WHERE IS YOUR MOM")
pause()

name= input("What's your name?").strip() or "Lil kid"
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
    else:
        slow_print("\nYou have social anxiety and just stand there holding a candle")
        slow_print("Hours pass. You smell like the candle now.")
        slow_print("You do not know when the candle ends and where you begin anymore")
        pause()
        slow_print("\n YOU ARE A CANDLE FOR ETERNITY NOW. YOU LOST")


else:
    slow_print("\nYou go to the food court. You remember your mom saying she was hungry")
    pause()
    slow_print("You look around... There she is!!! She's on her phone, very calm")
    slow_print("She didn't even notice you were gone.")
    slow_print("\n MOM FOUND! YOU WIN!")


print()
slow_print("Thanks for playing.")

