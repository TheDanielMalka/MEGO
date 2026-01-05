def open_message() -> None:
    print("Welcome to DM TaskManager 2.0\n"
    "our commands :\n"
    "<add> to add a task to the calender\n"
    "<show> to show your current tasks\n"
    "<remove> to remove a task [goes by task number]\n"
    "<mark> to mark the task as done\n"
    "<clear> to clear your tasks\n"
    "<save> to save your task on the calendar\n"
    "<menu> to go back to the menu\n"
    "<exit> to quit")

class TaskManager:
    def __init__(self, name:str):
        self.tasks:list = []
        self.name = name

    def add_task(self, task:str) -> None:
        if task.strip() in self.tasks:
            print("You already have that task in your tasks")
            inp = input("Wanna add it again ? press 'y' to add again")
            if inp.lower() == "y":
                self.tasks.append(task.strip())
        else:
            self.tasks.append(task.strip())

    def show_tasks(self) -> None:
        if len(self.tasks) == 0:
            print("No Tasks on the callender")
        else:
            for index, task in enumerate(self.tasks, start=1):
                print(f"{index}. {task}")

    def remove_task(self, num:int) -> None:
        while True:
            if 1 <= num <= len(self.tasks):
                self.tasks.pop(num-1)
                print(f"Task {num} has been removed")
                break
            elif len(self.tasks) == 0:
                print("Your Task List is empty")
                break
            elif num == 999:
                self.tasks = []
            else:
                print("You entered an invalid task number try again")
                num = int(input("Enter your task num again"))

    def mark_done(self, num:int) -> None:
        while True:
            if 1 <= num <= len(self.tasks):
                temp = self.tasks[num-1]
                if self.tasks[-2:] != " V":
                    self.tasks[num-1] += " V"
                    print(f"Task {temp} has been marked")
                    break
            else:
                print("Invalid Task Number Try Again")
            num = int(input("Enter task num"))

    def clear_done_tasks(self):
        new_tasks = []
        for task in self.tasks:
            if task[-2:] != " V":
                new_tasks.append(task)
        self.tasks = new_tasks

    def save_to_file(self, file_path):
        st = open(file_path, 'w')
        for task in self.tasks:
            st.write(task +'\n')
        print(f"Data written to {file_path} successfully.")
        st.close()

    def load_from_file(self, file_path):
        uploaded_file = []
        curr = ""
        rt = open(file_path, 'r')
        readed = rt.read()
        for task in readed:
            if task != '\n':
                curr+=task
            if task == '\n':
                uploaded_file.append(curr)
                curr = ""
        if curr != "":
            uploaded_file.append(curr)
        for task in uploaded_file:
            if task not in self.tasks:
                self.tasks.append(task)
        rt.close()

task_section = input("Welcome! Enter your TaskManager section name \n")
NewTaskManager = TaskManager(task_section)
open_message()
user_input = input("Enter your choice \n")

while user_input.lower() != "exit":
    if user_input.lower() == "add":
        new_task = input("Enter your new task name \n")
        NewTaskManager.add_task(new_task)
        print(f"Task: {new_task} Added to the calendar")

    elif user_input.lower() == "menu":
        open_message()

    elif user_input.lower() == "show":
        NewTaskManager.show_tasks()

    elif user_input.lower() == "mark":
        print(f"Heres your tasks :\n")
        NewTaskManager.show_tasks()
        mark_the_task = int(input(f"Enter task number to be marked \n"))
        try:
            NewTaskManager.mark_done(mark_the_task)
        except ValueError:
            print("Must Enter Integer between")

    elif user_input.lower() == "remove":
        print(f"Heres your tasks :\n")
        NewTaskManager.show_tasks()
        remove_the_task = int(input(f"Enter task number to be removed or 999 to clear all \n"))
        try:
            NewTaskManager.remove_task(remove_the_task)
        except ValueError:
            print("Must Enter Integer between")

    elif user_input.lower() == "save":
        path = input("Enter your path to the file: \n")
        NewTaskManager.save_to_file(path)

    elif user_input.lower() == "load":
        path = input("Enter your path to the file: \n")
        NewTaskManager.load_from_file(path)
    user_input = input("Enter your choice \n")
print("GoodBye")