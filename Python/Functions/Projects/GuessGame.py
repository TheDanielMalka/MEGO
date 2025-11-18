import random

random_num = random.randint(1,100)
counter = 0
tried = []
while True:
        try_input = int(input(f"Guess the number between 1-100\n>>>"))
        if counter == 10:
            print(f"{try_input} Is Incorrect!\nYou Maxxed your tries\nGame Over!")
            break
        if try_input <= 100:
            try:
                if random_num < try_input and try_input not in tried:
                    print(f"You Entered {try_input} - Too High! Try Again")
                    tried.append(try_input)
                    counter += 1

                elif try_input < random_num and try_input not in tried:
                    print(f"You Entered {try_input} - Too Low! Try Again")
                    tried.append(try_input)
                    counter += 1

                elif try_input in tried:
                    print(f"You Entered {try_input} Already Try again!")

                else:
                    print(f"{try_input} Is Correct!\nYou Win with {counter} Tries!")
                    break
                if len(tried) > 0:
                    print(f"Guessed Numbers: {tried}")
            except ValueError:
                print("Sorry must enter an integer")
        else:
            print("number must be between 1 and 100")


