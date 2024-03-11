import random

from proof_args_zk.multivariate_lagrange_interpolation import (
    MultilinearLagrangeInterpolationPolynomial,
)
from proof_args_zk.sum_check_protocol import bool_array_to_int, int_to_bool_array


class Circuit:
    def __init__(self, depth, layers):
        self.depth = depth
        self.layers = layers
        self.ki = [layer.k for layer in layers]
        self.out = None

    def evaluate(self):
        for layer in reversed(self.layers):
            out = layer.evaluate()
        self.out = out
        return out

    def w(self, layer_index: int) -> int:
        return self.layers[layer_index].layer_output


class FanIn2Circuit(Circuit):

    # in_1, i
    def left_index(self, layer_index: int, gate_index: int) -> int:
        """返回layer_index+1层的左输入的索引"""
        if layer_index == self.depth - 1:
            # 输入层的左输入是空
            return None
        layer_i = self.layers[layer_index]
        layer_i1 = self.layers[layer_index + 1]
        return layer_i1.gates.index(
            layer_i.gates[gate_index].left.connected_from.belongs_to
        )

    # in_2, i
    def right_index(self, layer_index: int, gate_index: int) -> int:
        """返回layer_index+1层的右输入的索引"""
        if layer_index == self.depth - 1:
            return None
        layer_i = self.layers[layer_index]
        layer_i1 = self.layers[layer_index + 1]
        return layer_i1.gates.index(
            layer_i.gates[gate_index].right.connected_from.belongs_to
        )

    # mapping {0, 1}^k_i + 2 * k_i+1 -> {0,1}
    def mult_i(self, layer_index: int) -> list[int]:
        k_i = self.ki[layer_index]
        k_i1 = self.ki[layer_index + 1]
        # {0, 1}^k_i * {0, 1}^k_i+1 * {0, 1}^k_i+1 -> {0,1}

        result = [0 for _ in range(1 << (k_i + 2 * k_i1))]

        layer_i = self.layers[layer_index]
        for j in range(1 << k_i):
            gate_j = layer_i.gates[j]
            if gate_j.operation == "mul":
                left = self.left_index(layer_index, j)
                right = self.right_index(layer_index, j)
                index_arr = (
                    int_to_bool_array(j, k_i)
                    + int_to_bool_array(left, k_i1)
                    + int_to_bool_array(right, k_i1)
                )
                index = bool_array_to_int(index_arr)
                result[index] = 1
        return result

    def add_i(self, layer_index: int) -> list[int]:
        k_i = self.ki[layer_index]
        k_i1 = self.ki[layer_index + 1]
        result = [0 for _ in range(1 << (k_i + 2 * k_i1))]
        layer_i = self.layers[layer_index]
        for j in range(1 << k_i):
            gate_j = layer_i.gates[j]
            if gate_j.operation == "add":
                left = self.left_index(layer_index, j)
                right = self.right_index(layer_index, j)
                index_arr = (
                    int_to_bool_array(j, k_i)
                    + int_to_bool_array(left, k_i1)
                    + int_to_bool_array(right, k_i1)
                )
                index = bool_array_to_int(index_arr)
                result[index] = 1
        return result


class Gate:
    pass


class Pin:
    def __init__(self, belongs_to: Gate):
        self.value = None
        self.belongs_to = belongs_to


class GateInput(Pin):
    def __init__(self, belongs_to: Gate):
        super().__init__(belongs_to)
        self.connected_from = None  # type: GateOutput


class GateOutput(Pin):
    def __init__(self, belongs_to: Gate):
        super().__init__(belongs_to)
        self.connected_to = []  # type: list[GateInput]


class InputGate(Gate):
    def __init__(self, value):
        self.value = value
        self.out = GateOutput(self)
        self.out.value = value

    def __str__(self):
        return f"{self.value} -> {self.outputs}"

    def evaluate(self):
        return self.value


class FanIn2Gate:
    def __init__(self, operation, prime):
        self.operation = operation
        self.prime = prime
        self.left = GateInput(self)
        self.right = GateInput(self)
        self.out = GateOutput(self)

    def __str__(self):
        return f"{self.operation} -> {self.outputs}"

    def evaluate(self):
        if self.left.value is None or self.right.value is None:
            raise ValueError("Input value is not set")
        left = self.left.value
        right = self.right.value
        if self.operation == "add":
            evaluation = (left + right) % self.prime
        elif self.operation == "mul":
            evaluation = (left * right) % self.prime
        else:
            raise ValueError(f"Unknown operation: {self.operation}")
        self.out.value = evaluation
        return evaluation


class CircuiLayer:
    def __init__(self, k, gates, output_wires):
        self.k = k
        if 1 << k != len(gates):
            raise ValueError(f"Number of gates should be 2^k, got {len(gates)}")
        self.gates = gates
        # self.input_wires = input_wires
        self.output_wires = output_wires
        self.layer_output = None
        self.size = len(gates)

    def evaluate(self):
        result = [gate.evaluate() for gate in self.gates]
        for wire in self.output_wires:
            wire.evaluate()
        self.layer_output = result
        return result


class Wire:
    def __init__(self, from_pin, to_pin):
        # 创建的时候，就表示连接了
        self.from_pin = from_pin
        self.to_pin = to_pin
        from_pin.connected_to.append(to_pin)
        to_pin.connected_from = from_pin

    def evaluate(self):
        # 仅仅是传递值
        self.to_pin.value = self.from_pin.value


class GKRProver:
    def __init__(self, circuit: FanIn2Circuit):
        self.circuit = circuit
        # 公共输入其实已经在电路中了，电路的inputlayer的输入就是公共输入

        self.D0 = None

    def mi(self):
        pass

    def fri(self):
        pass


class GKRVerifier:
    def __init__(self, circuit: FanIn2Circuit):
        self.circuit = circuit
        self.ri = [None for _ in range(circuit.depth)]
        self.prime = circuit.layers[0].gates[0].prime

        self.D0 = None
        self.m0 = None

    def generate_ri(self, layer_index: int):
        ki = self.circuit.ki[layer_index]
        layer_ri = [random.randint(1, self.prime - 1) for _ in range(ki)]
        self.ri[layer_index] = layer_ri
        return layer_ri

    def calculate_m0(self, r0, D0):
        k0 = self.circuit.ki[0]
        D0_mle = MultilinearLagrangeInterpolationPolynomial(self.prime, D0, k0)
        D0_mle_r0 = D0_mle.evaluate(r0)
        self.m0 = D0_mle_r0
        self.D0 = D0
        return D0_mle_r0


def gkr(prover: GKRProver, verifier: GKRVerifier):
    # todo
    circuit = prover.circuit
    prime = circuit.layers[0].gates[0].prime
    # prover evaluate the circuit
    circuit.evaluate()
    # prover claim D_0 = W_0
    D0 = prover.circuit.w(0)
    prover.D0 = D0
    # verifier picks random r_0
    r0 = verifier.generate_ri(0)
    # verifier MLE(D_0)
    m0 = verifier.calculate_m0(r0, D0)
    # The remainder of the protocol is devoted to confirming that m0 = ˜W0(r0).

    for i in range(circuit.depth):
        pass
