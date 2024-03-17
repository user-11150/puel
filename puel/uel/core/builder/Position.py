class Position:
    def __init__(self, idx, ln, col, fn, text):
        """
        :param idx: 索引下标
        :param ln: 行号(line)
        :param col: 列号(column)
        :param fn: 文件名(file name) ,报错用
        :param text: 内容文本
        :return:
        """
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.text = text

    def advance(self, current_char) -> None:
        """
        预读取下一个字符, 配合 Lexer 类进行使用
        :param current_char:
        :return:
        """
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.col = 0
            self.ln += 1

    def copy(self):
        """
        深拷贝
        :return: 一个深拷贝的 Position 对象
        """
        return Position(self.idx, self.ln, self.col, self.fn, self.text)
