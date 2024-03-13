from proof_args_zk.low_degree_test import Receiver, Sender, low_degree_test
from proof_args_zk.multivariate_lagrange_interpolation import (
    MultilinearLagrangeInterpolationPolynomial,
)


def test_low_degree_test():
    v = 2
    p = 5
    poly = MultilinearLagrangeInterpolationPolynomial(p, [1, 2, 1, 4], v)

    receiver = Receiver(p, v)
    sender = Sender(poly)

    assert low_degree_test(sender, receiver)

    for i in range(p):
        for j in range(p):
            print(f"[{i}, {j}] -> {poly.evaluate([i, j])}")
