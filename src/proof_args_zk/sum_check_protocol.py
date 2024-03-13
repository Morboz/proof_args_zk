import copy
import random

from .utils import int_to_bool_array


class PolynomialTerm:
    def __init__(self, cofficient: int, v: int, degrees: list[int], p):
        self.cofficient = cofficient
        self.v = v
        self.degrees = degrees
        is_constant = all([x == 0 for x in degrees])
        self.is_constant = is_constant
        self.p = p
        vars = set()
        for i in range(v):
            if degrees[i] != 0:
                vars.add(i)
        self.vars = vars
        self.var_count = len(vars)

    def evaluate(self, x: list[int]) -> int:
        if self.is_constant:
            return self.cofficient
        if len(x) != self.v:
            raise ValueError("The length of x must be v")
        result = self.cofficient

        for i in range(self.v):
            result *= pow(x[i], self.degrees[i], self.p)
        return result % self.p

    def merge(self, other):
        if not isinstance(other, PolynomialTerm):
            raise ValueError("The other must be PolynomialTerm")
        if self.v != other.v or self.p != other.p:
            raise ValueError("The v and p must be the same")
        if self.degrees != other.degrees:
            raise ValueError("The degrees must be the same")
        return PolynomialTerm(
            (self.cofficient + other.cofficient) % self.p, self.v, self.degrees, self.p
        )

    def __str__(self) -> str:
        if self.is_constant:
            return str(self.cofficient)
        elif self.cofficient == 1:
            s = ""
        else:
            s = str(self.cofficient)
        for i, d in enumerate(self.degrees):
            if d == 0:
                continue
            if s:
                s += " * "
            if d == 1:
                s += f"x{i+1}"
            else:
                s += f"x{i+1}^{d}"
        return s


class CoefficientPolynomial:
    def __init__(self, p: int, terms: list[PolynomialTerm]):
        self.p = p
        self.terms = terms
        self.vars = set()
        for term in terms:
            self.vars = self.vars.union(term.vars)
        self.var_count = len(self.vars)
        self.v = terms[0].v

    def evaluate(self, x: list[int]) -> int:
        if isinstance(x, int) and self.var_count == 1:
            input_x = x
            x = [0 for _ in range(self.v)]
            x[copy.copy(self.vars).pop()] = input_x
        result = 0
        for term in self.terms:
            result = (result + term.evaluate(x)) % self.p
        return result % self.p

    def __str__(self) -> str:
        return " + ".join([str(term) for term in self.terms])

    def __add__(self, other):
        if not isinstance(other, CoefficientPolynomial):
            raise ValueError("The other must be Polynomial")
        if self.p != other.p:
            raise ValueError("The p must be the same")
        new_terms = copy.copy(self.terms)
        for term in other.terms:
            new_term_merged = False
            for t in new_terms:
                if t.degrees == term.degrees:
                    t.cofficient = (t.cofficient + term.cofficient) % t.p
                    new_term_merged = True
                    break
            if not new_term_merged:
                new_terms.append(term)
        return CoefficientPolynomial(self.p, new_terms)


def fix_some_variables_in_term(term: PolynomialTerm, x: list[int]) -> PolynomialTerm:
    if len(x) != term.v:
        raise ValueError(f"The length of x must be {term.v}")

    new_cofficient = term.cofficient
    new_degrees = copy.copy(term.degrees)
    for i in range(term.v):
        # new_cofficient *= pow(x[i], term.degrees[i], term.p)
        if x[i] is None:
            continue
        new_degrees[i] = 0
        new_cofficient *= pow(x[i], term.degrees[i])
    return PolynomialTerm(new_cofficient, term.v, new_degrees, term.p)


def fix_some_variables(
    poly: CoefficientPolynomial, x: list[int]
) -> CoefficientPolynomial:
    new_terms = []
    for term in poly.terms:
        new_term = fix_some_variables_in_term(term, x)
        new_term_merged = False
        for t in new_terms:
            if t.degrees == new_term.degrees:
                t.cofficient = (t.cofficient + new_term.cofficient) % t.p
                new_term_merged = True
                break
        if not new_term_merged:
            new_terms.append(new_term)
    return CoefficientPolynomial(poly.p, new_terms)


class Prover:
    def __init__(self, g, v: int):
        self.g = g
        # v 和 g的l 是一样的
        self.v = v

    def calculate_sum(self):
        sum_ = 0
        # for k in range(self.v):
        #     sum_ += self.g.evaluate([int(i == k) for i in range(self.v)])
        for i in range(1 << self.v):
            # change i to bool list
            b = int_to_bool_array(i, self.v)
            sum_ += self.g.evaluate(b)
        return sum_

    def get_g_i(self, i: int, r: list[int]) -> CoefficientPolynomial:
        """

        Args:
            i (int): ith variable, 0 <= i < v
            r (list[int]): length is i
        """
        if i < 0 or i >= self.v:
            raise ValueError("i out of range")
        if len(r) != i:
            raise ValueError("The length of r must be i")
        g_i = None
        for j in range(1 << (self.v - 1 - i)):
            b = int_to_bool_array(j, self.v - i - 1)
            p_i = fix_some_variables(self.g, r + [None] + b)
            if g_i is None:
                g_i = p_i
            else:
                g_i += p_i
        # g_i 是一个一元多项式
        if g_i.var_count != 1:
            raise ValueError("The var_count of g_i must be 1")
        return g_i


class Verifier:
    def __init__(
        self,
        g: CoefficientPolynomial,
    ):
        self.g = g
        self.r = [None for _ in range(self.g.v)]

    def evaluate_g(self, b: list[int]):
        return self.g.evaluate(b)

    def generate_r_i(self, i: int) -> list[int]:
        r_i = random.randint(self.g.v, self.g.p - 1)
        self.r[i] = r_i
        return r_i


def sum_check(prover, verifier) -> bool:
    # prover
    sum_ = prover.calculate_sum()
    g1 = prover.get_g_i(0, [])
    print(f"g1 -> {g1}")
    # verifier
    r = verifier.generate_r_i(0)
    if g1.evaluate(0) + g1.evaluate(1) != sum_:
        return False

    g_i_1 = g1

    for i in range(1, prover.v):
        # prover
        g_i = prover.get_g_i(i, verifier.r[:i])

        print(f"g_{i} -> {g_i}")
        # verifier check g_i-1(r_i-1) = g_i(0) + g_i(1)
        if g_i_1.evaluate(r) != (g_i.evaluate(0) + g_i.evaluate(1)) % verifier.g.p:
            return False
        # verifier generate r_i
        r = verifier.generate_r_i(i)
        g_i_1 = g_i

    if g_i.evaluate(verifier.r) != verifier.g.evaluate(verifier.r):
        return False

    return True
