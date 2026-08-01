"""
Grace Hash Join：先分区，再对每个分区执行内存 hash join。

意图：展示当 build 表无法整体放入内存时，如何通过分区降低单次内存需求。
"""

from typing import Any


Row = dict[str, Any]


def grace_hash_join(
    left_rows: list[Row],
    right_rows: list[Row],
    left_key: str,
    right_key: str,
    partition_count: int,
) -> list[Row]:
    """执行 Grace hash join 的分区版等值连接。"""

    if partition_count <= 0:
        raise ValueError("partition_count 必须为正数")
    left_partitions = _partition(left_rows, left_key, partition_count)
    right_partitions = _partition(right_rows, right_key, partition_count)
    result: list[Row] = []
    for bucket in range(partition_count):
        result.extend(
            _hash_join_partition(
                left_partitions[bucket], right_partitions[bucket], left_key, right_key
            )
        )
    return result


def _partition(rows: list[Row], key: str, partition_count: int) -> list[list[Row]]:
    partitions: list[list[Row]] = [[] for _ in range(partition_count)]
    for row in rows:
        partitions[hash(row[key]) % partition_count].append(row)
    return partitions


def _hash_join_partition(
    left: list[Row], right: list[Row], left_key: str, right_key: str
) -> list[Row]:
    table: dict[Any, list[Row]] = {}
    for row in left:
        table.setdefault(row[left_key], []).append(row)
    result: list[Row] = []
    for row in right:
        for match in table.get(row[right_key], []):
            merged = dict(match)
            for key, value in row.items():
                merged[key if key not in merged else "right_" + key] = value
            result.append(merged)
    return result


if __name__ == "__main__":
    left = [{"id": 1, "name": "A"}, {"id": 2, "name": "B"}]
    right = [{"user_id": 2, "score": 9}, {"user_id": 1, "score": 7}]
    joined = grace_hash_join(left, right, "id", "user_id", partition_count=2)
    assert sorted((row["name"], row["score"]) for row in joined) == [("A", 7), ("B", 9)]

    print("010_grace_hash_join: all examples passed")
