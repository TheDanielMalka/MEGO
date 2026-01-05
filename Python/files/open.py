class Opens:

    def __init__(self,path):
        self.path = path

    def opening(self):
        print(f"Welcome to {MyFile.path}\n"
              f"For <read> type read\n"
              f"For <write> type write\n"
              f"For <append> type append\n"
              f"For <clear> type clear\n"
              f"For <exit> type exit\n"
              f"For <copy> type copy\n")

    def write(self,text):
        st = open(self.path,'w')
        st.write(text)
        print(f"Data written to {self.path} successfully.")
        st.close()

    def read(self):
        st = open(self.path,'r')
        readed = st.read()
        st.close()
        return readed

    def append(self,text):
        st = open(self.path,'a')
        print(f"Data Appended successfully.")
        st.write(text+'\n')
        st.close()

    def clear(self):
        op = open(self.path, 'r')
        self.read()
        clear_ensure = input("Do you want to clear the data? (y/n): ")
        if clear_ensure == 'y':
            st = open(self.path,'w')
            st.write('')
            print("Your file data now erased")
            st.close()
        else:
            op.close()

    def count_lines(self):
        st = open(self.path, 'r')
        lines = st.readlines()
        st.close()
        return len(lines)

    def copy(self,user_path,copy_path):
        st = open(user_path, 'r')
        copied = st.read()
        st.close()

        st = open(copy_path, 'w')
        st.write(copied)
        print(f"Data copied to {copy_path} successfully.")
        st.close()

counter = 0
MyFile = Opens("C:/Users/shimo/MEGO/Python/files/dat1.txt")
MyFile.opening()
user_inpt = input("Enter your request: ")

while True:
        if user_inpt == "exit":
            print("Exiting program.")
            break

        elif user_inpt == "clear":
            MyFile.clear()

        elif user_inpt == "append":
            user_data = input("Enter your Data: ")
            counter += 1
            print(f"You Appended {counter} lines so far")
            MyFile.append(user_data)

        elif user_inpt == "write":
            user_data = input("Enter your Data: ")
            MyFile.write(user_data)

        elif user_inpt == "read":
            print(MyFile.read())

        elif user_inpt == "5 lines":
            new_file = input("Enter your path: ")
            MyNewFile = Opens(new_file)
            inp = input(f"Enter your data:")+'\n'
            MyNewFile.write(inp)
            for i in range(4):
                inp = input("Enter your Next Data: ")
                MyNewFile.append(inp)
            line_count = MyNewFile.count_lines()
            print(f"{line_count} lines added so far")

        elif user_inpt == "copy":
                user_path = input("Enter your path: ")
                copy_path = input("Enter your new path: ")
                MyFile.copy(user_path,copy_path)

        elif user_inpt == "check":
            upperCases = 0
            lowerCases = 0
            digits = 0
            specials = 0
            MyFile2 = Opens("C:/Users/shimo/MEGO/Python/files/dat2.txt")
            check = MyFile2.read()
            for char in check:
                    if "a" <= char <= "z":
                        lowerCases += 1
                    elif "A" <= char <= "Z":
                        upperCases += 1
                    elif "1" <= char <= "9":
                        digits += 1
                    else:
                        specials += 1
            print(f"{lowerCases} lowercase letters added\n "
                  f"{upperCases} uppercase letters added\n "
                  f"{digits} digits added\n "
                  f"{specials} special characters added")

        elif user_inpt == "repeat":
            MyFile2 = Opens("C:/Users/shimo/MEGO/Python/files/dat2.txt")
            file = MyFile2.read()
            while True:
                repeat_counter = 0
                check = input("Write a char")
                for char in file:
                    if check == char:
                        repeat_counter += 1
                print(f"{repeat_counter} your char appears in the file")
                again = input("Write again? (y/n): ")
                if again == 'y':
                    continue
                else:
                    break

        elif user_inpt == "50int":
            MyFile5 = Opens("C:/Users/shimo/MEGO/Python/files/dat5.txt")
            ints = ''
            for i in range(5):
                inp = input("Enter your Ints: ")
                ints += inp + ' '
            MyFile5.write(ints)
            readed_ints = MyFile5.read().split()
            biggest = int(readed_ints[0])
            smallest = int(readed_ints[0])
            biggest_appeared = 0
            smallest_appeared = 0
            for integer in readed_ints:
                if int(integer) > biggest:
                    biggest = int(integer)
                elif int(integer) < smallest:
                    smallest = int(integer)
            for i in readed_ints:
                if int(i) == biggest:
                    biggest_appeared += 1
                if int(i) == smallest:
                    smallest_appeared += 1
            print(f"Biggest integer is {biggest} appeared {biggest_appeared} times. \n"
                  f"Smallest integer is {smallest} appeared {smallest_appeared} times. ")


        else:
            print("Invalid input.")

        MyFile.opening()
        user_inpt = input("Enter your request: ")
    except KeyboardInterrupt:
        print("Try Again.")
    except ValueError:
        print("Invalid input.")