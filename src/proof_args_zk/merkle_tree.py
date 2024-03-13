import hashlib


class Node:
    def __init__(self, depth: int = 0) -> None:
        self.parent = None
        self.left = None
        self.right = None
        self.hash = None
        self.depth = depth
        # self.index = index


def md5_hash(byts: bytes) -> bytes:
    return hashlib.md5(byts)


def leaf_hash(s: str) -> str:
    return md5_hash(b"0" + s.encode()).hexdigest()


def inner_hash(left: str, right: str) -> str:
    return md5_hash(b"1" + left.encode() + right.encode()).hexdigest()


def grow_up(nodes: list[Node]) -> list[Node]:
    if len(nodes) == 1:
        return nodes
    new_nodes = []
    for i in range(0, len(nodes), 2):
        node = Node()
        node.left = nodes[i]
        nodes[i].parent = node
        if i + 1 == len(nodes):
            node.hash = node.left.hash
            node.depth = node.left.depth + 1
            new_nodes.append(node)
        else:
            node.right = nodes[i + 1]
            nodes[i + 1].parent = node
            node.hash = inner_hash(node.left.hash, node.right.hash)
            node.depth = node.left.depth + 1
            new_nodes.append(node)
    return grow_up(new_nodes)


def build_merkle_tree(s: list) -> tuple[Node, list[Node]]:
    """

    Args:
        s (list): list of strings

    Returns:
        tuple[Node, list[Node]]: root of the merkle tree and the leaves
    """
    leaves = [Node() for i in range(len(s))]
    for i, leaf in enumerate(leaves):
        leaf.hash = leaf_hash(s[i])

    root = grow_up(leaves)[0]
    return root, leaves


def reaveal_leaf(node: Node) -> list[str]:
    """

    Args:
        node (Node): leaf node

    Returns:
        list[str]: list of hashes from the leaf to the root
    """
    hashes = []
    while node:
        hashes.append(
            (
                node.hash,
                node.left.hash if node.left else None,
                node.right.hash if node.right else None,
            )
        )
        node = node.parent
    return hashes
