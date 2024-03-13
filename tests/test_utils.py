from proof_args_zk.utils import bool_array_to_int, int_to_bool_array


def test_int_to_bool_array():
    assert int_to_bool_array(1, 3) == [1, 0, 0]
    assert int_to_bool_array(2, 3) == [0, 1, 0]
    assert int_to_bool_array(3, 3) == [1, 1, 0]
    assert int_to_bool_array(4, 3) == [0, 0, 1]
    assert int_to_bool_array(0, 3) == [0, 0, 0]
    assert int_to_bool_array(7, 3) == [1, 1, 1]
    assert int_to_bool_array(10, 4) == [0, 1, 0, 1]
    assert int_to_bool_array(15, 4) == [1, 1, 1, 1]
    assert int_to_bool_array(16, 5) == [0, 0, 0, 0, 1]
    assert int_to_bool_array(31, 5) == [1, 1, 1, 1, 1]


def test_bool_array_to_int():
    assert bool_array_to_int([1, 0, 0]) == 1
    assert bool_array_to_int([0, 1, 0]) == 2
    assert bool_array_to_int([1, 1, 0]) == 3
    assert bool_array_to_int([0, 0, 1]) == 4
    assert bool_array_to_int([0, 0, 0]) == 0
    assert bool_array_to_int([1, 1, 1]) == 7
    assert bool_array_to_int([0, 1, 0, 1]) == 10
    assert bool_array_to_int([1, 1, 1, 1]) == 15
    assert bool_array_to_int([0, 0, 0, 0, 1]) == 16
    assert bool_array_to_int([1, 1, 1, 1, 1]) == 31
