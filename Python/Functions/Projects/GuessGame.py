import random
import os
import sys
import time
from colorama import Fore, init

init(autoreset=True)

sys.path.append(os.path.join(os.path.dirname(__file__), "GameData"))
import game_auth

GAME_NAME = "Guess Game"


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def play_game_round(username):
    random_num = random.randint(1, 100)
    counter = 0
    max_tries = 10
    guessed_numbers = []

    clear_screen()
    print(f"\n{Fore.CYAN}{'='*50}")
    print(f"{Fore.CYAN}GUESS THE NUMBER GAME")
    print(f"{Fore.CYAN}{'='*50}")
    print(f"\n{Fore.WHITE}Try to guess the number between 1-100")
    print(f"{Fore.WHITE}You have {max_tries} tries!")
    print(f"{Fore.CYAN}{'='*50}\n")

    while counter < max_tries:
        try:
            try_input = int(input(f"{Fore.WHITE}Guess #{counter+1}: "))

            if try_input < 1 or try_input > 100:
                print(f"{Fore.RED}Number must be between 1 and 100!")
                continue

            if try_input in guessed_numbers:
                print(f"{Fore.YELLOW}You already guessed {try_input}! Try again!")
                continue

            guessed_numbers.append(try_input)
            counter += 1

            if try_input == random_num:
                print(f"\n{Fore.GREEN}{'='*50}")
                print(f"{Fore.GREEN}CORRECT! {try_input} is the number!")
                print(f"{Fore.GREEN}You won with {counter} tries!")
                print(f"{Fore.GREEN}{'='*50}")

                current_best = game_auth.get_user_high_scores(username, GAME_NAME).get("Least Tries", 999)
                if counter < current_best:
                    game_auth.update_user_high_score(username, GAME_NAME, "Least Tries", counter)
                    game_auth.update_leaderboard(username, GAME_NAME, "Least Tries", counter, higher_is_better=False)
                    print(f"{Fore.YELLOW}NEW BEST RECORD!")

                return True

            elif try_input < random_num:
                print(f"{Fore.YELLOW}Too Low!")
            else:
                print(f"{Fore.YELLOW}Too High!")

            if len(guessed_numbers) > 0:
                print(f"{Fore.CYAN}Guessed: {sorted(guessed_numbers)}")
            print(f"{Fore.WHITE}Tries left: {max_tries - counter}")

        except ValueError:
            print(f"{Fore.RED}Please enter a valid number!")

    print(f"\n{Fore.RED}{'='*50}")
    print(f"{Fore.RED}GAME OVER!")
    print(f"{Fore.RED}The number was {random_num}")
    print(f"{Fore.RED}{'='*50}")
    return False


def game_menu(username):
    while True:
        clear_screen()
        print(f"\n{Fore.CYAN}{'='*50}")
        print(f"{Fore.CYAN}GUESS GAME - {username}")
        print(f"{Fore.CYAN}{'='*50}")
        print(f"\n{Fore.WHITE}1. Play Game")
        print(f"{Fore.WHITE}2. View My High Scores")
        print(f"{Fore.WHITE}3. View Game Leaderboard")
        print(f"{Fore.WHITE}4. View All Games Leaderboard")
        print(f"{Fore.WHITE}5. Switch User")
        print(f"{Fore.WHITE}6. Exit")

        choice = input(f"\n{Fore.WHITE}Choose (1-6): ")

        if choice == '1':
            play_game_round(username)
            input(f"\n{Fore.WHITE}Press ENTER to continue...")
        elif choice == '2':
            game_auth.display_user_high_scores(username, GAME_NAME)
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
