import random
import os
import sys
import time
from colorama import Fore, init

init(autoreset=True)

sys.path.append(os.path.join(os.path.dirname(__file__), "GameData"))
import game_auth

GAME_NAME = "Coin Game"

min_cells = 10
max_cells = 30


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def welcome_message():
    print(f"\n{Fore.YELLOW}{'='*50}")
    print(f"{Fore.YELLOW}WELCOME TO".center(50))
    print(f"{Fore.YELLOW}Coin Game !".center(52))
    print(f"{Fore.YELLOW}{'='*50}\n")


def get_cellnum():
    global min_cells, max_cells
    cell_number = int(input(f"{Fore.WHITE}Enter cells number (10-30) for board length: "))
    while True:
        if max_cells >= cell_number >= min_cells:
            return cell_number
        else:
            print(f"{Fore.RED}Number must be between 10-30")
            cell_number = int(input(f"{Fore.WHITE}Please enter a cell number: "))


def place_coins_rand(cellnum):
    coins = random.sample(range(cellnum), 4)
    coins.sort()
    return coins


def draw_board(coins, cellnum):
    print(f"\n{Fore.CYAN}", end="")
    for i in range(cellnum):
        if i in coins:
            print(f"{Fore.YELLOW}[C]", end=" ")
        else:
            print(f"{Fore.CYAN}[ ]", end=" ")
    print()


def draw_line(length):
    print(f"{Fore.CYAN}{'-' * length * 4}")


def gameover(coins):
    for i in range(len(coins)):
        if coins[i] > 0:
            if i == 0:
                return False
            elif coins[i] - coins[i - 1] > 1:
                return False
    return True


def make_move(coins, player):
    while True:
        try:
            coin = int(input(f"\n{Fore.WHITE}Player {Fore.GREEN if player == 1 else Fore.RED}{player}{Fore.WHITE}, pick coin (1-4 from left to right): "))
            if coin < 1 or coin > 4:
                print(f"{Fore.RED}Must pick coin 1-4!")
                continue

            move = int(input(f"{Fore.WHITE}Steps left: "))
            coin_index = coins[coin - 1]
            new_index = coin_index - move

            if new_index < 0:
                print(f"{Fore.RED}You're out of range!")
                continue

            if new_index in coins:
                print(f"{Fore.RED}You got a coin there!")
                continue

            valid = True
            for check in coins:
                if new_index < check < coin_index:
                    valid = False
                    break

            if not valid:
                print(f"{Fore.RED}Can't pass over a coin!")
                continue

            coins[coin - 1] = new_index
            coins.sort()
            break

        except ValueError:
            print(f"{Fore.RED}Please enter a valid number!")


def play_game_round(username):
    player_number = 1
    clear_screen()
    welcome_message()

    cellnums = get_cellnum()
    picked_coins = place_coins_rand(cellnums)

    draw_board(picked_coins, cellnums)
    draw_line(cellnums)
    print(f"{Fore.GREEN}Here's your starting board! Good Luck!".center(50))

    moves_count = 0

    while not gameover(picked_coins):
        make_move(picked_coins, player_number)
        moves_count += 1
        clear_screen()
        draw_board(picked_coins, cellnums)
        draw_line(cellnums)
        player_number = 3 - player_number

    winner = 3 - player_number

    print(f"\n{Fore.GREEN}{'='*50}")
    print(f"{Fore.GREEN}GAME OVER!")
    print(f"{Fore.GREEN}Well done! Player {winner} has won!")
    print(f"{Fore.GREEN}Total moves: {moves_count}")
    print(f"{Fore.GREEN}{'='*50}")

    stats = game_auth.get_user_stats(username, GAME_NAME)
    wins = stats.get(f"Player {winner} Wins", 0)
    game_auth.update_user_stats(username, GAME_NAME, {f"Player {winner} Wins": wins + 1})

    total_games = stats.get("Total Games", 0)
    game_auth.update_user_stats(username, GAME_NAME, {"Total Games": total_games + 1})
    game_auth.update_user_high_score(username, GAME_NAME, "Total Games", total_games + 1)
    game_auth.update_leaderboard(username, GAME_NAME, "Total Games", total_games + 1, higher_is_better=True)


def game_menu(username):
    while True:
        clear_screen()
        print(f"\n{Fore.CYAN}{'='*50}")
        print(f"{Fore.CYAN}COIN GAME - {username}")
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
