def choose_difficulty():
    pass

def play_round(game_state):
    pass

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