"""
文件意图：手写实现标准 Nim 游戏的必胜性判断与一手必胜策略构造。
适用场景：若干堆石子、每步从恰一堆取走正数个石子的公平组合游戏。
核心思想：所有堆大小的按位异或为 0 时局面必败；否则可减少某一堆使异或恢复为 0。
输入输出：输入非负堆大小列表，输出局面胜负及可执行的一手移动。
时间复杂度：O(n)，空间复杂度 O(1)，其中 n 为堆数。
关键边界情况：空局面和全零局面均为必败；负堆大小无意义并抛出异常。
"""


def nim_sum(heaps: list[int]) -> int:
    """计算标准 Nim 局面的异或和。

    参数：heaps 是每堆的非负石子数。
    返回：所有堆大小的按位异或结果。
    边界情况：空列表返回 0；出现负数抛出 ValueError。
    关键算法点：Nim 的 Sprague-Grundy 值正是各堆大小，组合游戏值由异或合并。
    """
    if any(heap < 0 for heap in heaps):
        raise ValueError("堆大小必须是非负整数")
    result = 0
    for heap in heaps:
        result ^= heap
    return result


def is_winning_position(heaps: list[int]) -> bool:
    """判断当前玩家在标准 Nim 局面是否有必胜策略。

    参数：heaps 是每堆的非负石子数。
    返回：异或和非零时返回真，否则返回假。
    边界情况：空局面返回假。
    关键算法点：异或和为零的局面任意走法都会变为非零，反之总能走到零。
    """
    return nim_sum(heaps) != 0


def winning_move(heaps: list[int]) -> tuple[int, int] | None:
    """构造一手将 Nim 异或和变为零的移动。

    参数：heaps 是每堆的非负石子数。
    返回：(堆下标，新堆大小)；若局面必败则返回 None。
    边界情况：全零或异或和为零时无必胜移动。
    关键算法点：对 heap 满足 (heap XOR total) < heap 时，将其减少到该目标值即可消去总异或。
    """
    total = nim_sum(heaps)
    if total == 0:
        return None
    for index, heap in enumerate(heaps):
        target = heap ^ total
        if target < heap:
            return index, target
    raise AssertionError("非零 Nim 异或和必须存在可减小的一堆")


if __name__ == "__main__":
    assert nim_sum([1, 2, 3]) == 0
    assert not is_winning_position([1, 2, 3])
    assert winning_move([1, 2, 3]) is None
    move = winning_move([3, 4, 5])
    assert move is not None
    changed = [3, 4, 5]
    changed[move[0]] = move[1]
    assert nim_sum(changed) == 0
    assert not is_winning_position([])
    print("001_nim: all examples passed")
