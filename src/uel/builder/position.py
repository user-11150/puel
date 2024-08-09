class Position:
    def __init__(self, line, column):
        self.line = self.lineno = line
        self.column = column

    def __str__(self):
        return f"({self.line}, {self.column})"

    def __repr__(self):
        return f"Position({self.line}, {self.column})"

    def __iter__(self):
        yield self.line
        yield self.column

    def __getitem__(self, s):
        return list(self)[s]
