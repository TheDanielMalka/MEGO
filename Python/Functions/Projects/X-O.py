import random


def original_game_board():
    return ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

game_board = original_game_board()
players = ["X", "O"]
current_player = random.choice(players)

def display_board(board):
    """display the board at the current situation of the game"""
    print(f"{board[0]} | {board[1]} | {board[2]} \n"
          f"{board[3]} | {board[4]} | {board[5]} \n"
          f"{board[6]} | {board[7]} | {board[8]}")

def player_input(player):
    """ takes user input and returns their position choice """
    """ btw - added try \ except for invalid inputs"""
    while True:
        try:
            player_choice = int(input(f"[Player {player}] Enter your choice: "))
            if 1 <= player_choice <= 9:
                return player_choice
            else:
                print("Please enter a number between 1 and 9")
        except ValueError:
            print("Invalid input! Please enter a number")

def check_winner(board):
    """" checks if the game board is full and one of the conditions true"""
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


def check_tie(board):
    """" do the same as winner - checkes if board full and no winner condition true"""
    for cell in board:
        if cell not in ["X", "O"]:
            return False
    return True


def ask_play_again():
    """" function that can restart the game by choice """
    while True:
        play_again = input("\nDo you want to play again? (y/n): ").lower()
        if play_again == "y":
            return True
        elif play_again == "n":
            return False
        else:
            print("Invalid input!")


def play_game():
    global current_player, game_board
    print("\n" + "=" * 50)
    print("WELCOME TO".center(50))
    print("Tic Tac Toe Game".center(50))
    print("=" * 50)
    print(f"Starting player is: {current_player}")

    while not check_winner(game_board) or not check_tie(game_board):
        """" used this condition instead of 'while True:' so its be more readable"""

        display_board(game_board)
        rand = player_input(current_player)

        while not check_winner(game_board) or not check_tie(game_board):
            """" checks if the game board position empty if it does and 
            its in the range - fills it otherwise keep asking for 
             good position """

            if game_board[(rand - 1)] == "X" or game_board[(rand - 1)] == "O":
                print(f"This spot already taken")
                rand = player_input(current_player)
            else:
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

        if check_tie(game_board):
            display_board(game_board)
            print("It's a tie!")
            break

    if ask_play_again():
        """" if decided to play again - restart the board again from the function
         and again picks randon player to start with """
        game_board = original_game_board()
        current_player = random.choice(players)
        play_game()

play_game()