#pylint:disable=W0718
#pylint:disable=E0102
import os
import sys
import time
import re

try:
    import rich
    del rich
except ImportError as e:
    from pip import main
    main(["install", "rich"])
    del main

from rich.console import Console
from rich.table import Table

from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from concurrent.futures import Future
import sys

def getPath():
    try:
        argv = sys.argv
        run_path, *args = argv
        return args[0]
    except IndexError:
        return "./"

path = getPath()

sys.setrecursionlimit(1000000)

def contain(p):
    return (".git" in p or ".obsidian" in p or "mypy_cache" in p)

def getfilename(path,end):
    lis = []
    for root,_,files in os.walk(path):
        for i in files:
            p = os.path.join(root,i)
            #if contain(root):
#                break
            if contain(p):
                continue
            for i in end:
                if p.endswith(i):
                    lis.append(p)
                    break
    return lis
@lru_cache()    
def getLine(path):
#    try:
#        with open(path,'rt') as fp:
#            content = fp.read()
#            return content.count('\n') + 1
#    except:
#        return 1
     with open(path,"rb") as fp:
         content = fp.read()
         return content.count(b"\n") + 1

items = [
    (
        'Code',
        (
            '.js',
            '.css',
            '.py',
            '.html',
            ".md"
        )
    ),
    (
        'Documentation',
        (
            '.md',
        )
    ),
    (
        'Python',
        (
            '.py',
            ".pyi"
        )
    ),
    
    (
        'Configuration',
        (
            '.json',
            '.ini'
        )
    ),
    (
        'HTML CSS JS',
        (
            '.js',
            '.css',
            '.html',
        )
    ),
    (
        'Binary assets',
        (
            
            '.png',
            '.svg',
            '.mp4',
            '.mp3',
            '.ttf',
            '.jpg'
        )
    ),
    (
        'Shell',
        (
            '.sh',
        )
    ),
    (
        'Logs',
        (
            
            '.log',
            *[
                f'.log.{i}' for i in range(2,3)
            ]
        )
    ),
    (
        "C C++",
        (
            ".c",
            ".h",
            ".cpp",
            ".hpp"
        )
    ),
    (
        "Cython(Pyx)",
        (
           ".pyx",
        )
    )
]


items.insert(0,
  ("All",
    tuple(set(
        (lambda x:[n for t in x for n in t])([i for z,i in items])
    ))
  )
)
class Report:
    def __init__(self, items):
        self.start_time = time.mktime(time.strptime('2024-2-24 22:0:0','%Y-%m-%d %H:%M:%S'))
        self.dev_days = (time.time()-self.start_time)/60/60/24
        self.items = items
        self.console = Console()
        self.pool = ThreadPoolExecutor()
        self.futures = None
        tw = 80
        try:
            tw = os.get_terminal_size().columns
        except Exception:
            pass
        self.terminal_width = tw

    def remove_pycache_files(self):
        """
        为了方便，直接复制的原本的，所以看起来缩进较多
        """
        def rmpycache():
            def getpaths(path):
                result = []
                for i in os.listdir(path):
                    p = os.path.join(path,i)
                    result.append(p)
                    if os.path.isdir(p):
                        result += getpaths(p)
                return result
            def filterpyc(n):
                if os.path.split(n)[1] == '__pycache__' or n.endswith('.pyc'):
                    return True
                return False
            ps = getpaths(path)
            pyc = filter(filterpyc,ps)
            for p in pyc:
                if os.path.isfile(p):
                    os.remove(p)
            pyc,pyc2 = filter(filterpyc,ps),filter(filterpyc,ps)
            
            for p in pyc:
                
                if os.path.isdir(p):
                    os.rmdir(p)
        rmpycache()

    def day(self):
        self.console.print("Number of dev days: ", self.dev_days)

    def create_task(self, item):
        [name, ends] = item
        report_item = ReportItem(name, ends, self)
        return report_item.report()

    def report(self):
        starttime = time.time()
        self.remove_pycache_files()
        self.day()
        self.futures = []
        for item in self.items:
            self.futures.append(self.create_task(item))
        self.wait_for(self.futures)
        endtime = time.time()
        t = int((endtime - starttime) * 1000) #   ↓ Used. pylint: disable=C0103
        self.console.print(f"Time of this report {t} MS")

    @staticmethod
    def wait_for(fs: list[Future]):
        for f in fs:
            f.result()

class ReportItem:
    def __init__(self, name, ends, report: Report):
        self.name = name
        self.ends = ends
        self.__report = report
        self.table = None

    def report(self):
        def _report():
            m = 1.1
            self.table = Table(title=self.name, width=int(self.__report.terminal_width // m))
            self.table.add_column("Name", justify="left")
            self.table.add_column("Value", justify="center")
            class Print(Exception):
                pass
            class Return(Exception):
                pass
            try:
                files = getfilename(path, self.ends)
                res_file_number = len(files)
                if res_file_number == 0:
                    raise Return()
                size_i = sum(self.get_file_size(f) for f in files)
                size = self.stringSize(size_i)
                line_number_i = sum(getLine(f) for f in files)
                line_number = self.seg(str(line_number_i))
                average_number_of_rows = self.seg(int(line_number_i / res_file_number))
                average_number_of_size = self.stringSize(size_i / res_file_number)
                
                self.table.add_row("Number of files", str(res_file_number))
                self.table.add_row("Size", size)
                self.table.add_row("Line number", line_number)
                self.table.add_row("Average number of rows", average_number_of_rows)
                self.table.add_row("Average number of size", average_number_of_size)
                
                raise Print()
            except Print:
                self.__report.console.print(self.table)
            except Return:
                return
            
        return self.__report.pool.submit(_report)

    @staticmethod
    def get_file_size(i):
        return os.path.getsize(i)

    @staticmethod
    def stringSize(byte: int):
        base_unit = 'B', 1
        unit_kb = "KB", 1024
        unit_mb = "MB", 1024 * 1024
        unit_gb = "GB", 1024 * 1024 * 1024
        
        current_unit = base_unit
        
        u = 0.85
                
        if byte > 1024 * u:
            current_unit = unit_kb
        if byte > 1024 * 1024 * u:
            current_unit = unit_mb
        if byte > 1024 * 1024 * 1024 * u:
            current_unit = unit_gb
        left = round(byte / current_unit[1], 2)
        return f"{left}{current_unit[0]}"

    @staticmethod
    def seg(number: int):
        """
        example:
            104354 => 10,4354
        """
        if type(number) is float or type(number) is int: # pylint: disable=C0123
            number = str(number)
        return re.sub(r"(?=\B\d{3}+$)", ",", str(number))

def main():
    report = Report(items)
    report.report()
    

if __name__ == "__main__":
    main()
