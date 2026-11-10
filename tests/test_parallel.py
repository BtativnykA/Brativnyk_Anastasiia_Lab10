import pytest

from student_manager.analytics import statistics_numpy, statistics_python


def test_numpy_matches_python_stats():
    values = [70.0, 80.0, 90.0, 100.0, 60.0]
    py_res = statistics_python(values)
    np_res = statistics_numpy(values)

    assert np_res["average"] == pytest.approx(py_res["average"])
    assert np_res["minimum"] == pytest.approx(py_res["minimum"])
    assert np_res["maximum"] == pytest.approx(py_res["maximum"])
    assert np_res["std"] == pytest.approx(py_res["std"])
