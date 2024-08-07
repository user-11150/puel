from uel.builder.position import Position


class UELToken:
    def __init__(
        self, token_type: str, token_value: str, start: Position,
        end: Position
    ):
        self.token_type = token_type
        self.token_value = token_value
        self.start = start
        self.end = end

    def __repr__(self) -> str:
        return "UELToken(" \
               f"token_type={self.token_type}, " \
               f"token_value={repr(self.token_value)}, " \
               f"start={self.start}, " \
               f"end={self.end}" \
               ")"

    def __str__(self):
        return f"{self.token_type} " \
               f"{repr(self.token_value)} " \
               f"{self.start}-{self.end})"

    @staticmethod
    def idx_as_position(source: str, idx: int) -> Position | None:
        line = 1
        col = 1

        if len(source) <= idx:
            return None

        for i in range(idx):
            if source[i] == "\n":
                line += 1
                col = 1
            else:
                col += 1
        return Position(line, col)
