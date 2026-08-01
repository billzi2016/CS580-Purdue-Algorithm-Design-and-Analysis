"""
Bitmap Index：为低基数列的每个取值保存一张位图。

意图：展示 OLAP 查询中用位运算快速求交、求并的基本方法。
"""


class BitmapIndex:
    """低基数字段位图索引。"""

    def __init__(self, values: list[str]) -> None:
        self.row_count = len(values)
        self.bitmaps: dict[str, int] = {}
        for row_id, value in enumerate(values):
            self.bitmaps[value] = self.bitmaps.get(value, 0) | (1 << row_id)

    def equals(self, value: str) -> list[int]:
        """返回列值等于 value 的行号。"""

        return self._decode(self.bitmaps.get(value, 0))

    def in_values(self, values: set[str]) -> list[int]:
        """返回列值属于 values 的行号。"""

        bitmap = 0
        for value in values:
            bitmap |= self.bitmaps.get(value, 0)
        return self._decode(bitmap)

    def and_query(
        self, left_value: str, other: "BitmapIndex", right_value: str
    ) -> list[int]:
        """两个 bitmap index 的等值条件求交。"""

        return self._decode(
            self.bitmaps.get(left_value, 0) & other.bitmaps.get(right_value, 0)
        )

    def _decode(self, bitmap: int) -> list[int]:
        result: list[int] = []
        row_id = 0
        while bitmap:
            if bitmap & 1:
                result.append(row_id)
            bitmap >>= 1
            row_id += 1
        return result


if __name__ == "__main__":
    city = BitmapIndex(["A", "B", "A", "C", "B"])
    status = BitmapIndex(["open", "open", "closed", "open", "closed"])
    assert city.equals("A") == [0, 2]
    assert city.in_values({"A", "C"}) == [0, 2, 3]
    assert city.and_query("B", status, "closed") == [4]

    print("005_bitmap_index: all examples passed")
