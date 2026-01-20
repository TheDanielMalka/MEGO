import random
import time
import os
import sys
from colorama import Fore, init

init(autoreset=True)

sys.path.append(os.path.join(os.path.dirname(__file__), "GameData"))
import game_auth

GAME_NAME = "Memory Game"

DIFFICULTIES = {
    "1": {"name": "BEGINNER", "range": (1, 50), "start_length": 3, "time_mult": 1.2},
    "2": {"name": "ADVANCED", "range": (1, 150), "start_length": 4, "time_mult": 1.0},
    "3": {"name": "PRO", "range": (1, 300), "start_length": 5, "time_mult": 0.8},
    "4": {"name": "HARDCORE", "range": (1, 500), "start_length": 6, "time_mult": 0.6}
}


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def show_numbers(numbers, display_time):
    print(f"\n{Fore.YELLOW}{'='*50}")
    print(f"{Fore.YELLOW}MEMORIZE THESE NUMBERS:")
    print(f"{Fore.YELLOW}{'='*50}")
    print(f"\n{Fore.CYAN}{' -> '.join(map(str, numbers))}\n")
    print(f"{Fore.YELLOW}{'='*50}")
    time.sleep(display_time)
    clear_screen()


def get_user_input(length):
    print(f"\n{Fore.GREEN}{'='*50}")
    print(f"{Fore.GREEN}ENTER THE NUMBERS YOU REMEMBER:")
    print(f"{Fore.GREEN}{'='*50}")
    user_numbers = []
    for i in range(length):
        while True:
            try:
                num = int(input(f"{Fore.WHITE}Number {i+1}: "))
                user_numbers.append(num)
                break
            except ValueError:
                print(f"{Fore.RED}Please enter a valid number!")
    return user_numbers


def play_round(level, difficulty_config, difficulty_name):
    sequence_length = difficulty_config["start_length"] + level
    display_time = max(1.5, 5 - level * 0.5) * difficulty_config["time_mult"]

    num_range = difficulty_config["range"]
    numbers = [random.randint(num_range[0], num_range[1]) for _ in range(sequence_length)]

    print(f"\n{Fore.MAGENTA}{'='*50}")
    print(f"{Fore.MAGENTA}LEVEL {level + 1} - {difficulty_name}")
    print(f"{Fore.MAGENTA}Remember {sequence_length} numbers!")
    print(f"{Fore.MAGENTA}{'='*50}")
    input(f"\n{Fore.WHITE}Press ENTER when ready...")

    show_numbers(numbers, display_time)

    user_numbers = get_user_input(sequence_length)

    if user_numbers == numbers:
        print(f"\n{Fore.GREEN}{'='*50}")
        print(f"{Fore.GREEN}CORRECT! Moving to next level!")
        print(f"{Fore.GREEN}{'='*50}")
        time.sleep(1.5)
        return True
    else:
        print(f"\n{Fore.RED}{'='*50}")
        print(f"{Fore.RED}WRONG!")
        print(f"{Fore.WHITE}Correct sequence: {' -> '.join(map(str, numbers))}")
        print(f"{Fore.YELLOW}Your sequence:    {' -> '.join(map(str, user_numbers))}")
        print(f"{Fore.RED}{'='*50}")
        return False


def select_difficulty():
    print(f"\n{Fore.CYAN}{'='*50}")
    print(f"{Fore.CYAN}SELECT DIFFICULTY:")
    print(f"{Fore.CYAN}{'='*50}")
    for key, diff in DIFFICULTIES.items():
        print(f"{Fore.YELLOW}{key}. {diff['name']}")

    while True:
        choice = input(f"\n{Fore.WHITE}Enter difficulty (1-4): ")
        if choice in DIFFICULTIES:
            return choice, DIFFICULTIES[choice]
        print(f"{Fore.RED}Invalid choice! Try again.")


def game_menu(username):
    while True:
        clear_screen()
        print(f"\n{Fore.CYAN}{'='*50}")
        print(f"{Fore.CYAN}MEMORY GAME - {username}")
        print(f"{Fore.CYAN}{'='*50}")
        print(f"\n{Fore.WHITE}1. Play Game")
        print(f"{Fore.WHITE}2. View My High Scores")
        print(f"{Fore.WHITE}3. View Game Leaderboard")
        print(f"{Fore.WHITE}4. View All Games Leaderboard")
        print(f"{Fore.WHITE}5. Switch User")
        print(f"{Fore.WHITE}6. Exit")

        choice = input(f"\n{Fore.WHITE}Choose (1-6): ")

        if choice == '1':
            play_game(username)
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


def play_game(username):
    clear_screen()
    print(f"\n{Fore.CYAN}{'='*50}")
    print(f"{Fore.CYAN}MEMORY GAME")
    print(f"{Fore.CYAN}{'='*50}")
    print(f"\n{Fore.WHITE}How to play:")
    print(f"{Fore.WHITE}1. Numbers will appear on screen")
    print(f"{Fore.WHITE}2. Memorize them quickly!")
    print(f"{Fore.WHITE}3. Enter them in the correct order")
    print(f"{Fore.WHITE}4. Each level gets harder!")

    game_auth.display_user_high_scores(username, GAME_NAME)

    print(f"\n{Fore.CYAN}{'='*50}")
    input(f"\n{Fore.WHITE}Press ENTER to continue...")

    _, difficulty_config = select_difficulty()
    difficulty_name = difficulty_config["name"]

    level = 0
    playing = True

    while playing:
        clear_screen()
        success = play_round(level, difficulty_config, difficulty_name)

        if success:
            level += 1
        else:
            final_level = level + 1
            print(f"\n{Fore.YELLOW}GAME OVER! You reached level {final_level}")
            print(f"{Fore.YELLOW}{'='*50}")

            is_new_record = game_auth.update_user_high_score(username, GAME_NAME, difficulty_name, final_level)
            if is_new_record:
                print(f"{Fore.GREEN}NEW HIGH SCORE FOR {difficulty_name}!")
                game_auth.update_leaderboard(username, GAME_NAME, difficulty_name, final_level, higher_is_better=True)

            print(f"\n{Fore.WHITE}1. Play again")
            print(f"{Fore.WHITE}2. View Leaderboard")
            print(f"{Fore.WHITE}3. Switch User")
            print(f"{Fore.WHITE}4. Back to Menu")

            choice = input(f"\n{Fore.WHITE}Choose (1-4): ")

            if choice == '1':
                _, difficulty_config = select_difficulty()
                difficulty_name = difficulty_config["name"]
                level = 0
                clear_screen()
            elif choice == '2':
                game_auth.display_game_leaderboard(GAME_NAME)
                input(f"\n{Fore.WHITE}Press ENTER to continue...")
                playing = False
            elif choice == '3':
                main()
                return
            else:
                playing = False


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
