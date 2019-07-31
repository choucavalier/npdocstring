from typing import List, Union


def function_with_defaults(a: int, b: str = 'hello') -> List[int]:
  '''FIXME

  Parameters
  ----------
  a : int
    FIXME

  b : str, optional (default='hello')
    FIXME

  Returns
  -------
  list of int
    FIXME

  '''

  print(b, a)


def function_with_no_defaults(a: int, b: List[int]) -> int:
  '''FIXME

  Parameters
  ----------
  a : int
    FIXME

  b : list of int
    FIXME

  Returns
  -------
  int
    FIXME

  '''

  b.append(a)
  return sum(b)


def function_with_none_default(a: str = None) -> Union[int, str]:
  '''FIXME

  Parameters
  ----------
  a : str, optional (default=None)
    FIXME

  Returns
  -------
  int or str
    FIXME

  '''

  return a
