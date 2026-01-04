import random

def choose_difficulty():
    while True:
        level = input("Choose difficulty (easy / medium / hard): ").lower()

        if level == "easy":
            return random.randint(1, 10), 5
        elif level == "medium":
            return random.randint(1, 20), 4
        elif level == "hard":
            return random.randint(1, 50), 3
        else:
            print("❌ Invalid choice. Try again.")

def play_round(game_state):
    secret_number, attempts = choose_difficulty()

    game_state["secret_number"] = secret_number
    game_state["attempts_left"] = attempts
    game_state["status"] = "playing"

    print("\n🎯 New Round Started!")
    print("I have chosen a number. Try to guess it!")

    while game_state["attempts_left"] > 0:
        guess = input("Enter your guess: ")

        if not guess.isdigit():
            print("⚠️ Please enter a valid number.")
            continue
        
        guess = int(guess)

        if guess == game_state["secret_number"]:
            print("🎉 Correct! You guessed the number.")
            game_state["status"] = "won"
            return
        elif guess < game_state["secret_number"]:
            print("⬆️ Too low.")
        else:
            print("⬇️ Too high.")

        game_state["attempts_left"] -= 1
        print(f"Attempts left: {game_state['attempts_left']}")
    
    print(f"💀 You lost. The number was {game_state['secret_number']}")
    game_state["status"] = "lost"


def update_scoreboard(game_state):
    pass

def guess_number():
    game_state = {
        "secret_number" : None,
        "attempts_left" : 0,
        "status": "playing"
    }

    while True:
        play_round(game_state)
        update_scoreboard(game_state)

        again = input("Play again? (y/n): ").lower()
        if again != "y":
            break

guess_number()