import re
import abc

class BaseMatcher(metaclass=abc.ABCMeta):
    def __init__(self,val):
        self.val = val

    @abc.abstractmethod
    def matcher(self):
        pass

class CreateVariableSyntaxMatcher(BaseMatcher):
    def matcher(self):
        if match := re.fullmatch("var (.+)=(.+);?",self.val):
            self.result = match.group(1) + "=" + match.group(2)
            return self

class FunctionCallSyntaxMatcher(BaseMatcher):
    def matcher(self):
        if match := re.fullmatch(r"(.+) -> Call -> \((.*)\);?", self.val):
            self.result = match.group(1) + f"({match.group(2)})"
            return self

# 匹配所有语法的分析器，每一个分析器都含有一个方法
# `matcher`，用于判断是否符合这种语法，如果符合，
# 将会得到一个result，以便于后续的去操作。

syntaxs = [CreateVariableSyntaxMatcher,
           FunctionCallSyntaxMatcher]

class ParserLine:
    def __init__(self,line,line_index):
        self.line = line
        self.line_index = line_index
        
    def parser_line(self):
        for syn in syntaxs:
            tmp = syn(self.line).matcher()
            if tmp is not None:
                self.result = tmp.result
                break
        else:
            error(self.line_index, "SyntaxError", f"Unknown syntax {self.line}")

def split(code):
    return re.split("\n",code)

def error(line,type,errormessage):
    print(s,":",line)
    print(type,":",errormessage)
    raise SystemExit

def handler(code):
    if "\"\"\"" in code or "'''" in code:
        _lines = code.splitlines()
        line = 1
        for i in _lines:
            if "\"\"\"" in i or "'''" in i:
                break
            line += 1
        error(line,"SyntaxError","Unable to parse triple quote")
    lines = split(code)
    lines = [*filter(lambda x: x,lines)]
    for line_index in range(len(lines)):
        line = lines[line_index]
        class GotoNextLine(Exception):
            pass
        
        try:
            if line.endswith(":"):
                raise GotoNextLine()
            if line.endswith(": -> Python"):
                line = line.replace(": -> Python", "")
                raise GotoNextLine()
            indent = 0
            for char in line:
                if char == " ":
                    indent += 1
                    continue
                break
            line_strip_space = line.lstrip()
            
            parser_line = ParserLine(line_strip_space,line_index+1) # 解析单行
            parser_line.parser_line()
            line = indent * " " + parser_line.result
            raise GotoNextLine()
        except GotoNextLine:
            lines[line_index] = line
    code = "\n".join(lines)
 
    return code

import sys;s,d=sys.argv[1:];scf=open(s);sc=scf.read();scf.close();df=open(d,"w");r=handler(sc);df.write(r);df.close();
