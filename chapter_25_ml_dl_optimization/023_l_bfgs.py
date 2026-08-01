"""
L-BFGS：只保留最近 m 组 s/y 向量的有限内存 BFGS。
"""


Vector = list[float]


def objective(point: Vector) -> float:
    return (point[0] - 1.0) ** 2 + 2.0 * (point[1] + 2.0) ** 2


def gradient(point: Vector) -> Vector:
    return [2 * (point[0] - 1.0), 4 * (point[1] + 2.0)]


def l_bfgs_optimize(initial_point: Vector, learning_rate: float, memory: int, steps: int) -> list[Vector]:
    """执行二维教学版 L-BFGS。"""

    if len(initial_point) != 2 or learning_rate <= 0 or memory <= 0 or steps < 0:
        raise ValueError("参数范围非法")
    point = initial_point[:]
    s_history: list[Vector] = []
    y_history: list[Vector] = []
    history = [point[:]]
    for _ in range(steps):
        grad = gradient(point)
        direction = two_loop_recursion(grad, s_history, y_history)
        next_point = [point[i] - learning_rate * direction[i] for i in range(2)]
        s_vec = [next_point[i] - point[i] for i in range(2)]
        y_vec = [gradient(next_point)[i] - grad[i] for i in range(2)]
        s_history.append(s_vec)
        y_history.append(y_vec)
        if len(s_history) > memory:
            s_history.pop(0)
            y_history.pop(0)
        point = next_point
        history.append(point[:])
    return history


def two_loop_recursion(gradient_value: Vector, s_history: list[Vector], y_history: list[Vector]) -> Vector:
    """L-BFGS 的两层循环递推。"""

    q_vec = gradient_value[:]
    alphas: list[float] = []
    rhos: list[float] = []
    for s_vec, y_vec in zip(reversed(s_history), reversed(y_history), strict=True):
        ys = sum(y_vec[i] * s_vec[i] for i in range(2))
        rho = 0.0 if ys == 0 else 1.0 / ys
        alpha = rho * sum(s_vec[i] * q_vec[i] for i in range(2))
        q_vec = [q_vec[i] - alpha * y_vec[i] for i in range(2)]
        alphas.append(alpha)
        rhos.append(rho)
    r_vec = q_vec[:]
    for index, (s_vec, y_vec) in enumerate(zip(s_history, y_history, strict=True)):
        beta = rhos[-1 - index] * sum(y_vec[i] * r_vec[i] for i in range(2))
        r_vec = [r_vec[i] + s_vec[i] * (alphas[-1 - index] - beta) for i in range(2)]
    return r_vec


if __name__ == "__main__":
    history = l_bfgs_optimize([4.0, 2.0], learning_rate=0.2, memory=3, steps=6)
    assert objective(history[-1]) < objective(history[0])
    assert len(history) == 7

    print("023_l_bfgs: all examples passed")
