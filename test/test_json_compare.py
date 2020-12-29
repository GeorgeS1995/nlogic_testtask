import os
import pytest
from json_compare import _compare
from test.test_utils import get_test_data


@pytest.mark.parametrize("d", get_test_data(os.path.join(os.getcwd(), "test", "test_data", "test_json_compare.json")))
def test_json_compare(d):
    r = _compare(d['obj_1'], d['obj_2'])
    assert r == d['output']
