def int_to_bool_array(i: int, v: int) -> list[int]:
    """Convert an integer to a boolean array

    Example:
        i = 1, v = 3 -> [1, 0, 0]
        i = 2, v = 3 -> [0, 1, 0]
        i = 3, v = 3 -> [1, 1, 0]
        i = 4, v = 3 -> [0, 0, 1]
        第一位是最低位，最后一位是最高位，b100 -> [0, 0, 1]

        类似小端序, 低位在前，高位在后

    Args:
        i (int): integer
        v (int): length of the boolean array
    """
    if v == 0:
        return []
    return [int(x) for x in reversed(bin(i)[2:].zfill(v))]


def bool_array_to_int(b: list[int]) -> int:
    """Convert a boolean array to an integer

    Example:
        [1, 0, 0] -> 1
        [0, 1, 0] -> 2
        [1, 1, 0] -> 3
        [0, 0, 1] -> 4
        [0, 0, 0] -> 0

    Args:
        b (list[int]): boolean array
    """
    return int("".join([str(x) for x in reversed(b)]), 2)
