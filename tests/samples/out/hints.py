from typing import List, Union


def function_with_nested_subscript_hint(a: List[List[int]]) -> int:
  '''FIXME

  Parameters
  ----------
  a : list of list of int
    FIXME

  Returns
  -------
  int
    FIXME

  '''

  return sum(sum(a))


def function_with_union_hint(x: Union[List[int], str]) -> bool:
  '''FIXME

  Parameters
  ----------
  x : list of int or str
    FIXME

  Returns
  -------
  bool
    FIXME

  '''

  return len(x) > 0


def function_with_complex_hint(x: List[Union[List[int], str]]) -> bool:
  '''FIXME

  Parameters
  ----------
  x : list of list of int or str
    FIXME

  Returns
  -------
  bool
    FIXME

  '''

  return len(x)
