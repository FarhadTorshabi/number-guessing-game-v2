import random
import json
import os
from typing import Union

# --------------------------------------------------------
# Loading scoreboard file to scoreboard variable
# --------------------------------------------------------
def load_scoreboard(filename: str = "scoreboard.json") -> dict:
    """
    Load the scoreboard from a JSON file.
    If the file does not exist, return an empty dictionary.
    Args: filename (str): Path to scoreboard file.
    Returns: dict: Dictionary of player statistics.
    """
    if not os.path.exists(filename):
        return {}
    
    with open(filename, "r") as file:
        return json.load(file)

# --------------------------------------------------------
# Saving scoreboard variable to scoreboard file
# --------------------------------------------------------
def save_scoreboard(scoreboard : dict, filename : str ="scoreboard.json"):
    """
    Save the scoreboard to a JSON file.
    Args: scoreboard, that is a dictionary of players and their atrributes.
    """
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(scoreboard, file, ensure_ascii=False, indent=4)

# --------------------------------------------------------
# Update scoreboard after one game round and save it
# --------------------------------------------------------
def update_scoreboard(scoreboard: dict, player_name: str, game_state: dict, tries: int):
    """
    Update the scoreboard for player that recently played the game.
    If player does not exists in JSON file, first create a dictionary.
    According to game state, update player attributes.
    Args: scoreboard, playar name, game state for the player, and number of tries player did.
    """

    if player_name not in scoreboard:
        scoreboard[player_name] = {"games" : 0, "wins" : 0, "losses" : 0, "best_score" : None}
    
    scoreboard[player_name]["games"] += 1

    if game_state["status"] == "won":
        scoreboard[player_name]["wins"] += 1
        if scoreboard[player_name]["best_score"] is None or tries < scoreboard[player_name]["best_score"]:
            scoreboard[player_name]["best_score"] = tries
    elif game_state["status"] == "lost":
        scoreboard[player_name]["losses"] += 1

    

# --------------------------------------------------------
# Difficulty & range Selection
# --------------------------------------------------------
def choose_difficulty() -> tuple[int, int, int]:
    """
    Show difficulty levels to player to choose one.
    According to difficulty level chosen, pick a random number between one and a maximum number,
    named secret number.
    Returns: random number, number of guesses player allowed to make, and maximum number.
    """
    while True:
        level = input("Choose difficulty (easy / medium / hard): ").lower()

        if level == "easy":
            return random.randint(1, 10), 5, 10
        elif level == "medium":
            return random.randint(1, 20), 4, 20
        elif level == "hard":
            return random.randint(1, 50), 3, 50
        else:
            print("❌ Invalid choice. Try again.")

# --------------------------------------------------------
# Choosing a number in range
# --------------------------------------------------------
def get_valid_guess(max_number: int) -> int | None:
    """
    Get a number from player and return it.
    Player can enter 'q' for quiting the game. 
    If the guess is out of range, send a mesage and repeat the process.
    Args: maximum range.
    Reeturns: number guessed or 'q'.
    """
    while True:
        guess = input("Enter your guess: ").lower()
        if guess == 'q':
            return None
        elif not guess.isdigit():
            print("Please enter a number.")
            continue

        guess = int(guess)
        if 1 <= guess <= max_number:
            return guess
        else:
            print(f"Number must be between 1 and {max_number}.")

# --------------------------------------------------------
# Playing one game round
# --------------------------------------------------------
def play_round(game_state: dict) -> int:
    """
    Player plays one round of game to guess a number.
    After each attempt, the game shows hints to player if the guess is above o below
    the secret number and if the guess is very close to secret number.
    Args: game state for player.
    Returns: number of tries player did, or -1 if player quits the gmae.
    """
    secret_number, attempts, maximum = choose_difficulty()
    tries = 0
    minimum = 1

    game_state["secret_number"] = secret_number
    game_state["attempts_left"] = attempts
    game_state["status"] = "playing"

    print("\n🎯 New Round Started!")
    print(f"I have chosen a number between {minimum} and {maximum}. Try to guess it!")

    while game_state["status"] == "playing":
        guess = get_valid_guess(maximum)

        if guess == None:
            tries = -1
            break 
        if guess == game_state["secret_number"]:
            game_state["status"] = "won"
            tries += 1
            continue
        elif guess < game_state["secret_number"]:
            print("⬆️ Too low.")
        else:
            print("⬇️ Too high.")

        # Hot & Cold hint
        difference = abs(secret_number - guess)
        if difference <= 2:
            print("🔥 Very hot!\n")
        elif difference <= 5:
            print("🌡️ Hot!\n")
        else:
            print("❄️ Cold\n")
        
        game_state["attempts_left"] -= 1
        tries += 1
        print(f"Attempts left: {game_state['attempts_left']}")
        if game_state["attempts_left"] == 0:
            game_state["status"] = "lost"

    return tries

# --------------------------------------------------------
# Main game function
# --------------------------------------------------------
def guess_number():
    """
    Start the game, and ask player's name.
    Save in scoreboard the result.
    """
    game_state = {
        "secret_number" : None,
        "attempts_left" : 0,
        "status": "playing"
    }
    scoreboard = load_scoreboard()
    print("🎮 Welcome to the Number Guessing Game!")
    print("Be careful — wrong guesses cost attempts!\n")
    print("Type 'q' anytime to quit.\n")

    player_name = input("Enter your name: ").strip()

    while True:
        
        # -- Isolate the current user --
        # player_stats = scoreboard[player_name]
        
        tries = play_round(game_state)

        if game_state["status"] == "won":
            print("🎉 Correct! You guessed the number.")
            print(f"\n🎉 You won! The number was '{game_state['secret_number']}'.")
        elif game_state["status"] == "lost":
            print(f"\n💀 You lost. The number was '{game_state['secret_number']}'.")

        if tries > -1:
            update_scoreboard(scoreboard, player_name, game_state, tries)
            save_scoreboard(scoreboard)

        if player_name in scoreboard:
            print(f"\n📁 All-time stats for {player_name} → Games: {scoreboard[player_name]['games']} | "
                f"Wins: {scoreboard[player_name]['wins']} | Losses: {scoreboard[player_name]['losses']} |"
                f"Best score: {scoreboard[player_name]['best_score']}"
            )

        again = input("Do you want to play again? (y/n): ").lower()
        if again != "y":
            print("\nThanks for playing 👋")
            break

# --------------------------------------------------------
# Start the game
# --------------------------------------------------------
if __name__ == "__main__":
    guess_number()