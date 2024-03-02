import os,sys
import time
import io
import tqdm

from functools import lru_cache
path = './'

sys.setrecursionlimit(1000000)

def contain(p):
    return (".git" in p or ".obsidian" in p or "mypy_cache" in p)

def getsumsize(p = path):
    if contain(p):
        return 0
    if os.path.isdir(p):
        result = 0
        for i in os.listdir(p):
            allpath = os.path.join(p,i)
            result += getsumsize(allpath)
        return result
    else:
        #print(p)
        return os.path.getsize(p)    

def getfilename(path,end):
    lis = []
    for root,dirs,files in os.walk(path):
        for i in files:
            p = os.path.join(root,i)
            if contain(p):
                continue
            for i in end:
                if p.endswith(i):
                    lis.append(p)
    return lis
@lru_cache()    
def getLine(path):
    try:
        with open(path,'rt') as fp:
            content = fp.read()
            return content.count('\n') + 1
    except:
        return 1

import threading
item = [
    (
        '代码',
        (
            '.js',
            '.css',
            '.py',
            '.js.LICENSE.txt',
            '.html',
        )
    ),
    (
        '文档',
        (
            '.md',
            'LICENSE'
        )
    ),
    (
        'python',
        (
            '.py',
        )
    ),
    
    (
        '配置',
        (
            '.json',
            '.ini'
        )
    ),
    (
        '前端',
        (
            '.js',
            '.css',
            '.html',
        )
    ),
    (
        '图片，视频，音频等',
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
        'sh',
        (
            '.sh',
        )
    ),
    (
        '日志',
        (
            
            '.log',
            *[
                f'.log.{i}' for i in range(2,3)
            ]
        )
    ),
]

item.insert(0,
  ("所有的",
    tuple(set(
        (lambda x:[n for t in x for n in t])([i for z,i in item])
    ))
  )
)


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

def update(*args,**kwargs):
    print(*args,**kwargs,file=stream)

def getlength(i):
    with open(i,'rb')as f:
        res = f.read()
    return len(res)
def task(name,s):
    update(f'{name}：')
    f = files = getfilename(path,s)
    
    size = sum([os.path.getsize(i) for i in f])
    line_n = sum([getLine(i) for i in f])
    file_number = len(files)
    if file_number is 0 or line_n is 0:
        update('\t无')
        return
    def sizeof(x):
        sss = 0.8
        l = 5
        def f(x): return str(round(x,3)).rjust(l,"0")
        if x/1024/1024/1024 > sss:
            return f'{f(x/1024/1024/1024)}GB'
        if x/1024/1024 > sss:
            return f'{f(x/1024/1024)}MB'
        if x/1024 > sss:
            return f'{f(x/1024)}KB'
        return f'{x}字节'    
    update('\t所有代码总大小',sizeof(size))
    update('\t文件个数',len(files))
    update('\t行数和',line_n)
    update('\t平均文件行数',line_n/file_number)
    update('\t平均每一个文件的大小',sizeof(size/len(files)))
    update('\t平均一行多少',sizeof(size/line_n))
    update('\t占总数的', round(size/sumsize*100,7),'%')
    update('\t行数占总行数的',line_n/line*100,"%")

def main():

    rmpycache()
    global line,sumsize,stream,day
    startTime = time.mktime(time.strptime('2024-2-24 22:0:0','%Y-%m-%d %H:%M:%S'))
    day = (time.time()-startTime)/60/60/24
    stream = io.StringIO()
    line = sum([getLine(i) for i in getfilename(path,item[0][1])])
    sumsize = getsumsize()
    
    print('开发天数',day)
    print('平均每天代码行数',line/day)
    print('不算pyc，git，obsidian(markdwon软件)产生的')

    for i in tqdm.tqdm(item):
        task(*i)
    print(stream.getvalue())
    print(flush=True)

main()
