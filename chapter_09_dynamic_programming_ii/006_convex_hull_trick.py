"""
文件意图：
    本文件手写实现单调斜率 Convex Hull Trick，用于优化形如 dp[i]=min(m*x_i+b) 的转移。

适用场景：
    直线斜率按单调顺序加入，查询 x 也按单调顺序增长。

核心思想：
    维护一个下凸壳。若新直线使中间直线永远不可能最优，则删除中间直线。

时间复杂度：
    均摊 O(1) 插入和查询（单调条件下）。

空间复杂度：
    O(n)
"""

Line = tuple[int, int]


class MonotonicConvexHullTrick:
    """单调斜率、单调查询的最小值 CHT。"""

    def __init__(self) -> None:
        self.lines: list[Line] = []
        self.pointer = 0

    def add_line(self, slope: int, intercept: int) -> None:
        """添加直线 y = slope * x + intercept，要求 slope 单调递减或递增且不破坏本例顺序。"""
        new_line = (slope, intercept)
        while len(self.lines) >= 2 and _is_bad(self.lines[-2], self.lines[-1], new_line):
            self.lines.pop()
        self.lines.append(new_line)
        self.pointer = min(self.pointer, len(self.lines) - 1)

    def query(self, x: int) -> int:
        """查询给定 x 下所有直线的最小 y 值，要求 x 单调不降。"""
        if not self.lines:
            raise ValueError("没有可查询的直线")
        while self.pointer + 1 < len(self.lines) and _value(self.lines[self.pointer + 1], x) <= _value(self.lines[self.pointer], x):
            self.pointer += 1
        return _value(self.lines[self.pointer], x)


def _value(line: Line, x: int) -> int:
    slope, intercept = line
    return slope * x + intercept


def _is_bad(first: Line, second: Line, third: Line) -> bool:
    """判断 second 是否在 first 和 third 之间变得永远不优。"""
    m1, b1 = first
    m2, b2 = second
    m3, b3 = third
    return (b3 - b1) * (m1 - m2) <= (b2 - b1) * (m1 - m3)


if __name__ == "__main__":
    cht = MonotonicConvexHullTrick()
    cht.add_line(5, 0)
    cht.add_line(3, 1)
    cht.add_line(1, 3)
    assert cht.query(0) == 0
    assert cht.query(1) == 4
    assert cht.query(10) == 13

    try:
        MonotonicConvexHullTrick().query(1)
        raise AssertionError("空 CHT 查询必须抛出 ValueError")
    except ValueError:
        pass

    print("006_convex_hull_trick: all examples passed")
