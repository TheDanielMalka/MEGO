import random
import os
import sys
import time
from colorama import Fore, init

init(autoreset=True)

sys.path.append(os.path.join(os.path.dirname(__file__), "GameData"))
import game_auth

GAME_NAME = "Tic Tac Toe"


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def display_board(board):
    print(f"\n{Fore.CYAN}  {board[0]} | {board[1]} | {board[2]} ")
    print(f"{Fore.CYAN} -----------")
    print(f"{Fore.CYAN}  {board[3]} | {board[4]} | {board[5]} ")
    print(f"{Fore.CYAN} -----------")
    print(f"{Fore.CYAN}  {board[6]} | {board[7]} | {board[8]} \n")


def player_input(player, board):
    while True:
        try:
            player_choice = int(input(f"{Fore.WHITE}[Player {Fore.GREEN if player == 'X' else Fore.RED}{player}{Fore.WHITE}] Enter your choice (1-9): "))
            if 1 <= player_choice <= 9:
                if board[player_choice - 1] not in ["X", "O"]:
                    return player_choice
                else:
                    print(f"{Fore.RED}This spot is already taken!")
            else:
                print(f"{Fore.RED}Please enter a number between 1 and 9")
        except ValueError:
            print(f"{Fore.RED}Invalid input! Please enter a number")


def check_winner(board):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]

    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]]:
            if board[condition[0]] in ["X", "O"]:
                return True
    return False


def check_tie(board):
    for cell in board:
        if cell not in ["X", "O"]:
            return False
    return True


def play_game_round(username):
    game_board = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    players = ["X", "O"]
    current_player = random.choice(players)

    clear_screen()
    print(f"\n{Fore.YELLOW}{'='*50}")
    print(f"{Fore.YELLOW}TIC TAC TOE GAME")
    print(f"{Fore.YELLOW}{'='*50}")
    print(f"\n{Fore.WHITE}Starting player: {Fore.GREEN if current_player == 'X' else Fore.RED}{current_player}")
    print(f"{Fore.YELLOW}{'='*50}\n")

    while not check_winner(game_board) and not check_tie(game_board):
        display_board(game_board)
        choice = player_input(current_player, game_board)
        game_board[choice - 1] = current_player

        if check_winner(game_board):
            clear_screen()
            display_board(game_board)
            print(f"\n{Fore.GREEN}{'='*50}")
            print(f"{Fore.GREEN}Player {current_player} WINS!")
            print(f"{Fore.GREEN}{'='*50}")

            stats = game_auth.get_user_stats(username, GAME_NAME)
            wins = stats.get(f"{current_player} Wins", 0)
            game_auth.update_user_stats(username, GAME_NAME, {f"{current_player} Wins": wins + 1})

            total_wins = stats.get("Total Wins", 0)
            game_auth.update_user_stats(username, GAME_NAME, {"Total Wins": total_wins + 1})
            game_auth.update_user_high_score(username, GAME_NAME, "Total Wins", total_wins + 1)
            game_auth.update_leaderboard(username, GAME_NAME, "Total Wins", total_wins + 1, higher_is_better=True)

            return True

        if check_tie(game_board):
            clear_screen()
            display_board(game_board)
            print(f"\n{Fore.YELLOW}{'='*50}")
            print(f"{Fore.YELLOW}IT'S A TIE!")
            print(f"{Fore.YELLOW}{'='*50}")

            stats = game_auth.get_user_stats(username, GAME_NAME)
            ties = stats.get("Ties", 0)
            game_auth.update_user_stats(username, GAME_NAME, {"Ties": ties + 1})

            return False

        current_player = "O" if current_player == "X" else "X"
        clear_screen()


def game_menu(username):
    while True:
        clear_screen()
        print(f"\n{Fore.CYAN}{'='*50}")
        print(f"{Fore.CYAN}TIC TAC TOE - {username}")
        print(f"{Fore.CYAN}{'='*50}")
        print(f"\n{Fore.WHITE}1. Play Game")
        print(f"{Fore.WHITE}2. View My Stats")
        print(f"{Fore.WHITE}3. View Game Leaderboard")
        print(f"{Fore.WHITE}4. View All Games Leaderboard")
        print(f"{Fore.WHITE}5. Switch User")
        print(f"{Fore.WHITE}6. Exit")

        choice = input(f"\n{Fore.WHITE}Choose (1-6): ")

        if choice == '1':
            play_game_round(username)
            input(f"\n{Fore.WHITE}Press ENTER to continue...")
        elif choice == '2':
            game_auth.display_user_stats(username, GAME_NAME)
            input(f"\n{Fore.WHITE}Press ENTER to continue...")
        elif choice == '3':
            game_auth.display_game_leaderboard(GAME_NAME)
            input(f"\n{Fore.WHITE}Press ENTER to continue...")
        elif choice == '4':
            game_auth.display_all_leaderboards()
            input(f"\n{Fore.WHITE}Press ENTER to continue...")
        elif choice == '5':
            return True
        elif choice == '6':
            return False
        else:
            print(f"{Fore.RED}Invalid choice!")
            time.sleep(1)


def main():
    data_dir = os.path.join(os.path.dirname(__file__), "GameData")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    while True:
        username = game_auth.user_authentication(GAME_NAME, clear_screen)
        if not username:
            print(f"\n{Fore.CYAN}Thanks for playing!")
            break

        switch_user = game_menu(username)
        if not switch_user:
            print(f"\n{Fore.CYAN}Thanks for playing!")
            break


if __name__ == "__main__":
    main()
