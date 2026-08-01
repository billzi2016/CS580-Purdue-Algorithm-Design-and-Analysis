"""
Merkle Tree Sync：用哈希树定位副本差异。

意图：分布式存储中先比较根哈希，根不同再递归定位不同叶子，减少传输。
"""

from hashlib import sha256


def merkle_root(items: list[str]) -> str:
    """计算字符串列表的 Merkle root。"""

    if not items:
        return _hash("")
    level = [_hash(item) for item in items]
    while len(level) > 1:
        level = [_hash(level[i] + (level[i + 1] if i + 1 < len(level) else level[i])) for i in range(0, len(level), 2)]
    return level[0]


def differing_indices(left: list[str], right: list[str]) -> list[int]:
    """教学版差异定位：用分治哈希比较两个等长列表。"""

    if len(left) != len(right):
        raise ValueError("两个副本长度必须相同")
    result: list[int] = []
    _diff_range(left, right, 0, len(left), result)
    return result


def _diff_range(left: list[str], right: list[str], start: int, end: int, result: list[int]) -> None:
    if start >= end:
        return
    if merkle_root(left[start:end]) == merkle_root(right[start:end]):
        return
    if end - start == 1:
        result.append(start)
        return
    mid = (start + end) // 2
    _diff_range(left, right, start, mid, result)
    _diff_range(left, right, mid, end, result)


def _hash(value: str) -> str:
    return sha256(value.encode("utf-8")).hexdigest()


if __name__ == "__main__":
    left = ["a", "b", "c", "d"]
    right = ["a", "B", "c", "D"]
    assert merkle_root(left) == merkle_root(left[:])
    assert differing_indices(left, right) == [1, 3]

    print("013_merkle_tree_sync: all examples passed")
