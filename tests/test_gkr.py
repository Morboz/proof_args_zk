import pytest

from proof_args_zk.gkr import (
    CircuiLayer,
    FanIn2Circuit,
    FanIn2Gate,
    GKRProver,
    GKRVerifier,
    InputGate,
    Wire,
    gkr,
)
from proof_args_zk.sum_check_protocol import int_to_bool_array


@pytest.fixture
def simple_circuit():
    depth = 3
    prime = 2**16 + 1

    input_gates = [InputGate(3), InputGate(2), InputGate(3), InputGate(1)]
    layer1_gates = [
        FanIn2Gate("mul", prime),
        FanIn2Gate("mul", prime),
        FanIn2Gate("mul", prime),
        FanIn2Gate("mul", prime),
    ]
    layer0_gates = [FanIn2Gate("mul", prime), FanIn2Gate("mul", prime)]

    input_layer_output_wires = [
        Wire(input_gates[0].out, layer1_gates[0].left),
        Wire(input_gates[0].out, layer1_gates[0].right),
        Wire(input_gates[1].out, layer1_gates[1].left),
        Wire(input_gates[1].out, layer1_gates[1].right),
        Wire(input_gates[1].out, layer1_gates[2].left),
        Wire(input_gates[2].out, layer1_gates[2].right),
        Wire(input_gates[3].out, layer1_gates[3].left),
        Wire(input_gates[3].out, layer1_gates[3].right),
    ]
    input_layer = CircuiLayer(2, input_gates, input_layer_output_wires)

    layer1_output_wires = [
        Wire(layer1_gates[0].out, layer0_gates[0].left),
        Wire(layer1_gates[1].out, layer0_gates[0].right),
        Wire(layer1_gates[2].out, layer0_gates[1].left),
        Wire(layer1_gates[3].out, layer0_gates[1].right),
    ]

    layer1 = CircuiLayer(2, layer1_gates, layer1_output_wires)

    layer2_output_wires = []
    layer0 = CircuiLayer(1, layer0_gates, layer2_output_wires)

    layers = [layer0, layer1, input_layer]
    return FanIn2Circuit(depth, layers)


def test_simple_circuit_evaluate(simple_circuit):
    circuit = simple_circuit
    assert circuit.evaluate() == [36, 6]
    assert circuit.layers[0].layer_output == [36, 6]
    assert circuit.layers[1].layer_output == [9, 4, 6, 1]
    assert circuit.layers[2].layer_output == [3, 2, 3, 1]

    assert circuit.left_index(0, 0) == 0
    assert circuit.left_index(0, 1) == 2
    assert circuit.right_index(0, 0) == 1
    assert circuit.right_index(0, 1) == 3

    assert circuit.left_index(1, 0) == 0
    assert circuit.left_index(1, 1) == 1
    assert circuit.left_index(1, 2) == 1
    assert circuit.left_index(1, 3) == 3
    assert circuit.right_index(1, 0) == 0
    assert circuit.right_index(1, 1) == 1
    assert circuit.right_index(1, 2) == 2
    assert circuit.right_index(1, 3) == 3

    assert circuit.left_index(2, 0) is None
    assert circuit.left_index(2, 1) is None
    assert circuit.left_index(2, 2) is None
    assert circuit.left_index(2, 3) is None
    assert circuit.right_index(2, 0) is None
    assert circuit.right_index(2, 1) is None
    assert circuit.right_index(2, 2) is None
    assert circuit.right_index(2, 3) is None

    mult_0 = circuit.mult_i(0)
    for i in range(len(mult_0)):
        print(int_to_bool_array(i, 5), mult_0[i])

    print("-----" * 20)
    mult_1 = circuit.mult_i(1)
    for i in range(len(mult_1)):
        print(int_to_bool_array(i, 6), mult_1[i])


def test_gkr(simple_circuit):
    circuit = simple_circuit
    prover = GKRProver(circuit)
    verifier = GKRVerifier(circuit)
    assert gkr(prover, verifier)
