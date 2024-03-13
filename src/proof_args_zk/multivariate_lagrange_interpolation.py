class MultilinearPolynomial:
    def __init__(self, p: int):
        self.p = p

    def evaluate(self, x: list[int]) -> int:
        raise NotImplementedError


class MultilinearLagrangeInterpolationPolynomial(MultilinearPolynomial):
    """多线性拉格朗日插值多项式"""

    def __init__(self, p: int, a: list[int], v: int):
        """

        Args:
            p:
            a: 在插值点的值
            v: 变量个数

        """
        super().__init__(p)
        self.a = a
        self.v = v
        if len(a) != pow(2, v):
            raise ValueError("The length of a must be 2^l")
        self.multipliation_count = 0

    def evaluate(self, x: list[int]) -> int:
        if len(x) != self.v:
            raise ValueError("The length of x must be v")
        self.multipliation_count = 0

        result = 0
        for i in range(len(self.a)):
            result = (
                result + self.a[i] * self.evaluate_basis_polynomial(x, i)
            ) % self.p
            self.multipliation_count += 1
        return result

    def evaluate_basis_polynomial(self, x: list[int], w: int) -> int:
        """

        Args:
            x:
            w:
        """
        kai = 1
        for i in range(self.v):
            x_i = x[i]
            w_i = (w >> i) & 1  # 取出w的第i位
            kai = (kai * (x_i * w_i + (1 - x_i) * (1 - w_i))) % self.p
            self.multipliation_count += 3
        return kai

    def evaluate_fast(self, x: list[int]) -> int:
        # Vu
        # build table of kai_w
        # 用2阶举例子, 倒着遍历x, 从最高位开始
        # (1 - x1) * (1 - x2) | x1 * (1 - x2)| (1 - x1) * x2 | x1 * x2
        #          |                |                |            |
        #          ------------------                --------------
        #                   |                               |
        #                (1 - x2)          |                x2

        self.multipliation_count = 0
        x1 = x[self.v - 1]
        stage_table = [(1 - x1) % self.p, x1 % self.p]
        for stage in range(1, self.v):
            x_i = x[self.v - 1 - stage]
            new_stage_table = []
            for term in stage_table:
                new_stage_table.append(term * (1 - x_i) % self.p)
                new_stage_table.append(term * x_i % self.p)
                self.multipliation_count += 2
            stage_table = new_stage_table
        result = 0
        for i in range(len(self.a)):
            result = (result + self.a[i] * stage_table[i]) % self.p
            self.multipliation_count += 1
        return result

    def get_basis_polynomial(self, w: int):
        pass


def low_degree_multilinear_extension(a: list[int], r: list[int], v: int, p: int) -> int:
    return MultilinearLagrangeInterpolationPolynomial(p, a, v).evaluate(r)
