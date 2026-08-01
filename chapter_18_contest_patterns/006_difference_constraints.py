"""文件意图：手写 Bellman-Ford 求差分约束最短上界。适用场景：形如 x_v-x_u<=w 的约束系统。核心思想：每条约束作为 u 到 v 权重 w 的边反复松弛。输入输出：返回满足约束的一组距离或 None。时间 O(VE)，空间 O(V)。关键边界：可达负环表示约束矛盾。"""


def solve_difference_constraints(
    vertex_count: int, constraints: list[tuple[int, int, int]]
) -> list[int] | None:
    """求解 x_v<=x_u+w 约束。
    参数：顶点数和 (u,v,w) 列表。返回一组可行上界；非法编号抛出 ValueError；通过超级源零距离使每个分量都参与检测。"""
    if vertex_count < 0 or any(
        u < 0 or v < 0 or u >= vertex_count or v >= vertex_count
        for u, v, _ in constraints
    ):
        raise ValueError("顶点编号无效")
    distance = [0] * vertex_count
    for _ in range(vertex_count):
        changed = False
        for source, target, weight in constraints:
            if distance[target] > distance[source] + weight:
                distance[target] = distance[source] + weight
                changed = True
        if not changed:
            return distance
    return None


if __name__ == "__main__":
    assert solve_difference_constraints(3, [(0, 1, 5), (1, 2, 2), (0, 2, 10)]) == [
        0,
        0,
        0,
    ]
    assert solve_difference_constraints(2, [(0, 1, -1), (1, 0, -1)]) is None
    print("006_difference_constraints: all examples passed")
