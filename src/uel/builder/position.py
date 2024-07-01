from typing import Any, overload, final

__all__ = ["Position"]


class Position:
    def __new__(cls, *args, **kwargs) -> "Position":
        if args == () and kwargs == {}:
            return  # type: ignore
        return object.__new__(cls)

    @overload
    def __init__(self):
        ...

    @overload
    def __init__(self, idx: int, ln: int, col: int, fn: str, text: str):
        ...

    @final
    def __init__(self, *args):
        """
        :param idx: 索引下标
        :param ln: 行号(line)
        :param col: 列号(column)
        :param fn: 文件名(file name) ,报错用
        :param text: 内容文本
        :return:
        """
        idx, ln, col, fn, text = args
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.text = text

    def advance(self, current_char: str | None) -> None:
        """
        预读取下一个字符, 配合 Lexer 类进行使用
        :param current_char:
        :return:
        """
        if current_char is None:
            return
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.col = 0
            self.ln += 1

    def copy(self) -> "Position":
        """
        深拷贝
        :return: 一个深拷贝的 Position 对象
        """
        return Position(self.idx, self.ln, self.col, self.fn, self.text)
