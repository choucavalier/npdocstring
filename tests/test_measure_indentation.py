from npdocstring import measure_indentation


def test_measure_indentation():

  file_content = open('tests/samples/basic.py').read()
  indentation = measure_indentation(file_content)
  assert indentation == [0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 2, 4, 0, 2, 4, 6,
                         0, 2, 4, 0, 4, 4, 4, 0, 0, 0, 2, 0, 2, 2, 2]
