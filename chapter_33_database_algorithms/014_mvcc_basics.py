"""
MVCC 基础：每次写入生成新版本，读事务根据时间戳选择可见版本。

意图：展示多版本并发控制的核心可见性规则。
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Version:
    """一条记录的一个版本。deleted=True 表示删除墓碑。"""

    begin_ts: int
    value: str | None
    deleted: bool = False


class MVCCStore:
    """教学版 MVCC key-value 存储。"""

    def __init__(self) -> None:
        self.data: dict[str, list[Version]] = {}
        self.clock = 0

    def begin(self) -> int:
        """返回读事务快照时间戳。"""

        return self.clock

    def write(self, key: str, value: str) -> int:
        """写入新版本并返回提交时间戳。"""

        self.clock += 1
        self.data.setdefault(key, []).append(Version(self.clock, value))
        return self.clock

    def delete(self, key: str) -> int:
        """写入删除版本。"""

        self.clock += 1
        self.data.setdefault(key, []).append(Version(self.clock, None, True))
        return self.clock

    def read(self, key: str, read_ts: int) -> str | None:
        """读取 read_ts 时刻可见的最新版本。"""

        visible = None
        for version in self.data.get(key, []):
            if version.begin_ts <= read_ts:
                visible = version
            else:
                break
        if visible is None or visible.deleted:
            return None
        return visible.value


if __name__ == "__main__":
    store = MVCCStore()
    t0 = store.begin()
    store.write("x", "v1")
    t1 = store.begin()
    store.write("x", "v2")
    assert store.read("x", t0) is None
    assert store.read("x", t1) == "v1"
    assert store.read("x", store.begin()) == "v2"
    store.delete("x")
    assert store.read("x", store.begin()) is None

    print("014_mvcc_basics: all examples passed")
