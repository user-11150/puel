# 1. Is the feature like python "is"?
Yes. Like python, it determines whether two values are equal.
# 2. How to do use it?
It's like python. `<left value> is <right value>`
> **Note**:
> It's a BinOp, and it goes from left to right anyway.
> Example:
> ```UEL
> IF a + b is c + d
> ```
> It's equivalent to
>```UEL
> IF ((a + b) is c) + d
> ```
> Note, however, that the UEL does not have parentheses, just to be more intuitive
# How to judge whether it is equal or not
1. If left or right overload `tp_equal` call the PyFunction(or PyMethod)
2. If both left and right have `.val` use Python's `==`