import random
import time

from proof_args_zk.multivariate_lagrange_interpolation import (
    MultilinearLagrangeInterpolationPolynomial,
)
from proof_args_zk.univariate_lagrange_interpolation import prime_greater_than


def test_mli():
    # 这里的a的元素和x的数组映射关系，x的数组的第i个元素，是对应poly中的x_i+1,
    poly = MultilinearLagrangeInterpolationPolynomial(5, [1, 2, 1, 4], 2)
    # 低 -> 高
    # x1, x2 -> f(x1, x2)
    # 0, 0 -> 1
    # 1, 0 -> 2
    # 0, 1 -> 1
    # 1, 1 -> 4
    assert poly.evaluate([0, 0]) == 1
    assert poly.evaluate([1, 0]) == 2
    assert poly.evaluate([0, 1]) == 1
    assert poly.evaluate([1, 1]) == 4

    assert poly.evaluate([2, 0]) == 3
    assert poly.evaluate([3, 4]) == 3
    assert poly.evaluate([4, 4]) == 2
    assert poly.evaluate([3, 1]) == 0

    # exercise 3.3
    poly2 = MultilinearLagrangeInterpolationPolynomial(11, [1, 3, 2, 4, 5, 7, 6, 8], 3)
    assert poly2.evaluate([2, 4, 6]) == 0
    print("multi count: ", poly2.multipliation_count)


def test_mli_eval_fast():
    # 这里的a的元素和x的数组映射关系，x的数组的第i个元素，是对应poly中的x_i+1,
    poly = MultilinearLagrangeInterpolationPolynomial(5, [1, 2, 1, 4], 2)
    # 低 -> 高
    # x1, x2 -> f(x1, x2)
    # 0, 0 -> 1
    # 1, 0 -> 2
    # 0, 1 -> 1
    # 1, 1 -> 4
    assert poly.evaluate_fast([0, 0]) == 1
    assert poly.evaluate_fast([1, 0]) == 2
    assert poly.evaluate_fast([0, 1]) == 1
    assert poly.evaluate_fast([1, 1]) == 4

    assert poly.evaluate_fast([2, 0]) == 3
    assert poly.evaluate_fast([3, 4]) == 3
    assert poly.evaluate_fast([4, 4]) == 2
    assert poly.evaluate_fast([3, 1]) == 0
    # exercise 3.3
    poly2 = MultilinearLagrangeInterpolationPolynomial(11, [1, 3, 2, 4, 5, 7, 6, 8], 3)
    assert poly2.evaluate_fast([2, 4, 6]) == 0
    assert poly2.multipliation_count <= 20


def test_compare_calc_time():

    v = 16
    n = 2**v
    a = [random.randint(0, 128) for _ in range(n)]
    p = prime_greater_than(n * v)

    r = [random.randint(0, p - 1) for _ in range(v)]

    poly = MultilinearLagrangeInterpolationPolynomial(p, a, v)

    st = time.time()
    print(f"poly.evaluate(): {poly.evaluate(r)}")
    et1 = time.time()
    print(f"poly.evalate_fast(): {poly.evaluate_fast(r)}")
    et2 = time.time()
    print(f"evaluate time: {et1 - st}")
    print(f"evalate_fast time: {et2 - et1}")
