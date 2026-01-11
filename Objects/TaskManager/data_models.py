from datetime import datetime

class TaskAttributes:
    def __init__(self,task_name:str,priority:int,category:str,created_at:str=None):
        self.priority = priority
        self.task_name = task_name
        self.category = category
        if created_at:
            self.created_at = created_at
        else:
            self.created_at = datetime.now().strftime("%d/%m/%Y %H:%M")


def priority_analyze(input_list:list) -> int:
    priority_5 = ["crit", "urgent", "now", "asap", "immediate", "emergency", "deadly", "top", "burning", "instant"]
    priority_4 = ["please", "fast", "important", "soon", "priority", "quickly", "today", "must", "serious", "needed"]
    priority_3 = ["can", "normal", "regular", "standard", "maybe", "weekly", "routine", "usual", "next", "planning"]
    priority_2 = ["later", "someday", "slow", "whenever", "chill", "eventually", "backup", "secondary", "optional", "extra"]
    priority_1 = ["low", "future", "free", "spare", "ignore", "minor", "background", "trivial", "minimal", "easy"]
    for word in priority_5:
        if word in input_list:
            input_list.remove(word)
            return 5
    for word in priority_4:
        if word in input_list:
            input_list.remove(word)
            return 4
    for word in priority_3:
        if word in input_list:
            input_list.remove(word)
            return 3
    for word in priority_2:
        if word in input_list:
            input_list.remove(word)
            return 2
    for word in priority_1:
        if word in input_list:
            input_list.remove(word)
            return 1
    return 0

def category_analyze(input_list:list) -> str:
    categories = {
        "Work": ["office", "boss", "mail", "meeting", "project", "report", "salary", "client", "work", "job"],
        "Study": ["python", "exam", "math", "learn", "book", "university", "course", "homework", "test", "science"],
        "Home": ["clean", "cook", "buy", "laundry", "dishes", "fix", "rent", "garden", "home", "family"],
        "Health": ["gym", "doctor", "workout", "sport", "medicine", "dentist", "run", "water", "sleep", "healthy"],
        "Fun": ["movie", "game", "party", "trip", "beer", "friends", "vacation", "music", "hobby", "rest"]
    }
    for key, sections in categories.items():
        for section in sections:
            if section in input_list:
                input_list.remove(section)
                return key
    return "General"

def build_task(inp):
    word = inp.lower().split()
    priority = priority_analyze(word)
    category = category_analyze(word)
    new_word = " ".join(word)
    task = TaskAttributes(new_word,priority,category)
    return task

