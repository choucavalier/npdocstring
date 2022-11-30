from typing import List, Union


def function_with_defaults(a: int, b: str = "hello") -> List[int]:
    print(b, a)
    return [a, a]


def function_with_no_defaults(a: int, b: List[int]) -> int:
    b.append(a)
    return sum(b)


def function_with_none_default(a: str | None = None) -> Union[int, str]:
    if a is None:
        a = "hello"
    return a
