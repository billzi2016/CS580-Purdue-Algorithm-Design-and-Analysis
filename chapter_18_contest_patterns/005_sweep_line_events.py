"""文件意图：手写事件扫描线计算区间最大重叠数。适用场景：会议室数量和活动并发度。核心思想：起点加一、终点减一并按坐标扫描。输入输出：返回最大同时活跃区间数。时间 O(nlogn)，空间 O(n)。关键边界：采用半开区间，端点相接不重叠。"""


def maximum_overlap(intervals: list[tuple[int, int]]) -> int:
    """返回半开区间的最大重叠数。
    参数：每项为 (start,end)。返回非负数量；start>end 抛出 ValueError；同坐标时先处理结束事件以符合半开语义。"""
    events = []
    for start, end in intervals:
        if start > end:
            raise ValueError("区间起点不能晚于终点")
        if start != end:
            events.append((start, 1))
            events.append((end, -1))
    for i in range(1, len(events)):
        current = events[i]
        j = i - 1
        while j >= 0 and events[j] > current:
            events[j + 1] = events[j]
            j -= 1
        events[j + 1] = current
    active = best = 0
    for _, delta in events:
        active += delta
        best = max(best, active)
    return best


if __name__ == "__main__":
    assert maximum_overlap([(1, 3), (2, 4), (3, 5)]) == 2
    assert maximum_overlap([(1, 1), (-1, 0)]) == 1
    print("005_sweep_line_events: all examples passed")
