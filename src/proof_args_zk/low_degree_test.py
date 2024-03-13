# line versus point

import random

from proof_args_zk.univariate_lagrange_interpolation import (
    UnivariableLangrangeInterpolationPolynomial,
)


class Receiver:
    def __init__(self, p, v) -> None:
        self.p = p
        self.v = v

        self.univariate_polynomial = None
        self.random_line = None

    def pick_random_line(self) -> list[int]:
        a = [random.randint(0, self.p - 1) for _ in range(self.v)]
        b = [random.randint(0, self.p - 1) for _ in range(self.v)]

        self.random_line = a, b
        return a, b

    def func_l(self, t: int) -> list[int]:
        return [(self.random_line[i] * t) % self.p for i in range(self.v)]

    def evaluatations_of_univariate_polynomial(
        self,
        univariate_polynomial: UnivariableLangrangeInterpolationPolynomial,
    ) -> list[int]:
        evaluations = []
        for i in range(self.p):
            evaluations.append(univariate_polynomial.evaluate(i))
        return evaluations

    def check(
        self,
        univariate_polynomial: UnivariableLangrangeInterpolationPolynomial,
        multi_evaluations: list[int],
    ) -> bool:
        for ti in range(self.p):
            multi_eval_i = multi_evaluations[ti]
            uni_eval_i = univariate_polynomial.evaluate(ti)
            if multi_eval_i != uni_eval_i:
                return False
        return True


class Sender:
    def __init__(self, multilinear_polynomial) -> None:
        self.multilinear_polynomial = multilinear_polynomial
        self.p = multilinear_polynomial.p
        self.v = multilinear_polynomial.v

    def univariate_polynomial(
        self, a, b
    ) -> UnivariableLangrangeInterpolationPolynomial:
        u_interpolation = []
        degree = self.v

        def func_l(t: int) -> list[int]:
            return [(a[i] * t + b[i]) % self.p for i in range(degree)]

        for i in range(degree + 1):
            u_interpolation.append(self.multilinear_polynomial.evaluate(func_l(i)))
        return UnivariableLangrangeInterpolationPolynomial(self.p, u_interpolation)

    def query_multi_evaluations(self, a, b) -> list[int]:
        def func_l(t: int) -> list[int]:
            return [(a[i] * t + b[i]) % self.p for i in range(self.v)]

        multi_evaluations = []
        for i in range(self.p):
            multi_evaluations.append(self.multilinear_polynomial.evaluate(func_l(i)))
        return multi_evaluations


def low_degree_test(sender, receiver):
    # receiver pick a random line
    a, b = receiver.pick_random_line()  # x = at + b

    univariate_polynomial = sender.univariate_polynomial(a, b)
    multi_evaluations = sender.query_multi_evaluations(a, b)

    return receiver.check(univariate_polynomial, multi_evaluations)
