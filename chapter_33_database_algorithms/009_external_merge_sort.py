"""
External Merge Sort：内存有限时的外部排序模型。

意图：用 run generation + k-way merge 展示数据库排序算子的核心流程。
这里用内存列表模拟磁盘 run，不做真实文件 I/O，避免无关副作用。
"""

from heapq import heappop, heappush


def external_merge_sort(values: list[int], memory_limit: int) -> list[int]:
    """在每个 run 最多 memory_limit 个元素的限制下排序。"""

    if memory_limit <= 0:
        raise ValueError("memory_limit 必须为正数")
    runs = [sorted(values[index : index + memory_limit]) for index in range(0, len(values), memory_limit)]
    return merge_sorted_runs(runs)


def merge_sorted_runs(runs: list[list[int]]) -> list[int]:
    """对多个有序 run 做 k-way merge。"""

    heap: list[tuple[int, int, int]] = []
    for run_id, run in enumerate(runs):
        if run:
            heappush(heap, (run[0], run_id, 0))

    result: list[int] = []
    while heap:
        value, run_id, offset = heappop(heap)
        result.append(value)
        next_offset = offset + 1
        if next_offset < len(runs[run_id]):
            heappush(heap, (runs[run_id][next_offset], run_id, next_offset))
    return result


def estimate_initial_run_count(row_count: int, memory_limit: int) -> int:
    """估算第一阶段产生多少个 run。"""

    if row_count < 0 or memory_limit <= 0:
        raise ValueError("row_count 不能为负，memory_limit 必须为正")
    return (row_count + memory_limit - 1) // memory_limit


if __name__ == "__main__":
    assert external_merge_sort([5, 1, 4, 2, 3], memory_limit=2) == [1, 2, 3, 4, 5]
    assert merge_sorted_runs([[1, 4], [2, 3], []]) == [1, 2, 3, 4]
    assert estimate_initial_run_count(10, 4) == 3

    print("009_external_merge_sort: all examples passed")
