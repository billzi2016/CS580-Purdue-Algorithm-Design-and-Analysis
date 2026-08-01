"""
Nested-loop Join：双重循环连接。

意图：展示最直接的 join 执行算法；复杂度 O(|R|*|S|)，适合小表或有索引变体。
"""

from typing import Any


Row = dict[str, Any]


def nested_loop_join(
    left_rows: list[Row],
    right_rows: list[Row],
    left_key: str,
    right_key: str,
) -> list[Row]:
    """执行等值 nested-loop join。"""

    result: list[Row] = []
    for left in left_rows:
        for right in right_rows:
            if left[left_key] == right[right_key]:
                result.append(_merge_rows(left, right, "right_"))
    return result


def indexed_nested_loop_join(
    left_rows: list[Row],
    right_rows: list[Row],
    left_key: str,
    right_key: str,
) -> list[Row]:
    """构建右表 hash 索引后的 nested-loop join 变体。"""

    index: dict[Any, list[Row]] = {}
    for row in right_rows:
        index.setdefault(row[right_key], []).append(row)
    result: list[Row] = []
    for left in left_rows:
        for right in index.get(left[left_key], []):
            result.append(_merge_rows(left, right, "right_"))
    return result


def _merge_rows(left: Row, right: Row, right_prefix: str) -> Row:
    merged = dict(left)
    for key, value in right.items():
        output_key = key if key not in merged else right_prefix + key
        merged[output_key] = value
    return merged


if __name__ == "__main__":
    users = [{"id": 1, "name": "Ada"}, {"id": 2, "name": "Linus"}]
    orders = [{"user_id": 1, "item": "book"}, {"user_id": 1, "item": "pen"}]
    joined = nested_loop_join(users, orders, "id", "user_id")
    assert [row["item"] for row in joined] == ["book", "pen"]
    assert indexed_nested_loop_join(users, orders, "id", "user_id") == joined

    print("006_nested_loop_join: all examples passed")
