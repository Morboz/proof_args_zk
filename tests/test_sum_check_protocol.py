from proof_args_zk.multivariate_lagrange_interpolation import (
    MultilinearLagrangeInterpolationPolynomial,
    MultiplicationPolynomial,
    PartialPolynomial,
    PartialSpec,
)
from proof_args_zk.sum_check_protocol import (
    CoefficientPolynomial,
    PolynomialTerm,
    Prover,
    Verifier,
    fix_some_variables,
    fix_some_variables_in_term,
    sum_check,
)


def test_fix_some_variables_in_term():
    t1 = PolynomialTerm(1, 2, [1, 1], 65537)

    assert t1.evaluate([1, 1]) == 1
    assert t1.evaluate([0, 1]) == 0
    assert t1.evaluate([1, 0]) == 0
    assert t1.evaluate([0, 0]) == 0
    t2 = fix_some_variables_in_term(t1, [None, 1])
    assert t2.evaluate([1, 1]) == 1
    assert t2.evaluate([1, 0]) == 1


def test_term_evaluate():
    t1 = PolynomialTerm(1, 2, [1, 1], 65537)
    assert t1.evaluate([1, 1]) == 1

    assert t1.evaluate([0, 1]) == 0
    assert t1.evaluate([1, 0]) == 0
    assert t1.evaluate([0, 0]) == 0
    assert t1.var_count == 2

    t2 = PolynomialTerm(1, 2, [0, 1], 65537)

    assert t2.evaluate([1, 1]) == 1
    assert t2.evaluate([0, 1]) == 1
    assert t2.evaluate([1, 0]) == 0
    assert t2.evaluate([0, 0]) == 0
    assert t2.var_count == 1

    t3 = PolynomialTerm(2, 2, [0, 0], 65537)

    assert t3.evaluate([1, 1]) == 2
    assert t3.is_constant


def test_poly_evaluate():
    v = 3
    t1 = PolynomialTerm(2, v, [3, 0, 0], 65537)
    t2 = PolynomialTerm(1, v, [1, 0, 1], 65537)
    t3 = PolynomialTerm(1, v, [0, 1, 1], 65537)
    t4 = PolynomialTerm(2, v, [0, 0, 0], 65537)

    p = CoefficientPolynomial(65537, [t1, t2, t3, t4])
    assert p.var_count == 3
    # assert p.evaluate([1, 1, 1]) == 4
    assert p.evaluate([0, 0, 0]) == 2
    # assert p.evaluate([0, 0, 1]) == 1
    # assert p.evaluate([0, 1, 0]) == 1
    # assert p.evaluate([0, 1, 1]) == 3
    # assert p.evaluate([1, 0, 0]) == 2
    # assert p.evaluate([1, 0, 1]) == 3
    # assert p.evaluate([1, 1, 0]) == 3
    # assert p.evaluate([1, 1, 1]) == 4


def test_poly_evaluate2():
    v = 3
    t1 = PolynomialTerm(2, v, [3, 0, 0], 65537)
    t2 = PolynomialTerm(1, v, [1, 0, 0], 65537)
    t4 = PolynomialTerm(2, v, [0, 0, 0], 65537)

    p = CoefficientPolynomial(65537, [t1, t2, t4])
    assert p.var_count == 1

    assert p.evaluate(1) == 5


def test_poly_evaluate3():
    v = 3
    t1 = PolynomialTerm(2, v, [0, 3, 0], 65537)
    t2 = PolynomialTerm(1, v, [0, 2, 0], 65537)
    t4 = PolynomialTerm(2, v, [0, 0, 0], 65537)

    p = CoefficientPolynomial(65537, [t1, t2, t4])
    assert p.var_count == 1

    assert p.evaluate(1) == 5


def test_sum_check_protocol():
    # 手动计算一下手稿中的例子
    v = 3
    t1 = PolynomialTerm(2, v, [3, 0, 0], 65537)
    t2 = PolynomialTerm(1, v, [1, 0, 1], 65537)
    t3 = PolynomialTerm(1, v, [0, 1, 1], 65537)
    p = CoefficientPolynomial(65537, [t1, t2, t3])
    print(p)

    assert p.evaluate([1, 1, 1]) == 4
    sum_ = 0
    for i in range(1 << v):
        b = [int(x) for x in reversed(bin(i)[2:].zfill(v))]
        sum_ += p.evaluate(b)

    print(f"sum -> {sum_}")
    assert sum_ == 12

    g1 = None
    for i in range(1 << (v - 1)):
        b = [int(x) for x in reversed(bin(i)[2:].zfill(v - 1))]
        p1 = fix_some_variables(p, [None] + b)
        # sum_ += p.evaluate(b)
        if g1 is None:
            g1 = p1
        else:
            g1 += p1

    print(f"g1 -> {g1}")

    assert g1.evaluate([0, 0, 0]) + g1.evaluate([1, 0, 0]) == sum_

    # r1 = 2
    g2 = None
    for i in range(1 << (v - 2)):
        b = [int(x) for x in reversed(bin(i)[2:].zfill(v - 2))]
        p2 = fix_some_variables(p, [2, None] + b)
        if g2 is None:
            g2 = p2
        else:
            g2 += p2

    print(f"g2 -> {g2}")
    assert g1.evaluate([2, 0, 0]) == g2.evaluate([2, 0, 0]) + g2.evaluate([2, 1, 0])

    # r2 = 3
    g3 = None
    for i in range(1 << (v - 3)):
        p3 = fix_some_variables(p, [2, 3, None])
        if g3 is None:
            g3 = p3
        else:
            g3 += p3
    print(f"g3 -> {g3}")
    assert g2.evaluate([2, 3, 0]) == g3.evaluate([2, 3, 0]) + g3.evaluate([2, 3, 1])

    # r3 = 6
    assert g3.evaluate([2, 3, 6]) == p.evaluate([2, 3, 6])


def test_sum_check_protocol_total():
    v = 3
    t1 = PolynomialTerm(2, v, [3, 0, 0], 65537)
    t2 = PolynomialTerm(1, v, [1, 0, 1], 65537)
    t3 = PolynomialTerm(1, v, [0, 1, 1], 65537)
    g = CoefficientPolynomial(65537, [t1, t2, t3])
    prover = Prover(g, v)
    verifier = Verifier(g)

    assert sum_check(prover, verifier)


def test_matmult_sum_check():
    # mat n * n, n = 2
    n = 2
    # mat A

    A = [0, 1, 2, 0]
    p = 5

    f_A_mle = MultilinearLagrangeInterpolationPolynomial(p, A, n)

    assert f_A_mle.evaluate([0, 0]) == 0
    assert f_A_mle.evaluate([1, 0]) == 1
    assert f_A_mle.evaluate([0, 1]) == 2
    assert f_A_mle.evaluate([1, 1]) == 0

    B = [1, 0, 0, 4]
    f_B_mle = MultilinearLagrangeInterpolationPolynomial(p, B, n)

    assert f_B_mle.evaluate([0, 0]) == 1
    assert f_B_mle.evaluate([1, 0]) == 0
    assert f_B_mle.evaluate([0, 1]) == 0
    assert f_B_mle.evaluate([1, 1]) == 4

    # C = [0, 4, 2, 0]

    r1 = [3]
    r2 = [2]

    r1_partial = PartialSpec(r1, True)
    f_A_mle_r1 = PartialPolynomial(f_A_mle, r1_partial)
    r2_partial = PartialSpec(r2, False)
    f_B_mle_r2 = PartialPolynomial(f_B_mle, r2_partial)

    assert f_A_mle_r1.evaluate([2]) == f_A_mle.evaluate([3, 2])
    assert f_B_mle_r2.evaluate([3]) == f_B_mle.evaluate([3, 2])

    g = MultiplicationPolynomial(f_A_mle_r1, f_B_mle_r2)
    assert g.evaluate([2]) == (f_A_mle.evaluate([3, 2]) * f_B_mle.evaluate([2, 2]) % p)
