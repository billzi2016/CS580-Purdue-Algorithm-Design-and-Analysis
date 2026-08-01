"""
Hash Join：构建较小输入的 hash table，再探测另一侧。

意图：展示内存等值 join 的主力算法；只适合等值连接。
"""

from typing import Any


Row = dict[str, Any]


def hash_join(
    left_rows: list[Row], right_rows: list[Row], left_key: str, right_key: str
) -> list[Row]:
    """对较小表构建 hash table，然后执行等值连接。"""

    build_left = len(left_rows) <= len(right_rows)
    build_rows = left_rows if build_left else right_rows
    probe_rows = right_rows if build_left else left_rows
    build_key = left_key if build_left else right_key
    probe_key = right_key if build_left else left_key

    table: dict[Any, list[Row]] = {}
    for row in build_rows:
        table.setdefault(row[build_key], []).append(row)

    result: list[Row] = []
    for probe in probe_rows:
        for build in table.get(probe[probe_key], []):
            left, right = (build, probe) if build_left else (probe, build)
            result.append(_merge_rows(left, right))
    return result


def _merge_rows(left: Row, right: Row) -> Row:
    merged = dict(left)
    for key, value in right.items():
        merged[key if key not in merged else "right_" + key] = value
    return merged


if __name__ == "__main__":
    employees = [{"dept": "cs", "name": "A"}, {"dept": "math", "name": "B"}]
    depts = [{"dept": "cs", "building": "LWSN"}, {"dept": "bio", "building": "MJIS"}]
    assert hash_join(employees, depts, "dept", "dept") == [
        {"dept": "cs", "name": "A", "right_dept": "cs", "building": "LWSN"}
    ]

    print("007_hash_join: all examples passed")
