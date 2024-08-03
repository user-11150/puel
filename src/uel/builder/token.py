import typing as t


class UELToken:
    def __init__(
        self,
        token_type: str,  # Token's Type
        token_value: str,  # token value
        start_line: int,  # Token's start line
        start_col: int,  # Token's start col
        end_line: int,  # Token's end line
        end_col: int  # Token's end col
    ):
        self.token_type = token_type
        self.token_value = token_value
        self.start_line = start_line
        self.start_col = start_col
        self.end_line = end_line
        self.end_col = end_col

    def __repr__(self) -> str:
        pos = f"start_col={self.start_col}, end_line={self.end_line}, end_col={self.end_col}"
        return f"UELToken(token_type={self.token_type}, token_value={repr(self.token_value)}, start_line={self.start_line}, {pos})"

    @staticmethod
    def idx_as_line_and_col(
        source: str, idx: int
    ) -> tuple[t.Union[int, None], t.Union[int, None]]:
        line = 1
        col = 1

        if len(source) <= idx:
            return None, None

        for i in range(idx):
            if source[i] == "\n":
                line += 1
                col = 1
            else:
                col += 1
        return line, col
