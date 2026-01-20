import os
import json
import hashlib
import time
from colorama import Fore

DATA_DIR = os.path.dirname(__file__)
LEADERBOARD_FILE = os.path.join(DATA_DIR, "all_games_leaderboard.json")


def get_users_file(game_name):
    return os.path.join(DATA_DIR, f"{game_name}_users.json")


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def load_users(game_name):
    users_file = get_users_file(game_name)
    if not os.path.exists(users_file):
        return {}
    with open(users_file, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except:
            return {}


def save_users(game_name, users):
    users_file = get_users_file(game_name)
    with open(users_file, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=2, ensure_ascii=False)


def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return {}
    with open(LEADERBOARD_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except:
            return {}


def save_leaderboard(leaderboard):
    with open(LEADERBOARD_FILE, 'w', encoding='utf-8') as f:
        json.dump(leaderboard, f, indent=2, ensure_ascii=False)


def register_user(game_name):
    print(f"\n{Fore.GREEN}{'='*50}")
    print(f"{Fore.GREEN}USER REGISTRATION")
    print(f"{Fore.GREEN}{'='*50}")

    users = load_users(game_name)

    while True:
        username = input(f"\n{Fore.WHITE}Enter username: ").strip()
        if not username:
            print(f"{Fore.RED}Username cannot be empty!")
            continue
        if username in users:
            print(f"{Fore.RED}Username already exists in {game_name}!")
            continue
        break

    password = input(f"{Fore.WHITE}Enter password: ").strip()
    if not password:
        print(f"{Fore.RED}Password cannot be empty!")
        return None

    users[username] = {
        "password": hash_password(password),
        "stats": {},
        "high_scores": {}
    }

    save_users(game_name, users)
    print(f"\n{Fore.GREEN}User registered successfully!")
    time.sleep(1)
    return username


def login_user(game_name):
    print(f"\n{Fore.CYAN}{'='*50}")
    print(f"{Fore.CYAN}USER LOGIN")
    print(f"{Fore.CYAN}{'='*50}")

    users = load_users(game_name)

    if not users:
        print(f"\n{Fore.YELLOW}No users registered yet in {game_name}!")
        time.sleep(1)
        return None

    username = input(f"\n{Fore.WHITE}Username: ").strip()
    password = input(f"{Fore.WHITE}Password: ").strip()

    if username not in users:
        print(f"\n{Fore.RED}User not found in {game_name}!")
        time.sleep(1)
        return None

    if users[username]["password"] != hash_password(password):
        print(f"\n{Fore.RED}Wrong password!")
        time.sleep(1)
        return None

    print(f"\n{Fore.GREEN}Welcome back, {username}!")
    time.sleep(1)
    return username


def user_authentication(game_name, clear_func):
    while True:
        clear_func()
        print(f"\n{Fore.YELLOW}{'='*50}")
        print(f"{Fore.YELLOW}{game_name} - AUTHENTICATION")
        print(f"{Fore.YELLOW}{'='*50}")
        print(f"\n{Fore.WHITE}1. Login")
        print(f"{Fore.WHITE}2. Register")
        print(f"{Fore.WHITE}3. View All Games Leaderboard")
        print(f"{Fore.WHITE}4. Exit")

        choice = input(f"\n{Fore.WHITE}Choose (1-4): ")

        if choice == '1':
            username = login_user(game_name)
            if username:
                return username
        elif choice == '2':
            username = register_user(game_name)
            if username:
                return username
        elif choice == '3':
            display_all_leaderboards()
            input(f"\n{Fore.WHITE}Press ENTER to continue...")
        elif choice == '4':
            return None
        else:
            print(f"{Fore.RED}Invalid choice!")
            time.sleep(1)


def update_user_stats(username, game_name, stats_data):
    users = load_users(game_name)
    if username not in users:
        return

    if "stats" not in users[username]:
        users[username]["stats"] = {}

    users[username]["stats"].update(stats_data)
    save_users(game_name, users)


def get_user_stats(username, game_name):
    users = load_users(game_name)
    if username not in users:
        return {}

    return users[username].get("stats", {})


def update_user_high_score(username, game_name, category, score):
    users = load_users(game_name)
    if username not in users:
        return False

    if "high_scores" not in users[username]:
        users[username]["high_scores"] = {}

    if category not in users[username]["high_scores"] or score > users[username]["high_scores"][category]:
        users[username]["high_scores"][category] = score
        save_users(game_name, users)
        return True

    return False


def get_user_high_scores(username, game_name):
    users = load_users(game_name)
    if username not in users:
        return {}

    return users[username].get("high_scores", {})


def update_leaderboard(username, game_name, category, score, higher_is_better=True):
    leaderboard = load_leaderboard()

    if game_name not in leaderboard:
        leaderboard[game_name] = {}

    if category not in leaderboard[game_name]:
        leaderboard[game_name][category] = []

    user_entry = next((entry for entry in leaderboard[game_name][category] if entry["username"] == username), None)

    if user_entry:
        if higher_is_better:
            if score > user_entry["score"]:
                user_entry["score"] = score
        else:
            if score < user_entry["score"]:
                user_entry["score"] = score
    else:
        leaderboard[game_name][category].append({"username": username, "score": score})

    leaderboard[game_name][category].sort(key=lambda x: x["score"], reverse=higher_is_better)

    save_leaderboard(leaderboard)


def display_game_leaderboard(game_name, category_name=None):
    leaderboard = load_leaderboard()

    if game_name not in leaderboard:
        print(f"{Fore.YELLOW}No scores yet for {game_name}!")
        return

    print(f"\n{Fore.YELLOW}{'='*50}")
    print(f"{Fore.YELLOW}{game_name.upper()} LEADERBOARD")
    print(f"{Fore.YELLOW}{'='*50}")

    game_data = leaderboard[game_name]

    if category_name:
        if category_name in game_data:
            print(f"\n{Fore.MAGENTA}{category_name}:")
            for i, entry in enumerate(game_data[category_name][:10], 1):
                rank_color = Fore.GREEN if i == 1 else Fore.CYAN if i <= 3 else Fore.WHITE
                print(f"  {rank_color}{i}. {entry['username']}: {entry['score']}")
        else:
            print(f"{Fore.YELLOW}No scores yet for {category_name}!")
    else:
        for category, scores in game_data.items():
            print(f"\n{Fore.MAGENTA}{category}:")
            for i, entry in enumerate(scores[:10], 1):
                rank_color = Fore.GREEN if i == 1 else Fore.CYAN if i <= 3 else Fore.WHITE
                print(f"  {rank_color}{i}. {entry['username']}: {entry['score']}")


def display_all_leaderboards():
    leaderboard = load_leaderboard()

    print(f"\n{Fore.YELLOW}{'='*60}")
    print(f"{Fore.YELLOW}ALL GAMES LEADERBOARD")
    print(f"{Fore.YELLOW}{'='*60}")

    if not leaderboard:
        print(f"{Fore.YELLOW}No scores yet!")
        return

    for game_name, game_data in leaderboard.items():
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}{game_name.upper()}")
        print(f"{Fore.CYAN}{'='*60}")

        for category, scores in game_data.items():
            print(f"\n{Fore.MAGENTA}  {category}:")
            for i, entry in enumerate(scores[:5], 1):
                rank_color = Fore.GREEN if i == 1 else Fore.CYAN if i <= 3 else Fore.WHITE
                print(f"    {rank_color}{i}. {entry['username']}: {entry['score']}")


def display_user_stats(username, game_name):
    stats = get_user_stats(username, game_name)

    if not stats:
        print(f"\n{Fore.YELLOW}No stats yet for {game_name}!")
        return

    print(f"\n{Fore.CYAN}{'='*50}")
    print(f"{Fore.CYAN}YOUR {game_name.upper()} STATS")
    print(f"{Fore.CYAN}{'='*50}")

    for key, value in stats.items():
        if isinstance(value, dict):
            print(f"\n{Fore.MAGENTA}{key}:")
            for sub_key, sub_value in value.items():
                print(f"  {Fore.WHITE}{sub_key}: {sub_value}")
        else:
            print(f"{Fore.WHITE}{key}: {value}")


def display_user_high_scores(username, game_name):
    high_scores = get_user_high_scores(username, game_name)

    print(f"\n{Fore.YELLOW}{'='*50}")
    print(f"{Fore.YELLOW}YOUR {game_name.upper()} HIGH SCORES")
    print(f"{Fore.YELLOW}{'='*50}")

    if not high_scores:
        print(f"{Fore.YELLOW}No high scores yet!")
    else:
        for category, score in high_scores.items():
            print(f"{Fore.GREEN}{category}: {score}")
