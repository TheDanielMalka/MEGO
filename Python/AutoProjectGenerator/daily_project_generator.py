import os
import random
from datetime import datetime


PROJECTS_DIR = os.path.join(os.path.dirname(__file__), "..", "Functions", "Projects")

GAME_AUTH_IMPORT = """import os
import sys
import time
from colorama import Fore, init

init(autoreset=True)

sys.path.append(os.path.join(os.path.dirname(__file__), "GameData"))
import game_auth

GAME_NAME = "{game_name}"


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

"""

GAME_MENU_TEMPLATE = """
def game_menu(username):
    while True:
        clear_screen()
        print(f"\\n{Fore.CYAN}{'='*50}")
        print(f"{Fore.CYAN}{GAME_NAME.upper()} - {username}")
        print(f"\\n{Fore.WHITE}1. Play Game")
        print(f"{Fore.WHITE}2. View My High Scores")
        print(f"{Fore.WHITE}3. View Game Leaderboard")
        print(f"{Fore.WHITE}4. View All Games Leaderboard")
        print(f"{Fore.WHITE}5. Switch User")
        print(f"{Fore.WHITE}6. Exit")

        choice = input(f"\\n{Fore.WHITE}Choose (1-6): ")

        if choice == '1':
            play_game_round(username)
            input(f"\\n{Fore.WHITE}Press ENTER to continue...")
        elif choice == '2':
            game_auth.display_user_high_scores(username, GAME_NAME)
            input(f"\\n{Fore.WHITE}Press ENTER to continue...")
        elif choice == '3':
            game_auth.display_game_leaderboard(GAME_NAME)
            input(f"\\n{Fore.WHITE}Press ENTER to continue...")
        elif choice == '4':
            game_auth.display_all_leaderboards()
            input(f"\\n{Fore.WHITE}Press ENTER to continue...")
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
            print(f"\\n{Fore.CYAN}Thanks for playing!")
            break

        switch_user = game_menu(username)
        if not switch_user:
            print(f"\\n{Fore.CYAN}Thanks for playing!")
            break


if __name__ == "__main__":
    main()
"""

PROJECTS = {
    "games": [
        {
            "name": "NumberGuessingRace",
            "code": """import random

def play_game_round(username):
    target = random.randint(1, 100)
    attempts = 0
    max_attempts = 7

    clear_screen()
    print(f"\\n{{Fore.YELLOW}}{{'='*50}}")
    print(f"{{Fore.YELLOW}}NUMBER GUESSING RACE")
    print(f"{{Fore.YELLOW}}{{'='*50}}")
    print(f"\\n{{Fore.WHITE}}Guess the number between 1-100")
    print(f"{{Fore.WHITE}}You have {{max_attempts}} attempts!")

    while attempts < max_attempts:
        try:
            guess = int(input(f"\\n{{Fore.CYAN}}Attempt {{attempts+1}}/{{max_attempts}}: "))
            attempts += 1

            if guess == target:
                print(f"\\n{{Fore.GREEN}}{{'='*50}}")
                print(f"{{Fore.GREEN}}CORRECT! You won in {{attempts}} attempts!")
                print(f"{{Fore.GREEN}}{{'='*50}}")

                current_best = game_auth.get_user_high_scores(username, GAME_NAME).get("Best Score", 999)
                if attempts < current_best:
                    game_auth.update_user_high_score(username, GAME_NAME, "Best Score", attempts)
                    game_auth.update_leaderboard(username, GAME_NAME, "Least Attempts", attempts, higher_is_better=False)
                    print(f"{{Fore.YELLOW}}NEW RECORD!")
                return

            elif guess < target:
                print(f"{{Fore.YELLOW}}Too low!")
            else:
                print(f"{{Fore.YELLOW}}Too high!")

        except ValueError:
            print(f"{{Fore.RED}}Invalid input!")

    print(f"\\n{{Fore.RED}}Game Over! The number was {{target}}")
"""
        },
        {
            "name": "ReactionTimeGame",
            "code": """import random
import time

def play_game_round(username):
    clear_screen()
    print(f"\\n{{Fore.YELLOW}}{{'='*50}}")
    print(f"{{Fore.YELLOW}}REACTION TIME GAME")
    print(f"{{Fore.YELLOW}}{{'='*50}}")
    print(f"\\n{{Fore.WHITE}}Press ENTER when you see GO!")

    input(f"{{Fore.CYAN}}Press ENTER to start...")

    clear_screen()
    print(f"{{Fore.RED}}WAIT...")
    time.sleep(random.uniform(2, 5))

    clear_screen()
    print(f"{{Fore.GREEN}}GO!")
    start = time.time()
    input()
    reaction_time = time.time() - start

    print(f"\\n{{Fore.CYAN}}Your reaction time: {{reaction_time:.3f}} seconds")

    current_best = game_auth.get_user_high_scores(username, GAME_NAME).get("Best Time", 999)
    if reaction_time < current_best:
        game_auth.update_user_high_score(username, GAME_NAME, "Best Time", round(reaction_time, 3))
        game_auth.update_leaderboard(username, GAME_NAME, "Fastest Time", round(reaction_time, 3), higher_is_better=False)
        print(f"{{Fore.GREEN}}NEW RECORD!")

    stats = game_auth.get_user_stats(username, GAME_NAME)
    total = stats.get("Total Games", 0) + 1
    game_auth.update_user_stats(username, GAME_NAME, {{"Total Games": total}})
"""
        },
        {
            "name": "MathQuizChallenge",
            "code": """import random
import time

def play_game_round(username):
    clear_screen()
    print(f"\\n{{Fore.YELLOW}}{{'='*50}}")
    print(f"{{Fore.YELLOW}}MATH QUIZ CHALLENGE")
    print(f"{{Fore.YELLOW}}{{'='*50}}")

    score = 0
    questions = 5

    for i in range(questions):
        a = random.randint(1, 20)
        b = random.randint(1, 20)
        op = random.choice(['+', '-', '*'])

        if op == '+':
            answer = a + b
        elif op == '-':
            answer = a - b
        else:
            answer = a * b

        print(f"\\n{{Fore.CYAN}}Question {{i+1}}/{{questions}}")
        try:
            user_answer = int(input(f"{{Fore.WHITE}}{{a}} {{op}} {{b}} = "))
            if user_answer == answer:
                print(f"{{Fore.GREEN}}Correct!")
                score += 1
            else:
                print(f"{{Fore.RED}}Wrong! Answer: {{answer}}")
        except ValueError:
            print(f"{{Fore.RED}}Invalid input!")

    print(f"\\n{{Fore.YELLOW}}{{'='*50}}")
    print(f"{{Fore.YELLOW}}Final Score: {{score}}/{{questions}}")
    print(f"{{Fore.YELLOW}}{{'='*50}}")

    current_best = game_auth.get_user_high_scores(username, GAME_NAME).get("High Score", 0)
    if score > current_best:
        game_auth.update_user_high_score(username, GAME_NAME, "High Score", score)
        game_auth.update_leaderboard(username, GAME_NAME, "High Score", score, higher_is_better=True)
        print(f"{{Fore.GREEN}}NEW HIGH SCORE!")
"""
        },
        {
            "name": "WordScramble",
            "code": """import random

WORDS = ["python", "programming", "computer", "keyboard", "algorithm", "function", "variable", "database"]

def play_game_round(username):
    word = random.choice(WORDS)
    scrambled = ''.join(random.sample(word, len(word)))
    attempts = 0
    max_attempts = 3

    clear_screen()
    print(f"\\n{{Fore.YELLOW}}{{'='*50}}")
    print(f"{{Fore.YELLOW}}WORD SCRAMBLE")
    print(f"{{Fore.YELLOW}}{{'='*50}}")
    print(f"\\n{{Fore.CYAN}}Unscramble this word: {{Fore.GREEN}}{{scrambled}}")
    print(f"{{Fore.WHITE}}You have {{max_attempts}} attempts")

    while attempts < max_attempts:
        guess = input(f"\\n{{Fore.WHITE}}Your guess: ").lower()
        attempts += 1

        if guess == word:
            print(f"\\n{{Fore.GREEN}}CORRECT!")
            stats = game_auth.get_user_stats(username, GAME_NAME)
            wins = stats.get("Wins", 0) + 1
            game_auth.update_user_stats(username, GAME_NAME, {{"Wins": wins}})
            game_auth.update_user_high_score(username, GAME_NAME, "Total Wins", wins)
            game_auth.update_leaderboard(username, GAME_NAME, "Total Wins", wins, higher_is_better=True)
            return
        else:
            print(f"{{Fore.RED}}Wrong! {{max_attempts - attempts}} attempts left")

    print(f"\\n{{Fore.RED}}Game Over! The word was: {{word}}")
"""
        },
        {
            "name": "RockPaperScissorsRounds",
            "code": """import random

CHOICES = {{"1": "Rock", "2": "Paper", "3": "Scissors"}}

def get_winner(player, computer):
    if player == computer:
        return "tie"
    if (player == "Rock" and computer == "Scissors") or \\
       (player == "Paper" and computer == "Rock") or \\
       (player == "Scissors" and computer == "Paper"):
        return "player"
    return "computer"

def play_game_round(username):
    clear_screen()
    print(f"\\n{{Fore.YELLOW}}{{'='*50}}")
    print(f"{{Fore.YELLOW}}ROCK PAPER SCISSORS")
    print(f"{{Fore.YELLOW}}{{'='*50}}")

    player_score = 0
    computer_score = 0
    rounds = 5

    for i in range(rounds):
        print(f"\\n{{Fore.CYAN}}Round {{i+1}}/{{rounds}}")
        print(f"{{Fore.WHITE}}1. Rock  2. Paper  3. Scissors")

        choice = input(f"\\n{{Fore.WHITE}}Your choice: ")
        if choice not in CHOICES:
            print(f"{{Fore.RED}}Invalid choice!")
            continue

        player_choice = CHOICES[choice]
        computer_choice = random.choice(list(CHOICES.values()))

        print(f"{{Fore.CYAN}}You: {{player_choice}} vs Computer: {{computer_choice}}")

        result = get_winner(player_choice, computer_choice)
        if result == "player":
            print(f"{{Fore.GREEN}}You win this round!")
            player_score += 1
        elif result == "computer":
            print(f"{{Fore.RED}}Computer wins this round!")
            computer_score += 1
        else:
            print(f"{{Fore.YELLOW}}Tie!")

    print(f"\\n{{Fore.YELLOW}}{{'='*50}}")
    if player_score > computer_score:
        print(f"{{Fore.GREEN}}YOU WIN! {{player_score}}-{{computer_score}}")
        stats = game_auth.get_user_stats(username, GAME_NAME)
        wins = stats.get("Wins", 0) + 1
        game_auth.update_user_stats(username, GAME_NAME, {{"Wins": wins}})
        game_auth.update_user_high_score(username, GAME_NAME, "Total Wins", wins)
        game_auth.update_leaderboard(username, GAME_NAME, "Total Wins", wins, higher_is_better=True)
    elif computer_score > player_score:
        print(f"{{Fore.RED}}COMPUTER WINS! {{computer_score}}-{{player_score}}")
    else:
        print(f"{{Fore.YELLOW}}IT'S A TIE! {{player_score}}-{{computer_score}}")
    print(f"{{Fore.YELLOW}}{{'='*50}}")
"""
        },
        {
            "name": "ColorMemoryGame",
            "code": """import random
import time

COLORS = ["Red", "Blue", "Green", "Yellow", "Purple", "Orange"]

def play_game_round(username):
    clear_screen()
    print(f"\\n{{Fore.YELLOW}}{{'='*50}}")
    print(f"{{Fore.YELLOW}}COLOR MEMORY GAME")
    print(f"{{Fore.YELLOW}}{{'='*50}}")

    level = 1

    while True:
        sequence = [random.choice(COLORS) for _ in range(level + 2)]

        print(f"\\n{{Fore.CYAN}}Level {{level}}")
        print(f"{{Fore.WHITE}}Memorize this sequence:")
        print(f"{{Fore.MAGENTA}}{{' -> '.join(sequence)}}")
        time.sleep(2 + level * 0.5)
        clear_screen()

        print(f"{{Fore.WHITE}}Enter the colors (separated by spaces):")
        user_input = input(f"{{Fore.CYAN}}Your answer: ").title().split()

        if user_input == sequence:
            print(f"{{Fore.GREEN}}Correct! Moving to level {{level + 1}}")
            level += 1
            time.sleep(1)
            clear_screen()
        else:
            print(f"\\n{{Fore.RED}}Wrong!")
            print(f"{{Fore.WHITE}}Correct: {{' -> '.join(sequence)}}")
            print(f"{{Fore.YELLOW}}You reached level {{level}}")

            current_best = game_auth.get_user_high_scores(username, GAME_NAME).get("Highest Level", 0)
            if level > current_best:
                game_auth.update_user_high_score(username, GAME_NAME, "Highest Level", level)
                game_auth.update_leaderboard(username, GAME_NAME, "Highest Level", level, higher_is_better=True)
                print(f"{{Fore.GREEN}}NEW RECORD!")
            break
"""
        }
    ]
}


def create_project():
    category = random.choice(list(PROJECTS.keys()))
    project = random.choice(PROJECTS[category])

    game_name = project['name']

    full_code = GAME_AUTH_IMPORT.format(game_name=game_name)
    full_code += project['code']
    full_code += GAME_MENU_TEMPLATE

    today = datetime.now().strftime("%d-%m-%Y")
    filename = f"{game_name}_{today}.py"
    filepath = os.path.join(PROJECTS_DIR, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(full_code)

    log_file = os.path.join(os.path.dirname(__file__), "generation_log.txt")
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Created: {filename} (Category: {category})\n")

    print(f"\nCreated new project: {filename}")
    print(f"Category: {category}")
    print(f"Location: {filepath}")
    print(f"\nThis game uses the centralized game_auth system!")
    print(f"All user data will be saved in GameData folder.")


if __name__ == "__main__":
    create_project()
