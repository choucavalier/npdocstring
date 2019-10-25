from typing import List, Union


def function_with_defaults(a: int, b: str = "hello") -> List[int]:
    print(b, a)


def function_with_no_defaults(a: int, b: List[int]) -> int:
    b.append(a)
    return sum(b)


def function_with_none_default(a: str = None) -> Union[int, str]:
    return a
