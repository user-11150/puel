from uel.Constants import ENCODING
from uel.core.builder.Handler import Handler

# class Builder:
    # def __init__(self,*args):
        # self.args = args[:-1]
        # self.source = args[-2]
        # self.dist = args[-1]
    
    # def build(self) -> None:
        # """
        # 编译
        # """
        # with open(self.source, mode="rt", encoding=ENCODING) as fps, \
             # open(self.dist,   mode='wb') as fpo:
             
            # content = fps.read()
            # handler = Handler(self.source, content)
            # handler.build()
            
            # result: str = handler.result or ""
            
            # file_header = f"# coding: {ENCODING}".encode("ASCII")
            
            # fpo.write(file_header)
            # fpo.write("\n".encode(ENCODING))
            
            # fpo.write(result.encode(ENCODING))
            
            # if not result.endswith("\n"):
                # # Convention: Final newline missing
                
                # fpo.write('\n'.encode(ENCODING))
            # fpo.flush()
            # print('Compelete')
