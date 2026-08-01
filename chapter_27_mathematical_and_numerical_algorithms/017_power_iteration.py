"""
幂迭代：逼近矩阵主特征值和主特征向量。
"""

from math import sqrt


def power_iteration(matrix: list[list[float]], initial: list[float], steps: int) -> tuple[float, list[float]]:
    """返回主特征值近似和单位化特征向量近似。"""

    if steps < 0 or len(matrix) != len(initial):
        raise ValueError("参数范围非法")
    vector = initial[:]
    for _ in range(steps):
        next_vector = [sum(matrix[row][column] * vector[column] for column in range(len(vector))) for row in range(len(vector))]
        norm = sqrt(sum(value * value for value in next_vector))
        if norm == 0:
            raise ValueError("幂迭代遇到零向量，输入矩阵或初始向量不适合继续迭代")
        vector = [value / norm for value in next_vector]
    numerator = sum(
        vector[row] * sum(matrix[row][column] * vector[column] for column in range(len(vector)))
        for row in range(len(vector))
    )
    return numerator, vector


if __name__ == "__main__":
    eigenvalue, eigenvector = power_iteration([[2.0, 0.0], [0.0, 1.0]], [1.0, 1.0], 10)
    assert round(eigenvalue, 6) == 1.999999
    assert eigenvector[0] > eigenvector[1]
    try:
        power_iteration([[0.0, 0.0], [0.0, 0.0]], [1.0, 0.0], 1)
        raise AssertionError("零矩阵应触发异常")
    except ValueError:
        pass

    print("017_power_iteration: all examples passed")
