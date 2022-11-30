# npdocstring

Generate missing docstrings
([numpydoc](https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt)
style) in your **Python** source code.

Requirements:

- `Python 3.10+`

![Build Status](https://github.com/tgy/npdocstring/actions/workflows/ci.yml/badge.svg)
<img src="https://github.com/tgy/npdocstring/actions/workflows/ci.yml/badge.svg">

This program will also parse the `Python 3.X.X` type hints and add them to the
generated docstring.

For example, when the following file is piped to `npdocstring`

```python
def test_function(a: int, b: List[int]) -> int:

  b.append(a)
  return sum(b)
```

`npdocstring` outputs this

```python
def test_function(a: int, b: List[int]) -> int:
  '''

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
```
