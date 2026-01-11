import data_models as dm

class TaskManager:
    def __init__(self):
        self.tasks:list = []

    def open_message(self) -> None:

        """" This function is a main menu function """

        print("Welcome to DM TaskManager 2.0\n"
              "our commands :\n"
              "<show> to show your current tasks\n"
              "<add> to add a task to the calender\n"
              "<remove> to remove a task [goes by task number]\n"
              "<edit> to edit a task name\n"
              "<mark> to mark the task as done\n"
              "<clear> to clear your done tasks\n"
              "<save> to save your task on the calendar\n"
              "<menu> to go back to the menu\n"
              "<exit> to quit")

    def show_tasks(self) -> None:

        """This function shows the tasks that exist in you calendar"""

        if len(self.tasks) == 0:
            print("No Tasks on the calendar")
        else:
            for i, task in enumerate(self.tasks, 1):
                print(f"{i}. {task.task_name} | Priority: {task.priority} | Category: {task.category} | Created: {task.created_at}")

    def add_task(self, task:object) -> None:

        """This function is adding a single task each time you execute her"""
        existing_list = []
        for t in self.tasks:
            existing_list.append(t.task_name)
        if task.task_name in existing_list:
            print("You already have that task in your tasks")
            inp = input("Wanna add it again? press 'y' to add again: ")
            if inp.lower() == "y":
                self.tasks.append(task)
        else:
            self.tasks.append(task)

    def edit_task(self, num: int, new_name: str) -> None:

        """This function edits the name of an existing task"""

        if 1 <= num <= len(self.tasks):
            old_name = self.tasks[num - 1].task_name
            self.tasks[num - 1].task_name = new_name
            print(f"Task {num} changed from '{old_name}' to '{new_name}'")
        else:
            print("Invalid task number. Edit failed.")

    def remove_task(self, num:int) -> None:

        """This function remove a single task every time you execute her"""

        if not self.tasks:
            print("Your Task List is empty")

        elif 1 <= num <= len(self.tasks):
            removed = self.tasks.pop(num - 1)
            print(f"Task '{removed.task_name}' has been removed")

        else:
            print("Invalid task number")

    def mark_done(self, num:int) -> None:

        """This func marking a single task as done with a ✅ """

        while True:
            if 1 <= num <= len(self.tasks):
                temp = self.tasks[num-1]
                if "✅" not in temp.task_name:
                    print(f"Task: ({temp.task_name}) has been marked")
                    temp.task_name += "✅"
                    break
            else:
                print("Invalid Task Number Try Again")
            again = input("You entered invalid task number you wanna try again? ( y / n )")
            if again.lower() == "y":
                num = int(input("Enter task num"))
            else:
                break

    def clear_done_tasks(self) -> None:

        """This function clears all of your tasks from the calandar"""

        new_tasks = []
        for task in self.tasks:
            if "✅" not in task.task_name:
                new_tasks.append(task)
        self.tasks = new_tasks

    def save_to_file(self, file_path):

        """This function is writing your calandar into a '.txt' file """

        st = open(file_path, 'w', encoding='utf-8')
        for task in self.tasks:
            line = f"{task.task_name}|{task.priority}|{task.category}|{task.created_at}\n"
            st.write(line)
        print(f"Data written to {file_path} successfully.")
        st.close()

    def load_from_file(self,file_path):

        """This function is loading an existing calandar from a txt file """
        try:
            line = []
            lines = []
            curr = ""
            rt = open(file_path, 'r', encoding='utf-8')
            readed = rt.read()
            rt.close()
            for char in readed:
                if char == "|":
                    line.append(curr)
                    curr = ""
                elif char == "\n":
                    line.append(curr)
                    lines.append(line)
                    line = []
                    curr = ""
                else:
                    curr += char
            for task in lines:
                if len(task) == 4:
                    task_name = task[0]
                    priority = int(task[1])
                    category = task[2]
                    time = task[3]
                    new_task_obj = dm.TaskAttributes(task_name, priority, category,time)
                    exists = False
                    for existing_task in self.tasks:
                        if existing_task.task_name == task_name:
                            exists = True
                            break
                    if not exists:
                        self.tasks.append(new_task_obj)
        except FileNotFoundError:
            print("Your calendar is empty")


TaskManagerBank = TaskManager()
TaskManagerBank.load_from_file("./TaskManager.txt")
TaskManagerBank.open_message()
user_input = input("Enter your choice \n")

if __name__ == "__main__":
    while user_input.lower() != "exit":

        if user_input.lower() == "menu":
            TaskManager.open_message()

        elif user_input.lower() == "show":
            TaskManagerBank.show_tasks()

        elif user_input.lower() == "add":
            new_task = input("Enter your new task name \n")
            task_obj = dm.build_task(new_task)
            TaskManagerBank.add_task(task_obj)
            print(f"Task: '{task_obj.task_name}' Added! [Priority: {task_obj.priority}, Category: {task_obj.category}]")

        elif user_input.lower() == "edit":
            print(f"Heres your tasks :\n")
            TaskManagerBank.show_tasks()
            try:
                task_num = int(input("Enter task number to edit: "))
                if 1 <= task_num <= len(TaskManagerBank.tasks):
                    new_name = input("Enter the new name for the task: ")
                    TaskManagerBank.edit_task(task_num, new_name)
                else:
                    print("Invalid task number")
            except ValueError:
                print("You must enter a valid number")

        elif user_input.lower() == "mark":
            print(f"Heres your tasks :\n")
            TaskManagerBank.show_tasks()
            try:
                mark_the_task = int(input(f"Enter task number to be marked \n"))
                TaskManagerBank.mark_done(mark_the_task)
            except ValueError:
                print("You must enter a valid number")

        elif user_input.lower() == "remove":
            print(f"Heres your tasks :\n")
            TaskManagerBank.show_tasks()
            try:
                remove_the_task = int(input(f"Enter task number to be removed \n"))
                TaskManagerBank.remove_task(remove_the_task)
            except ValueError:
                print("You must enter a valid number")

        elif user_input.lower() == "clear":
            TaskManagerBank.clear_done_tasks()
            print("Done tasks have been cleared.")

        elif user_input.lower() == "save":
            TaskManagerBank.save_to_file('./TaskManager.txt')

        user_input = input("Enter your choice \n")
    print("GoodBye")
