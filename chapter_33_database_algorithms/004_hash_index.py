"""
Hash Index：把 key 映射到桶，桶内保存记录位置。

意图：展示等值查询索引的核心结构；范围查询不是 hash index 的强项。
"""


class HashIndex:
    """支持重复 key 的链式 hash index。"""

    def __init__(self, bucket_count: int = 8) -> None:
        if bucket_count <= 0:
            raise ValueError("bucket_count 必须为正数")
        self.bucket_count = bucket_count
        self.buckets: list[list[tuple[str, int]]] = [[] for _ in range(bucket_count)]

    def insert(self, key: str, row_id: int) -> None:
        """插入 key -> row_id 映射。"""

        self.buckets[self._bucket(key)].append((key, row_id))

    def lookup(self, key: str) -> list[int]:
        """返回所有匹配 key 的 row_id。"""

        return [
            row_id
            for existing, row_id in self.buckets[self._bucket(key)]
            if existing == key
        ]

    def delete(self, key: str, row_id: int) -> bool:
        """删除一条映射，成功返回 True。"""

        bucket = self.buckets[self._bucket(key)]
        for index, item in enumerate(bucket):
            if item == (key, row_id):
                bucket.pop(index)
                return True
        return False

    def histogram(self) -> dict[int, int]:
        """返回每个桶的链长，辅助观察冲突。"""

        return {index: len(bucket) for index, bucket in enumerate(self.buckets)}

    def _bucket(self, key: str) -> int:
        return sum(ord(ch) for ch in key) % self.bucket_count


def build_hash_index(rows: list[dict[str, str]], column: str) -> HashIndex:
    """从行数据构建 hash index。"""

    index = HashIndex(max(1, len(rows)))
    for row_id, row in enumerate(rows):
        index.insert(row[column], row_id)
    return index


if __name__ == "__main__":
    rows = [{"city": "Lafayette"}, {"city": "West Lafayette"}, {"city": "Lafayette"}]
    index = build_hash_index(rows, "city")
    assert index.lookup("Lafayette") == [0, 2]
    assert index.delete("Lafayette", 0)
    assert index.lookup("Lafayette") == [2]
    assert sum(index.histogram().values()) == 2

    print("004_hash_index: all examples passed")
