from proof_args_zk.multivariate_lagrange_interpolation import (
    MultilinearLagrangeInterpolationPolynomial,
)
from proof_args_zk.relaxed_polynomial_commitment_scheme import (
    Prover,
    Verifier,
    field_element_array_to_int,
    int_to_field_element_array,
    polynomial_commitment_scheme,
)


def test_int_to_field_element_array():
    # Test case 1: prime = 2, variables = 3
    integer = 10
    prime = 2
    variables = 3
    expected_result = [0, 1, 0]
    assert int_to_field_element_array(integer, prime, variables) == expected_result

    # Test case 2: prime = 5, variables = 4
    integer = 123
    prime = 5
    variables = 4
    expected_result = [3, 4, 4, 0]
    assert int_to_field_element_array(integer, prime, variables) == expected_result

    # Test case 3: prime = 7, variables = 2
    integer = 9
    prime = 7
    variables = 2
    expected_result = [2, 1]
    assert int_to_field_element_array(integer, prime, variables) == expected_result

    # Test case 4: prime = 3, variables = 1
    integer = 2
    prime = 3
    variables = 1
    expected_result = [2]
    assert int_to_field_element_array(integer, prime, variables) == expected_result

    # Test case 5: prime = 2, variables = 5
    integer = 31
    prime = 2
    variables = 5
    expected_result = [1, 1, 1, 1, 1]
    assert int_to_field_element_array(integer, prime, variables) == expected_result


def test_field_element_array_to_int():
    # Test case 1: prime = 2
    field_element_array = [0, 1, 0]
    prime = 2
    variables = 3
    expected_result = 2
    assert field_element_array_to_int(field_element_array, prime, 3) == expected_result

    # Test case 2: prime = 5
    field_element_array = [3, 4, 4, 0]
    prime = 5
    variables = 4
    expected_result = 123
    assert (
        field_element_array_to_int(field_element_array, prime, variables)
        == expected_result
    )


def test_calculate_s():
    v = 2
    p = 5
    poly = MultilinearLagrangeInterpolationPolynomial(p, [1, 2, 1, 4], v)
    s = Prover(poly).calculate_s()
    print(s)
    assert len(s) == p**v

    for i in range(p**v):
        ele_arr = int_to_field_element_array(i, p, v)
        print(f"{ele_arr} -> {s[i]}")


def test_polynomial_commitment_scheme():
    v = 2
    p = 5
    poly = MultilinearLagrangeInterpolationPolynomial(p, [1, 2, 1, 4], v)
    prover = Prover(poly)
    verifier = Verifier(p, v)
    assert polynomial_commitment_scheme(prover, verifier)
