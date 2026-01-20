""" Stack  - מחסנית
1.Last In - First Out
2.Only Works When the Stack is not empty
3.Always brings back the last item that entered
4.you can see only the top of the Stack
"""
class Stack:
    def __init__(self,size:int = 5):
        self.size = size
        self.top = -1
        self.data = [0] * self.size

    def push(self,var) -> bool:
        if not self.full():
            self.top += 1
            self.data[self.top] = var
            return True
        else:
            return False

    def pop(self):
        if not self.empty():
           val = self.data[self.top]
           self.top -= 1
           return val
        return None

    def peek(self):
        if not self.empty():
            return self.data[self.top]
        return None

    def empty(self):
        return self.top == -1

    def full(self):
        return ( self.size -1 ) == self.top

s1 = Stack()
s1.push("a")
s1.push("b")
print(s1.pop())
print(s1.__dict__)
