"""基于本章 SHA-256 的 Merkle tree 教学实现；奇数层复制末叶，提供根与路径验证。"""

import importlib.util
from pathlib import Path


def _sha(data: bytes) -> bytes:
    spec = importlib.util.spec_from_file_location(
        "sha_core", Path(__file__).with_name("007_sha256_core.py")
    )
    module = importlib.util.module_from_spec(spec)
    if spec is None or spec.loader is None:
        raise RuntimeError("无法加载 SHA-256 实现")
    spec.loader.exec_module(module)
    return module.sha256_digest(data)


def merkle_root(leaves: list[bytes]) -> bytes:
    """对 bytes 叶先哈希再两两连接哈希，奇数节点复制自身；空树拒绝。"""
    if (
        not isinstance(leaves, list)
        or not leaves
        or any(not isinstance(x, bytes) for x in leaves)
    ):
        raise ValueError("leaves 必须是非空 bytes 列表")
    level = [_sha(x) for x in leaves]
    while len(level) > 1:
        if len(level) % 2:
            level.append(level[-1])
        level = [_sha(level[i] + level[i + 1]) for i in range(0, len(level), 2)]
    return level[0]


def merkle_proof(leaves: list[bytes], index: int) -> list[tuple[bytes, bool]]:
    """返回 (兄弟哈希, 兄弟是否在左侧) 路径，用于独立验证某个叶。"""
    if not isinstance(index, int) or not 0 <= index < len(leaves):
        raise ValueError("index 越界")
    level = [_sha(x) for x in leaves]
    proof = []
    while len(level) > 1:
        if len(level) % 2:
            level.append(level[-1])
        sibling = index ^ 1
        proof.append((level[sibling], sibling < index))
        level = [_sha(level[i] + level[i + 1]) for i in range(0, len(level), 2)]
        index //= 2
    return proof


def verify_merkle_proof(
    leaf: bytes, proof: list[tuple[bytes, bool]], root: bytes
) -> bool:
    """从叶哈希按左右方向折叠认证路径，结果等于 root 才通过。"""
    if not isinstance(leaf, bytes) or not isinstance(root, bytes):
        raise ValueError("leaf 和 root 必须是 bytes")
    value = _sha(leaf)
    for sibling, is_left in proof:
        if not isinstance(sibling, bytes) or not isinstance(is_left, bool):
            raise ValueError("proof 格式无效")
        value = _sha(sibling + value if is_left else value + sibling)
    return value == root


if __name__ == "__main__":
    leaves = [b"a", b"b", b"c"]
    root = merkle_root(leaves)
    assert verify_merkle_proof(b"b", merkle_proof(leaves, 1), root)
    assert not verify_merkle_proof(b"x", merkle_proof(leaves, 1), root)
    print("009_merkle_tree: all examples passed")
