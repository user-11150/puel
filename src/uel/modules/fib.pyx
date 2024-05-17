from functools import cache

@cache
def fib(n: Int):
    if n <= 2:
        return 1
    return fib(n - 1) + fib(n - 2)
