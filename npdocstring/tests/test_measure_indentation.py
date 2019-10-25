from ..npdocstring import measure_indentation


def test_measure_indentation():
    file_content = open("npdocstring/tests/samples/in/basic.py").read()
    indentation = measure_indentation(file_content)
    assert indentation == [
        0,
        0,
        0,
        0,
        4,
        4,
        4,
        0,
        0,
        0,
        4,
        8,
        0,
        4,
        8,
        12,
        0,
        4,
        8,
        0,
        8,
        8,
        8,
        0,
        0,
        0,
        4,
        0,
        4,
        4,
        4,
    ]
