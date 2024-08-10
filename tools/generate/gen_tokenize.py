from generate import task, python
import textwrap
import copy
import os
import ast
import linecache

SCRIPT_NAME = "tools/generate/gen_tokenize.py"
FROM = "grammer/tokens"
DESCRIPTION = """
UEL's tokenizer
"""

class GenerateTokenizer:
    
    
    def __init__(self, dirname):
        self.result = ""
        self.dirname = dirname
        token_declarations = linecache.getlines(os.path.join(dirname, "grammer/tokens"))
        self.tokens = {}
        for declaration in token_declarations:
            if not declaration:
                continue
            tok = declaration.split(" ", 1)
            tok[0] = tok[0].strip()
            if len(tok) != 1:
                self.tokens[f"TT_{tok[0]}"] = tok[1]
            else:
                self.tokens[f"TT_{tok[0]}"] = None
    
    def add_global_imports(self):
        self.result += textwrap.dedent(
        """
        from uel.internal.uelcore_internal_exceptions import throw
        from uel.exceptions import UELSyntaxError, uel_set_error_string
        from uel.builder.codeobject import UELCode
        from uel.builder.token import UELToken
        from uel.builder.position import Position
        import typing as t
        """
        )
    
    def add_global_consts(self):
        from string import ascii_letters
        self.result += textwrap.dedent(
        f"""
        numbers = {repr("".join(map(str, range(10))))}
        ascii_letters = {repr(ascii_letters)}
        """
        )
    
    def add_implement(self):
        template = textwrap.dedent(
        """
        class UELTokenize:
            def __init__(self, source: t.Any) -> None:
                self.source = source
                self.current_idx = 0
        
            @property
            def current_char(self) -> str:
                return self.peek(0)
            
            def peek(self, relative):
                try:
                    return self.source[self.current_idx + relative]
                except IndexError:
                    return None
        
            def advance(self) -> str:
                self.current_idx += 1
                return self.current_char
        
            def rollback(self) -> str:
                self.current_idx -= 1
                return self.current_char
        
            def idx_as_position(self, idx):
                return UELToken.idx_as_position(self.source, idx)
        
            @property
            def current_position(self):
                return self.idx_as_position(self.current_idx)
        
            def make_tokens(self) -> list[UELToken]:
                tokens = []
                while self.current_char is not None:
        
                    start_position = self.current_position
        
        %s
                    if self.current_char is None:
                        break
                tokens.append(UELToken(Token.TT_EOF, None, None, None))
        
                return tokens
        
            @staticmethod
            def is_identifier_start(char_):
                if char_ in ascii_letters:
                    return True
                if '\u4e00' <= char_ <= '\u9fff':
                    return True
                if char_ in ["_", "$"]:
                    return True
                return False
        
            @classmethod
            def is_identifier(cls, char_):
                return cls.is_identifier_start(char_) or char_ in numbers
        
            def make_identifier(self):
                result = ""
        
                while True:
                    if self.current_char is None:
                        break
                    if self.is_identifier(self.current_char):
                        result += self.current_char
                        self.advance()
                    else:
                        break
        
                self.rollback()
                return result
        """
        )
        
        self.result += template % textwrap.indent(self.generate_cases(), "    " * 3)
     
    def generate_normal_cases(self, items):
        for key, value in sorted(items.items(), key=lambda x: len(ast.literal_eval(x[1])), reverse=True):
            assert value is not None, key
            txt = ast.literal_eval(value)
            cond = " and ".join(map(lambda item: f"self.peek({item[0]}) == {repr(item[1])}", enumerate(txt)))
            cond = cond.replace("self.peek(0)", "self.current_char")
            body = ""
            body += "self.advance()\n" * len(txt)
            body += textwrap.dedent(
                f"""
                tokens.append(
                    UELToken(
                        {key}, {repr(txt)}, start_position, self.current_position
                    )
                )
                """
            )
            
            yield key, (cond, body)
 
    def generate_cases(self):
        numbers = "".join(map(str, range(10)))
        special_cases = {
            "TT_IDENTIFIER": ("self.is_identifier_start(self.current_char)",
            textwrap.dedent(
                """
                identifier = self.make_identifier()
                token_type = TT_KEYWORD if identifier in TT_KEYWORDS else TT_IDENTIFIER
                tokens.append(
                    UELToken(
                        token_type, identifier, start_position, self.current_position
                    )
                )
                self.advance()
                """)),
            "TT_STRING": ("self.current_char in ['\"', '\\'']",
            textwrap.dedent(
                """
                start = self.current_char
                res = ""
                while True:
                    self.advance()
                    if self.current_char == "\\\\":
                        self.advance()
                        if self.current_char == start:
                            res += start
                        
                        else:
                            uel_set_error_string(UELSyntaxError, "Anomalous backlash in string", self.source, self.current_position)
                        continue
                    if self.current_char == start:
                        self.advance()
                        break
                    if self.current_char is None:
                        uel_set_error_string(UELSyntaxError, "unterminated string literal", self.source, self.current_position)
                    res += self.current_char
                tokens.append(
                    UELToken(
                        TT_STRING, res, start_position, self.current_position
                    )
                )
                self.advance()
                """
            )),
            "TT_NUMBER": (f"self.current_char in {repr(numbers)}", textwrap.dedent(
                fr"""
                result = ""
                while self.current_char is not None and self.current_char in {repr(numbers + ".")}:
                    if "." in result and self.current_char == ".":
                        uel_set_error_string(UELSyntaxError, "Too many dots", self.source, self.current_position)
                    result += self.current_char
                    self.advance()
                tokens.append(
                    UELToken(
                        TT_NUMBER, result, start_position, self.current_position
                    )
                )
                """
            ))
        
        }
        result = textwrap.dedent(
            """
            if self.current_char == " " or self.current_char == "\\n":
                self.advance()
                continue
            elif self.current_char == "#":
                while self.advance() not in [None, "\\n"]:
                    pass
            
            """
        )
        items = sorted(self.tokens.items(), key=lambda x: x[0])
        
        options = copy.deepcopy(self.tokens)
        
        tmp = {}
        for key, value in special_cases.items():
            options.pop(key)
            tmp[key] = tmp.get(key) or [None, None]
            tmp[key][0] = value[0]
            tmp[key][1] = value[1]
        tmp2 = map(lambda x: x[1], self.generate_normal_cases(options))
        for cond, body in tmp2:
            result += f"""\nelif {cond}:\n{textwrap.indent(body, "    ")}"""
        for cond, body in tmp.values():
            result += f"""\nelif {cond}:\n{textwrap.indent(body, "    ")}"""
        result += "\n"
        result += textwrap.dedent(
            """
            else:
                uel_set_error_string(UELSyntaxError, "Invalid character", self.source, self.current_position)
            """)
        return result
    
    def add_token_types(self):
        tmp = "\n".join(map(lambda x: f"{x} = {repr(x)}", self.tokens.keys()))
        keywords = [
            "import"
        ]
        extras = f"TT_KEYWORDS = {repr(keywords)};" \
                 "TT_KEYWORD = 'TT_KEYWORD';" \
                 "TT_EOF = 'TT_EOF'"
        tmp += f"\n{extras}"
        
        self.result += tmp
        self.result += "\nclass Token:\n" + textwrap.indent(tmp, "    ")
    
    def add_interface(self):
        self.result += textwrap.dedent(
        """
        def uel_generate_tokens(source: str) -> list[UELToken]:
            return UELTokenize(source).make_tokens()
        """)
    
    
    
    def generate(self):
        self.add_global_imports()
        self.add_global_consts()
        
        self.add_token_types()
        
        self.add_implement()
        
        self.add_interface()
        
        return self.result

@task("src/uel/builder/tokenize.py")
@python(SCRIPT_NAME, FROM, DESCRIPTION)
def generate_tokenizer(dirname):
    result = ""
    result += GenerateTokenizer(dirname).generate()
    return result
