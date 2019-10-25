from ..npdocstring import get_funclassdef_nodes
from ..npdocstring import get_function_arguments
from ..npdocstring import AtrOrArg


def test_get_function_arguments():
    file_content = open("npdocstring/tests/samples/in/basic.py").read()
    fcnodes = get_funclassdef_nodes(file_content)
    assert len(fcnodes) == 4
    args = get_function_arguments(fcnodes[0])
    assert len(args) == 1
    assert args[0] == AtrOrArg(name="file_path", hint="str", default=None)
    args = get_function_arguments(fcnodes[-1])
    assert len(args) == 0


def test_get_function_arguments_with_defaults():
    file_content = open("npdocstring/tests/samples/in/defaults.py").read()
    fcnodes = get_funclassdef_nodes(file_content)
    assert len(fcnodes) == 3
    args = get_function_arguments(fcnodes[0])
    assert len(args) == 2
    assert args[0].default is None
    assert args[1].default == "'hello'"
    args = get_function_arguments(fcnodes[1])
    assert len(args) == 2
    assert args[0].default is None
    assert args[1].default is None
    args = get_function_arguments(fcnodes[2])
    assert len(args) == 1
    assert args[0].default == "None"
