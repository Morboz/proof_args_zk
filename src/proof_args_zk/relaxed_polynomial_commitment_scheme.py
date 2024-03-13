# A (Relaxed) Polynomial Commitment Scheme by Combining Merkle Trees
# and Low-Degree Tests.

from proof_args_zk.low_degree_test import Receiver, Sender
from proof_args_zk.merkle_tree import build_merkle_tree, leaf_hash, reaveal_leaf
from proof_args_zk.univariate_lagrange_interpolation import (
    UnivariableLangrangeInterpolationPolynomial,
)


def int_to_field_element_array(integer: int, prime: int, variables: int):
    result = []
    for _ in range(variables):
        result.append(integer % prime)
        integer = integer // prime
    return result


def field_element_array_to_int(
    field_element_array: list[int], prime: int, variables: int
):
    if len(field_element_array) != variables:
        raise ValueError("Length of field_element_array should be equal to variables")
    result = 0
    for i in range(len(field_element_array)):
        result += field_element_array[i] * prime**i
    return result


class Prover:
    def __init__(self, multilinear_polynomial) -> None:
        self.multilinear_polynomial = multilinear_polynomial
        self.p = multilinear_polynomial.p
        self.v = multilinear_polynomial.v

        self.low_degree_test_sender = Sender(multilinear_polynomial)

        self.merkle_root = None
        self.merkle_leaves = None

    def calculate_s(self) -> list[int]:
        # for all possible input, calculate evaluations
        s_list = []
        all_inputs_num = self.p**self.v
        for i in range(all_inputs_num):
            ele_arr = int_to_field_element_array(i, self.p, self.v)
            s_list.append(self.multilinear_polynomial.evaluate(ele_arr))
        return s_list

    def build_merkle_tree(self, s: list[int]) -> tuple:
        root, leaves = build_merkle_tree([str(i) for i in s])
        self.merkle_root = root
        self.merkle_leaves = leaves
        return root, leaves

    def authentications_of_line(
        self, a: int, b: int
    ) -> list[list[tuple[str, str | None, str | None]]]:
        def func_l(t: int) -> list[int]:
            return [(a[i] * t + b[i]) % self.p for i in range(self.v)]

        authentications = []
        for ti in range(self.p):
            xi = func_l(ti)
            leaf_index = field_element_array_to_int(xi, self.p, self.v)
            authentications.append(self.reveal_authentication_at(leaf_index))
        return authentications

    def reveal_authentication_at(
        self, index: int
    ) -> list[tuple[str, str | None, str | None]]:
        return reaveal_leaf(self.merkle_leaves[index])


class Verifier:
    def __init__(self, p: int, v: int) -> None:
        self.low_degree_test_receiver = Receiver(p, v)
        self.root_hash = None

    def check_authentications(
        self,
        univariate_polynomial: UnivariableLangrangeInterpolationPolynomial,
        authentications: list[list[tuple[str, str | None, str | None]]],
    ) -> bool:
        univariate_polynomial_evaluations = (
            self.low_degree_test_receiver.evaluatations_of_univariate_polynomial(
                univariate_polynomial
            )
        )

        for i in range(len(authentications)):
            auth_i = authentications[i]
            if auth_i[-1][0] != self.root_hash:
                return False
            if auth_i[0][0] != leaf_hash(str(univariate_polynomial_evaluations[i])):
                return False
        return True


def polynomial_commitment_scheme(prover: Prover, verifier: Verifier) -> bool:
    # prover calculate s and build merkle tree
    s = prover.calculate_s()
    root, _ = prover.build_merkle_tree(s)
    # prover send merkle tree root to verifier
    root_hash = root.hash
    verifier.root_hash = root_hash
    # verifier pick a random line
    a, b = verifier.low_degree_test_receiver.pick_random_line()
    # sender
    univariate_polynomial = prover.low_degree_test_sender.univariate_polynomial(a, b)
    # reveal points authentications
    authentications = prover.authentications_of_line(a, b)
    # multi_evaluations = prover.low_degree_test_sender.query_multi_evaluations(a, b)
    # verifier check evaluations
    return verifier.check_authentications(univariate_polynomial, authentications)
