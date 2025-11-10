import random

min_cells = 10
max_cells = 30
coins_num = 4

def welcome_message () -> None:
    """"  פונקציה שמדפיסה הודעת פתיחה ראשונית """
    print("\n" + "=" * 50)
    print("WELCOME TO".center(50))
    print("Coin Game !".center(52))
    print("=" * 50)

def get_cellnum() -> int:
    """" פונקציה שמקבלת מספר בין 10 ל 30 והמספר הזה ייצג לי את גודל הלוח של המשחק"""
    global min_cells, max_cells
    cell_number = int(input("Please enter a cells number between 10 - 30 \n"
                            "(this cells will define the game board length): "))
    """"הוספתי פה בדיקת שגיאות למקרה המשתמש יכניס מספר מחוץ לטווח של המשימה"""
    while True:
        if max_cells >= cell_number >=  min_cells:
            return cell_number
        else:
            print("Number must be between 10-30")
            cell_number = int(input("Please enter a cell number: "))

def place_coins_rand(cellnum: int) -> list[int]:
    """"פונקציה שמקבלת את גודל הלוח ומחזירה רשימה בגודל 4
     עם מספר רנדומלי בין 0 לגודל הלוח """
    coins = random.sample(range(cellnum), 4) # כמו RANDINT רק בלי כפילויות כמו סט לרנדאינט פשוט
    coins.sort()
    """ אופציה להתחיל את המשחק שאין מיקום 0 ככה 4 מטבעות זזים אם אתה בחור """
    # if coins[0] == 0:
    #     coins[0] = random.randint(1,cellnum)
    return coins

def draw_board(coins: list[int], cellnum: int) -> None:
    for i in range(cellnum):
        if i in coins:
            print("[C]", end=" ")
        else:
            print("[ ]", end=" ")
    print()

def gameover(coins: list[int]) -> bool:
    for i in range(len(coins)):
        if coins[i] > 0:
            if i == 0:
                return False
            elif coins[i] - coins[i - 1] > 1:
                return False
    return True

def make_move(coins: list[int], player: int) -> None:
    while True:
        coin = int(input(f"Player {player}, pick coin (1-4 from left to right): "))
        move = int(input("Steps left: "))
        coin_index = coins[coin-1]
        new_index = coin_index - move
        valid = True
        if new_index < 0:
            print("your out of range")
            continue
        if new_index in coins:
            print("you got a coin there")
            continue
        for check in coins:
            if new_index < check < coin_index: # 7 < check < 11
                valid = False
                break
        if not valid:
            print("cant pass coin")
            continue
        coins[coin-1] = new_index
        coins.sort()
        break

def game_summary(player: int) -> None:
    print(f"well done player {player} has won!!")

def draw_line(length: int) -> None:
        print("-" * length * 4)

def main():
    player_number = 1
    welcome_message()
    cellnums = get_cellnum()
    picked_coins = place_coins_rand(cellnums)
    draw_board(picked_coins, cellnums)
    draw_line(cellnums)
    print("Heres your starting board ! Good Luck!".center(50))
    while not gameover(picked_coins):
        make_move(picked_coins, player_number)
        draw_board(picked_coins, cellnums)
        draw_line(cellnums)
        player_number = 3 - player_number
    game_summary(3 - player_number)
main()