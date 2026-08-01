"""
文件意图：
    本文件用可执行函数展示贪心算法中的交换论证思想。

适用场景：
    需要说明“为什么局部最优选择不会损害全局最优”，例如区间调度、最小化等待时间等。

核心思想：
    如果某个最优解没有采用贪心选择，证明可以把它的第一步替换成贪心选择，
    且解的质量不变差；反复交换后得到包含贪心选择的最优解。

时间复杂度：
    取决于具体示例；本文件示例为 O(n log n)。

空间复杂度：
    O(n)
"""


def minimize_total_waiting_time(processing_times: list[int]) -> tuple[list[int], int]:
    """
    使用短作业优先顺序最小化总等待时间。

    参数：
        processing_times: 每个任务的处理时间，必须非负。

    返回：
        (schedule, total_waiting_time)。

    交换论证：
        若两个相邻任务 a > b，却让 a 排在 b 前，则交换后总等待时间减少 a - b。
        因此最优序列中处理时间必须非递减。
    """
    if any(time < 0 for time in processing_times):
        raise ValueError("处理时间必须非负")

    schedule = sorted(processing_times)
    elapsed = 0
    total_waiting_time = 0

    for processing_time in schedule:
        total_waiting_time += elapsed
        elapsed += processing_time

    return schedule, total_waiting_time


def adjacent_exchange_delta(first: int, second: int) -> int:
    """
    计算相邻任务从 [first, second] 交换成 [second, first] 后等待时间减少量。

    返回：
        first - second。若为正，说明把较短任务 second 放前面更优。
    """
    if first < 0 or second < 0:
        raise ValueError("处理时间必须非负")
    return first - second


if __name__ == "__main__":
    assert minimize_total_waiting_time([3, 1, 2]) == ([1, 2, 3], 4)
    assert minimize_total_waiting_time([]) == ([], 0)
    assert minimize_total_waiting_time([5]) == ([5], 0)
    assert adjacent_exchange_delta(10, 3) == 7
    assert adjacent_exchange_delta(2, 5) == -3

    try:
        minimize_total_waiting_time([1, -1])
        raise AssertionError("负处理时间必须抛出 ValueError")
    except ValueError:
        pass

    print("005_exchange_argument_examples: all examples passed")
