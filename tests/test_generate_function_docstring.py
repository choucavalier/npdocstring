from npdocstring.npdocstring import (
    generate_function_docstring,
    get_funclassdef_nodes,
)

BASIC_FUNCTION_EXPECTED = """\"\"\"
FIXME

Parameters
----------
file_path : str
    FIXME

Returns
-------
int
    FIXME

\"\"\"
"""


DEFAULT_FUNCTION_EXPECTED = """\"\"\"
FIXME

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

\"\"\"
"""


def test_basic_function():
    file_content = open("tests/samples/in/basic.py").read()
    fcnodes = get_funclassdef_nodes(file_content)
    assert len(fcnodes) == 4
    assert fcnodes[0].name == "basic_function"
    assert generate_function_docstring(fcnodes[0]) == BASIC_FUNCTION_EXPECTED


def test_default_function():
    file_content = open("tests/samples/in/defaults.py").read()
    fcnodes = get_funclassdef_nodes(file_content)
    assert len(fcnodes) == 3
    assert generate_function_docstring(fcnodes[0]) == DEFAULT_FUNCTION_EXPECTED
