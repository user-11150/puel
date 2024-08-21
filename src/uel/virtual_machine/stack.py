class Stack:
    def __init__(self):
        self.values = []

    def push(self, value):
        self.values.append(value)

    def top(self):
        return self.value[-1]

    def pop(self):
        return self.values.pop()
