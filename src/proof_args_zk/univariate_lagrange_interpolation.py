# possible characters
import math

m = 128


class Polynomial:
    def __init__(self, p: int):
        """

        Args:
            p (int): prime number
        """
        self.p = p

    def evaluate(self, x: int) -> int:
        raise NotImplementedError


class UnivariableLangrangeInterpolationPolynomial(Polynomial):
    def __init__(self, p: int, a: list[int]):
        """

        Args:
            p (int): prime number
            a (list[int]): list of integers
        """
        super().__init__(p)
        self.a = a

    def evaluate(self, x: int) -> int:
        result = 0
        for i in range(len(self.a)):
            term = self.a[i]
            for j in range(len(self.a)):
                if i != j:
                    term = (term * (x - j) * pow(i - j, -1, self.p)) % self.p
            result = (result + term) % self.p
        return result

    def evalate_fast(self, x: int) -> int:
        n = len(self.a)

        if x < n:
            return self.a[x]
        delta0 = 1
        for k in range(1, len(self.a)):
            delta0 = (delta0 * (x - k) * pow(0 - k, -1, self.p)) % self.p

        delta_i = delta0
        result = delta0 * self.a[0]

        for i in range(1, len(self.a)):
            delta_i = (
                delta_i
                * (x - (i - 1))
                * pow(x - i, -1, self.p)
                * pow(i, -1, self.p)
                * (-1 * (n - i))
                % self.p
            )
            result = (result + self.a[i] * delta_i % self.p) % self.p
        return result


def low_degree_extension(a: list[int], p, r) -> Polynomial:
    if not a:
        raise ValueError("a must not be empty")
    # p = prime_greater_than(pow(len(a), 2))

    poly = UnivariableLangrangeInterpolationPolynomial(p, a)
    # random r in Z_p
    # r = random.randint(0, p - 1)
    # return poly
    return poly.evalate_fast(r)


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, math.isqrt(n) + 1, 2):
        if n % i == 0:
            return False
    return True


def prime_greater_than(n: int) -> int:
    # find the first prime number greater than n
    if n < 2:
        return 2
    if n == 2:
        return 3
    n += 1
    if n % 2 == 0:
        n += 1
    while True:
        if is_prime(n):
            return n
        n += 2
