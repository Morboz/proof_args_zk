from proof_args_zk.merkle_tree import build_merkle_tree, reaveal_leaf


def test_build_merkle_tree():
    root, leaves = build_merkle_tree(["hello", "world"])

    print(root.hash)
    print(leaves[0].hash)
    print(leaves[1].hash)

    leaf0_auth = reaveal_leaf(leaves[0])
    print(leaf0_auth)

    leaf1_auth = reaveal_leaf(leaves[1])
    print(leaf1_auth)


def test_build_merkle_tree2():
    root, leaves = build_merkle_tree(
        ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    )

    print(root.hash)
    leaf0_auth = reaveal_leaf(leaves[0])
    leaf1_auth = reaveal_leaf(leaves[1])
    assert leaf0_auth[1:] == leaf1_auth[1:]
    print(leaf0_auth)
    print(leaf1_auth)

    leaf2_auth = reaveal_leaf(leaves[2])
    assert leaf0_auth[2:] == leaf2_auth[2:]

    leaf8_auth = reaveal_leaf(leaves[8])
    leaf9_auth = reaveal_leaf(leaves[9])
    assert leaf8_auth[1:] == leaf9_auth[1:]
    assert leaf0_auth[-1] == leaf8_auth[-1]
