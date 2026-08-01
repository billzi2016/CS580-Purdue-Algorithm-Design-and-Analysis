"""
Sort-merge Join：先按连接键排序，再线性合并。

意图：展示有序输入 join 如何处理重复键分组，适合范围友好的执行计划。
"""

from typing import Any


Row = dict[str, Any]


def sort_merge_join(left_rows: list[Row], right_rows: list[Row], left_key: str, right_key: str) -> list[Row]:
    """执行等值 sort-merge join。"""

    left = sorted(left_rows, key=lambda row: row[left_key])
    right = sorted(right_rows, key=lambda row: row[right_key])
    i = j = 0
    result: list[Row] = []

    while i < len(left) and j < len(right):
        left_value = left[i][left_key]
        right_value = right[j][right_key]
        if left_value < right_value:
            i += 1
        elif left_value > right_value:
            j += 1
        else:
            left_group = _collect_group(left, i, left_key)
            right_group = _collect_group(right, j, right_key)
            for lrow in left_group:
                for rrow in right_group:
                    result.append(_merge_rows(lrow, rrow))
            i += len(left_group)
            j += len(right_group)
    return result


def _collect_group(rows: list[Row], start: int, key: str) -> list[Row]:
    value = rows[start][key]
    end = start
    while end < len(rows) and rows[end][key] == value:
        end += 1
    return rows[start:end]


def _merge_rows(left: Row, right: Row) -> Row:
    merged = dict(left)
    for key, value in right.items():
        merged[key if key not in merged else "right_" + key] = value
    return merged


if __name__ == "__main__":
    left = [{"k": 2, "l": "b"}, {"k": 1, "l": "a"}]
    right = [{"k": 1, "r": "x"}, {"k": 2, "r": "y"}, {"k": 2, "r": "z"}]
    joined = sort_merge_join(left, right, "k", "k")
    assert [(row["l"], row["r"]) for row in joined] == [("a", "x"), ("b", "y"), ("b", "z")]

    print("008_sort_merge_join: all examples passed")
