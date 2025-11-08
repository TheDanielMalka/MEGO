import random
game_board = [ "1", "2", "3",
               "4", "5", "6",
               "7", "8", "9"]
players = ["X", "O"]
current_player = random.choice(players)

def display_board(board):
    """Display the board at the current situation of the game"""
    print(f"{board[0]} | {board[1]} | {board[2]} \n"
          f"{board[3]} | {board[4]} | {board[5]} \n"
          f"{board[6]} | {board[7]} | {board[8]}")

def player_input(player):
    """ Takes user input and returns their position choice """
    player_choice = int(input(f"[Player {player}] Enter your choice: "))
    return player_choice

def check_winner(board):
    """Checks if the player has won"""
    if (board[0] == board[1] == board[2]
            or board[3] == board[4] == board[5]
            or board[6] == board[7] == board[8]):
        return True
    elif (board[0] == board[3] == board[6] or
          board[1] == board[4] == board[7] or
          board[2] == board[5] == board[8]):
        return True
    elif (board[0] == board[4] == board[8]
          or board[2] == board[4] == board[6]):
        return True
    else:
        return False


def play_game():
    global current_player
    print("\n" + "=" * 50)
    print("WELCOME TO".center(50))
    print("Tic Tac Toe Game".center(50))
    print("=" * 50)
    print(f"Starting player is: {current_player}")

    while not check_winner(game_board):
        display_board(game_board)
        rand = player_input(current_player)
        while True:
            if game_board[(rand - 1)] == "X" or game_board[(rand - 1)] == "O":
                print(f"This spot already taken try again")
                rand = player_input(current_player)
            if game_board[(rand - 1)] != "X" or game_board[(rand - 1)] != "O":
                game_board[(rand - 1)] = current_player
                if current_player == "X":
                    current_player = "O"
                    break
                else:
                    current_player = "X"
                    break
        if check_winner(game_board):
            if current_player == "X":
                current_player = "O"
            else:
                current_player = "X"
            display_board(game_board)
            print(f"Player {current_player} won!")
            break
play_game()
