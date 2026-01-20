import os
import sys
import time
from colorama import Fore, init

init(autoreset=True)

sys.path.append(os.path.join(os.path.dirname(__file__), "GameData"))
import game_auth

GAME_NAME = "ReactionTimeGame"


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

import random
import time

def play_game_round(username):
    clear_screen()
    print(f"\n{{Fore.YELLOW}}{{'='*50}}")
    print(f"{{Fore.YELLOW}}REACTION TIME GAME")
    print(f"{{Fore.YELLOW}}{{'='*50}}")
    print(f"\n{{Fore.WHITE}}Press ENTER when you see GO!")

    input(f"{{Fore.CYAN}}Press ENTER to start...")

    clear_screen()
    print(f"{{Fore.RED}}WAIT...")
    time.sleep(random.uniform(2, 5))

    clear_screen()
    print(f"{{Fore.GREEN}}GO!")
    start = time.time()
    input()
    reaction_time = time.time() - start

    print(f"\n{{Fore.CYAN}}Your reaction time: {{reaction_time:.3f}} seconds")

    current_best = game_auth.get_user_high_scores(username, GAME_NAME).get("Best Time", 999)
    if reaction_time < current_best:
        game_auth.update_user_high_score(username, GAME_NAME, "Best Time", round(reaction_time, 3))
        game_auth.update_leaderboard(username, GAME_NAME, "Fastest Time", round(reaction_time, 3), higher_is_better=False)
        print(f"{{Fore.GREEN}}NEW RECORD!")

    stats = game_auth.get_user_stats(username, GAME_NAME)
    total = stats.get("Total Games", 0) + 1
    game_auth.update_user_stats(username, GAME_NAME, {{"Total Games": total}})

def game_menu(username):
    while True:
        clear_screen()
        print(f"\n{{Fore.CYAN}}{{'='*50}}")
        print(f"{{Fore.CYAN}}{{GAME_NAME.upper()}} - {{username}}")
        print(f"\n{{Fore.WHITE}}1. Play Game")
        print(f"{{Fore.WHITE}}2. View My High Scores")
        print(f"{{Fore.WHITE}}3. View Game Leaderboard")
        print(f"{{Fore.WHITE}}4. View All Games Leaderboard")
        print(f"{{Fore.WHITE}}5. Switch User")
        print(f"{{Fore.WHITE}}6. Exit")

        choice = input(f"\n{{Fore.WHITE}}Choose (1-6): ")

        if choice == '1':
            play_game_round(username)
            input(f"\n{{Fore.WHITE}}Press ENTER to continue...")
        elif choice == '2':
            game_auth.display_user_high_scores(username, GAME_NAME)
            input(f"\n{{Fore.WHITE}}Press ENTER to continue...")
        elif choice == '3':
            game_auth.display_game_leaderboard(GAME_NAME)
            input(f"\n{{Fore.WHITE}}Press ENTER to continue...")
        elif choice == '4':
            game_auth.display_all_leaderboards()
            input(f"\n{{Fore.WHITE}}Press ENTER to continue...")
        elif choice == '5':
            return True
        elif choice == '6':
            return False
        else:
            print(f"{{Fore.RED}}Invalid choice!")
            time.sleep(1)


def main():
    data_dir = os.path.join(os.path.dirname(__file__), "GameData")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    while True:
        username = game_auth.user_authentication(GAME_NAME, clear_screen)
        if not username:
            print(f"\n{{Fore.CYAN}}Thanks for playing!")
            break

        switch_user = game_menu(username)
        if not switch_user:
            print(f"\n{{Fore.CYAN}}Thanks for playing!")
            break


if __name__ == "__main__":
    main()
