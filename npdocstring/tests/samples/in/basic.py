import sys


def basic_function(file_path: str) -> int:
    result = len(sys.path)
    result += len(open(file_path).readlines())
    return result


class BasicClass:
    def basic_method(self) -> None:
        pass

    async def basic_async_method(self) -> None:
        def nested_method() -> None:
            pass

    def method_with_docstring(self) -> None:
        """This method has a docstring.

        Because of that, it shouldn't be generated.
        """
        pass


def function_with_docstring(a: int, b: int) -> int:
    """This function has a docstring.

    Because of that, it shouldn't be generated.
    """
    return a ** b
