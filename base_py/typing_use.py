from typing import List

"""
typing - 类型标注支持: https://docs.python.org/zh-cn/3/library/typing.html
"""

# 类型别名
Vector = List[float]


def scale(scalar: float, vector: Vector) -> Vector:  # define return type
    return [scalar * num for num in vector]


new_v = scale(2, [1.0, -4.2, 5.4])
print(new_v)

from typing import NewType

# 自定义类型，为 int 创建别名
UserId = NewType('UserId', int)
a_id = UserId(1)
print(a_id)
print(type(a_id))  # <class 'int'>

# Callable
# 期望特定的回调函数的框架，可以将类型标注为 Callable[[Arg1Type, Arg2Type], ReturnType]
from typing import Callable


def len_fn(s):
    return len(s)


def fetch_data(len_of_str: Callable[[str], int], a_str) -> int:
    return len_of_str(a_str)


print(fetch_data(len_fn, 'hello'))
