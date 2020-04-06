from typing import List


class MyClass:
    """FIXME

  Parameters
  ----------
  attr1 : str
    FIXME

  arg2 : int, optional (default=42)
    FIXME

  arg3 : list of int, optional (default=[])
    FIXME

  Attributes
  ----------
  attr2
    FIXME

  attr3
    FIXME

  """

    def __init__(
        self, attr1: str, arg2: int = 42, arg3: List[int] = []
    ) -> None:

        self.attr1 = attr1
        self.attr2 = arg2
        self.attr3 = arg3
