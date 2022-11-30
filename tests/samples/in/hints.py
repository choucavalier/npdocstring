from typing import Iterable, List, Union


def function_with_nested_subscript_hint(a: List[List[int]]) -> int:
    return sum(sum(x) for x in a)


def function_with_union_hint(x: Union[List[int], str]) -> bool:
    return len(x) > 0


def function_with_complex_hint(x: List[Union[List[int], str]]) -> int:
    return len(x)


def function_with_iterable(x: Union[int, Iterable[int]]) -> Iterable[int]:
    if isinstance(x, int):
        return [x]
    return x
