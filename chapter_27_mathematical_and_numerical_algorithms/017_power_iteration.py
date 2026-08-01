"""
幂迭代：逼近矩阵主特征值和主特征向量。

意图：展示反复执行矩阵向量乘法并单位化，如何逼近绝对值最大的特征值和
对应特征向量。输入是方阵、非零初始向量和迭代步数。

时间复杂度：O(k n^2)，k 为迭代步数。空间复杂度：O(n)。
边界情况：矩阵必须是 n x n 方阵，初始向量不能为零，迭代中遇到零向量会失败。
"""

from math import sqrt


def power_iteration(
    matrix: list[list[float]], initial: list[float], steps: int
) -> tuple[float, list[float]]:
    """返回主特征值近似和单位化特征向量近似。

    参数：matrix 为方阵，initial 为初始向量，steps 为迭代次数。
    返回值：Rayleigh quotient 形式的特征值近似和单位化向量。
    关键算法点：每步单位化保留方向，避免向量范数指数级放大或缩小。
    """

    if steps < 0 or len(matrix) != len(initial):
        raise ValueError("参数范围非法")
    if any(len(row) != len(initial) for row in matrix):
        raise ValueError("matrix 必须是 n x n 方阵")
    if not initial:
        raise ValueError("initial 不能为空")
    vector = initial[:]
    initial_norm = sqrt(sum(value * value for value in vector))
    if initial_norm == 0:
        raise ValueError("initial 不能是零向量")
    vector = [value / initial_norm for value in vector]
    for _ in range(steps):
        next_vector = [
            sum(matrix[row][column] * vector[column] for column in range(len(vector)))
            for row in range(len(vector))
        ]
        norm = sqrt(sum(value * value for value in next_vector))
        if norm == 0:
            raise ValueError("幂迭代遇到零向量，输入矩阵或初始向量不适合继续迭代")
        vector = [value / norm for value in next_vector]
    numerator = sum(
        vector[row]
        * sum(matrix[row][column] * vector[column] for column in range(len(vector)))
        for row in range(len(vector))
    )
    return numerator, vector


if __name__ == "__main__":
    eigenvalue, eigenvector = power_iteration([[2.0, 0.0], [0.0, 1.0]], [1.0, 1.0], 10)
    assert round(eigenvalue, 6) == 1.999999
    assert eigenvector[0] > eigenvector[1]
    assert power_iteration([[3.0]], [2.0], 0)[0] == 3.0
    try:
        power_iteration([[0.0, 0.0], [0.0, 0.0]], [1.0, 0.0], 1)
        raise AssertionError("零矩阵应触发异常")
    except ValueError:
        pass
    try:
        power_iteration([[1.0], [2.0, 3.0]], [1.0, 1.0], 1)
        raise AssertionError("非方阵输入应触发异常")
    except ValueError:
        pass

    print("017_power_iteration: all examples passed")
