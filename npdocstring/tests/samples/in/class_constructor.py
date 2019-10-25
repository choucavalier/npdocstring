from typing import List


class MyClass:
    def __init__(
        self, attr1: str, arg2: int = 42, arg3: List[int] = []
    ) -> None:
        self.attr1 = attr1
        self.attr2 = arg2
        self.attr3 = arg3
