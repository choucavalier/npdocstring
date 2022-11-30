from ..npdocstring import get_funclassdef_nodes, get_function_arguments, process_file


def test_list_of_dataframes():
    file_content = open("npdocstring/tests/samples/in/pandas.py").read()
    fcnodes = get_funclassdef_nodes(file_content)
    assert len(fcnodes) == 1
    args = get_function_arguments(fcnodes[0])
    assert len(args) == 1
    assert args[0].hint == "pd.DataFrame"
    output = process_file(file_content)
