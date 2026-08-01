"""
Volcano Iterator Model：open / next / close 查询执行接口。

意图：展示数据库算子如何像流水线一样逐行产出数据。
"""

from typing import Any, Protocol


Row = dict[str, Any]


class Operator(Protocol):
    """Volcano 算子接口。"""

    def open(self) -> None: ...
    def next(self) -> Row | None: ...
    def close(self) -> None: ...


class TableScan:
    """表扫描算子。"""

    def __init__(self, rows: list[Row]) -> None:
        self.rows = rows
        self.index = 0

    def open(self) -> None:
        self.index = 0

    def next(self) -> Row | None:
        if self.index >= len(self.rows):
            return None
        row = self.rows[self.index]
        self.index += 1
        return row

    def close(self) -> None:
        self.index = len(self.rows)


class Filter:
    """谓词过滤算子。"""

    def __init__(self, child: Operator, predicate) -> None:
        self.child = child
        self.predicate = predicate

    def open(self) -> None:
        self.child.open()

    def next(self) -> Row | None:
        while True:
            row = self.child.next()
            if row is None or self.predicate(row):
                return row

    def close(self) -> None:
        self.child.close()


def collect(operator: Operator) -> list[Row]:
    """执行算子并收集全部输出。"""

    result: list[Row] = []
    operator.open()
    while True:
        row = operator.next()
        if row is None:
            break
        result.append(row)
    operator.close()
    return result


if __name__ == "__main__":
    scan = TableScan([{"x": 1}, {"x": 2}, {"x": 3}])
    operator = Filter(scan, lambda row: row["x"] >= 2)
    assert collect(operator) == [{"x": 2}, {"x": 3}]

    print("011_volcano_iterator_model: all examples passed")
