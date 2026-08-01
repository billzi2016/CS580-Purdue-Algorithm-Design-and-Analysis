"""共线种子锚点链的动态规划教学实现。

适用场景：将参考序列和查询序列中的精确种子命中连接为单调、近对角线的候选比对骨架。
核心思想：按参考坐标处理锚点；dp[i] 保存以第 i 个锚点结束的最佳链分数，前驱转移扣除两轴步长不一致的间隙代价。
输入输出：输入锚点、最大坐标跨度与间隙惩罚，输出分数最高的一条共线链及其总覆盖长度。
时间复杂度：O(a²)，a 为锚点数；空间复杂度 O(a)。本版为可读 DP，不采用 minimap2 的范围树或跳过启发式。
关键边界情况：零长度锚点、重叠锚点、逆序锚点均拒绝；无锚点返回空链；同分时采用确定性坐标顺序。
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class SeedAnchor:
    """一段两序列中长度相等的精确种子，坐标均为左闭右开。"""

    reference_start: int
    query_start: int
    length: int

    @property
    def reference_end(self) -> int:
        """返回参考序列上的开区间末端。"""
        return self.reference_start + self.length

    @property
    def query_end(self) -> int:
        """返回查询序列上的开区间末端。"""
        return self.query_start + self.length


@dataclass(frozen=True)
class SeedChain:
    """一条共线锚点链、其 DP 分数与不重叠锚点覆盖总长度。"""

    anchors: tuple[SeedAnchor, ...]
    score: int
    covered_bases: int


def chain_seeds(anchors: list[SeedAnchor], max_gap: int = 100, gap_penalty: int = 1) -> SeedChain:
    """用手写 O(a²) 动态规划选择一条高分共线锚点链。

    参数：anchors 是未排序精确种子；max_gap 限制相邻锚点任一轴的空档；gap_penalty 为每个对角线偏差单位的扣分。
    返回：分数最高的链；空输入返回 anchors 为空、分数零的链。
    边界情况：负参数、负坐标或非正长度抛出 ValueError；链中不允许两轴重叠或倒退。
    关键算法点：转移只允许 predecessor 的两个结束坐标均不超过当前起点，从而维持共线单调性。
    """
    _validate_inputs(anchors, max_gap, gap_penalty)
    if not anchors:
        return SeedChain((), 0, 0)
    ordered = sorted(anchors, key=lambda anchor: (anchor.reference_start, anchor.query_start, anchor.length))
    scores = [anchor.length for anchor in ordered]
    predecessors: list[int | None] = [None] * len(ordered)
    for current_index, current in enumerate(ordered):
        for previous_index in range(current_index):
            previous = ordered[previous_index]
            transition = _transition_score(previous, current, max_gap, gap_penalty)
            if transition is None:
                continue
            candidate = scores[previous_index] + current.length - transition
            # 严格大于才替换，确保同分时保留先出现（坐标更小）的可复现前驱。
            if candidate > scores[current_index]:
                scores[current_index] = candidate
                predecessors[current_index] = previous_index
    best_index = max(range(len(ordered)), key=lambda index: (scores[index], -ordered[index].reference_start, -ordered[index].query_start))
    path: list[SeedAnchor] = []
    cursor: int | None = best_index
    while cursor is not None:
        path.append(ordered[cursor])
        cursor = predecessors[cursor]
    path.reverse()
    return SeedChain(tuple(path), scores[best_index], sum(anchor.length for anchor in path))


def _transition_score(previous: SeedAnchor, current: SeedAnchor, max_gap: int, gap_penalty: int) -> int | None:
    """计算合法前驱的对角线间隙成本；不共线或太远时返回 None。"""
    reference_gap = current.reference_start - previous.reference_end
    query_gap = current.query_start - previous.query_end
    if reference_gap < 0 or query_gap < 0:
        return None
    if max(reference_gap, query_gap) > max_gap:
        return None
    # 同步前进的 gap 不惩罚；两轴距离差才提示插入/删除等非对角偏离。
    return gap_penalty * abs(reference_gap - query_gap)


def _validate_inputs(anchors: list[SeedAnchor], max_gap: int, gap_penalty: int) -> None:
    """验证锚点坐标与评分参数，避免不可能的种子默默进入 DP。"""
    if max_gap < 0 or gap_penalty < 0:
        raise ValueError("max_gap 和 gap_penalty 必须非负")
    for anchor in anchors:
        if anchor.reference_start < 0 or anchor.query_start < 0 or anchor.length <= 0:
            raise ValueError("锚点坐标必须非负且长度必须为正")


if __name__ == "__main__":
    anchors = [SeedAnchor(10, 11, 3), SeedAnchor(0, 0, 4), SeedAnchor(5, 5, 3), SeedAnchor(20, 2, 4)]
    chain = chain_seeds(anchors, max_gap=10)
    assert chain.anchors == (SeedAnchor(0, 0, 4), SeedAnchor(5, 5, 3), SeedAnchor(10, 11, 3))
    assert chain.score == 9
    assert chain.covered_bases == 10
    assert chain_seeds([]) == SeedChain((), 0, 0)
    assert chain_seeds([SeedAnchor(0, 0, 3), SeedAnchor(20, 20, 3)], max_gap=5).covered_bases == 3
    try:
        chain_seeds([SeedAnchor(-1, 0, 3)])
        raise AssertionError("应拒绝负坐标")
    except ValueError:
        pass
    print("021_seed_chaining: all examples passed")
