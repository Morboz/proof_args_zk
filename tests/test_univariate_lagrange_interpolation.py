from proof_args_zk.univariate_lagrange_interpolation import (
    UnivariableLangrangeInterpolationPolynomial,
    prime_greater_than,
)


def test_univariate_lagrange_interpolation():
    p = 11
    a = [2, 1, 1]
    poly1 = UnivariableLangrangeInterpolationPolynomial(p, a)

    assert poly1.evaluate(0) == 2
    assert poly1.evaluate(1) == 1
    assert poly1.evaluate(2) == 1
    assert poly1.evaluate(3) == 2
    assert poly1.evaluate(4) == 4
    assert poly1.evaluate(5) == 7
    assert poly1.evaluate(6) == 0
    assert poly1.evaluate(7) == 5
    assert poly1.evaluate(8) == 0
    assert poly1.evaluate(9) == 7
    assert poly1.evaluate(10) == 4

    # assert poly1.evalate_fast(1) == 1

    for i in range(11):
        assert poly1.evaluate(i) == poly1.evalate_fast(i)

    b = [2, 1, 0]
    poly2 = UnivariableLangrangeInterpolationPolynomial(p, b)

    assert poly2.evaluate(0) == 2
    assert poly2.evaluate(1) == 1
    assert poly2.evaluate(2) == 0
    assert poly2.evaluate(3) == 10
    assert poly2.evaluate(4) == 9
    assert poly2.evaluate(5) == 8
    assert poly2.evaluate(6) == 7
    assert poly2.evaluate(7) == 6
    assert poly2.evaluate(8) == 5
    assert poly2.evaluate(9) == 4
    assert poly2.evaluate(10) == 3

    for i in range(11):
        assert poly2.evaluate(i) == poly2.evalate_fast(i)


# def test_lde():
#     # generate a integer list of length 10000

#     a = [random.randint(0, 128) for _ in range(10000)]

#     # test the low degree extension

#     poly = low_degree_extension(a)
#     r = random.randint(0, poly.p - 1)
#     st = time.time()
#     print(f"poly.evaluate({r}): {poly.evaluate(r)}")
#     et1 = time.time()
#     print(f"poly.evalate_fast({r}): {poly.evalate_fast(r)}")
#     et2 = time.time()
#     print(f"evaluate time: {et1 - st}")
#     print(f"evalate_fast time: {et2 - et1}")


def test_prime_greater_than():
    assert prime_greater_than(0) == 2
    assert prime_greater_than(1) == 2
    assert prime_greater_than(2) == 3
    assert prime_greater_than(3) == 5
    assert prime_greater_than(10) == 11
    assert prime_greater_than(100) == 101
    assert prime_greater_than(1000) == 1009
    assert prime_greater_than(10000) == 10007
    # Add more test cases if needed
