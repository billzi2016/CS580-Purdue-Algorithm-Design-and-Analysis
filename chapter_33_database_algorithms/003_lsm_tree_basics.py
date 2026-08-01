"""
LSM tree 基础：写入内存表，满后 flush 为有序 run，查询按新到旧查找。

意图：展示写优化存储的核心流程：memtable、SSTable/run、compact。
"""


class SimpleLSMTree:
    """教学版 LSM tree，只支持 put/get/delete 和全量 compaction。"""

    TOMBSTONE = object()

    def __init__(self, memtable_limit: int = 3) -> None:
        if memtable_limit <= 0:
            raise ValueError("memtable_limit 必须为正数")
        self.memtable_limit = memtable_limit
        self.memtable: dict[str, object] = {}
        self.runs: list[list[tuple[str, object]]] = []

    def put(self, key: str, value: str) -> None:
        """写入 key-value；先进入 memtable。"""

        self.memtable[key] = value
        self._flush_if_needed()

    def delete(self, key: str) -> None:
        """写入墓碑标记，表示删除。"""

        self.memtable[key] = self.TOMBSTONE
        self._flush_if_needed()

    def get(self, key: str) -> str | None:
        """按 memtable、新 run 到旧 run 的顺序查询。"""

        if key in self.memtable:
            value = self.memtable[key]
            return None if value is self.TOMBSTONE else str(value)
        for run in reversed(self.runs):
            position = self._binary_search_run(run, key)
            if position != -1:
                value = run[position][1]
                return None if value is self.TOMBSTONE else str(value)
        return None

    def compact(self) -> None:
        """合并所有 run，删除被覆盖值和墓碑。"""

        merged: dict[str, object] = {}
        for run in self.runs:
            for key, value in run:
                merged[key] = value
        self.runs = [
            [
                (key, value)
                for key, value in sorted(merged.items())
                if value is not self.TOMBSTONE
            ]
        ]

    def _flush_if_needed(self) -> None:
        if len(self.memtable) < self.memtable_limit:
            return
        self.runs.append(sorted(self.memtable.items()))
        self.memtable.clear()

    def _binary_search_run(self, run: list[tuple[str, object]], key: str) -> int:
        left, right = 0, len(run) - 1
        while left <= right:
            mid = (left + right) // 2
            if run[mid][0] == key:
                return mid
            if run[mid][0] < key:
                left = mid + 1
            else:
                right = mid - 1
        return -1


if __name__ == "__main__":
    lsm = SimpleLSMTree(memtable_limit=2)
    lsm.put("a", "1")
    lsm.put("b", "2")
    assert lsm.get("a") == "1"
    lsm.put("a", "3")
    assert lsm.get("a") == "3"
    lsm.delete("a")
    assert lsm.get("a") is None
    lsm.compact()
    assert lsm.get("b") == "2"

    print("003_lsm_tree_basics: all examples passed")
