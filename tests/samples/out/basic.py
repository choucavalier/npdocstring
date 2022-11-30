import sys


def basic_function(file_path: str) -> int:
    """FIXME

    Parameters
    ----------
    file_path : str
      FIXME

    Returns
    -------
    int
      FIXME

    """

    result = len(sys.path)
    result += len(open(file_path).readlines())
    return result


class BasicClass:
    """FIXME"""

    def basic_method(self) -> None:
        """FIXME

        Returns
        -------
        None
            FIXME

        """
        pass

    async def basic_async_method(self) -> None:
        """FIXME

        Returns
        -------
        None
            FIXME

        """

        def nested_method() -> None:
            pass

    def method_with_docstring(self) -> None:
        """This method has a docstring

        Because of that, it shouldn't be generated.
        """
        pass


def function_with_docstring(a: int, b: int) -> int:
    """This function has a docstring

    Because of that, it shouldn't be generated.
    """
    return a**b
