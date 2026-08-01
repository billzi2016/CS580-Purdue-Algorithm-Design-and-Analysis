"""手写 CDQ 分治：计算二维点的严格支配计数。"""


def cdq_dominance_counts(points: list[tuple[int, int]]) -> list[int]:
    """返回所有 x、y 都严格更小的点数，按输入顺序输出。"""
    ys = sorted({y for _, y in points})
    rank = {y: i + 1 for i, y in enumerate(ys)}
    bit = [0] * (len(ys) + 1)
    ans = [0] * len(points)
    groups = []
    for point in sorted((x, y, i) for i, (x, y) in enumerate(points)):
        if not groups or groups[-1][0][0] != point[0]:
            groups.append([point])
        else:
            groups[-1].append(point)

    def add(i, delta):
        while i < len(bit):
            bit[i] += delta
            i += i & -i

    def query(i):
        total = 0
        while i:
            total += bit[i]
            i -= i & -i
        return total

    def solve(left, right):
        if right - left <= 1:
            return
        middle = (left + right) // 2
        solve(left, middle)
        solve(middle, right)
        # 左半的 x 全小于右半；按 y 扫描才可用 Fenwick 查询严格更小 y。
        source = sorted(
            (p for group in groups[left:middle] for p in group), key=lambda p: p[1]
        )
        target = sorted(
            (p for group in groups[middle:right] for p in group), key=lambda p: p[1]
        )
        index = 0
        for _, y, original in target:
            while index < len(source) and source[index][1] < y:
                add(rank[source[index][1]], 1)
                index += 1
            ans[original] += query(rank[y] - 1)
        for _, y, _ in source[:index]:
            add(rank[y], -1)

    solve(0, len(groups))
    return ans


if __name__ == "__main__":
    assert cdq_dominance_counts([(1, 1), (2, 2), (3, 1), (4, 3)]) == [0, 1, 0, 3]
    assert cdq_dominance_counts([]) == []
    print("003_cdq_divide_and_conquer: all examples passed")
