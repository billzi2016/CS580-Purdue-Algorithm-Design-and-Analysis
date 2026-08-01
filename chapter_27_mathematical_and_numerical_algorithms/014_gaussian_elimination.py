"""
Gaussian elimination：高斯消元求解线性方程组。

意图：教学展示带部分选主元的高斯消元，求解方阵线性系统 Ax=b。
输入是 n x n 系数矩阵和长度为 n 的右端向量，输出解向量。

时间复杂度：O(n^3)。空间复杂度：O(n^2)，因为会复制矩阵避免改动输入。
边界情况：空系统返回空解；非方阵、行长度不一致或奇异矩阵会抛出 ValueError。
"""


def gaussian_elimination(matrix: list[list[float]], vector: list[float]) -> list[float]:
    """用部分选主元高斯消元求解 Ax=b。

    参数：matrix 是方阵 A，vector 是右端项 b。
    返回值：解向量 x，使 Ax=b。
    关键算法点：每列选择当前列绝对值最大的可用行作为主元，降低除以小主元
    导致的不稳定风险。
    """

    if len(matrix) != len(vector):
        raise ValueError("矩阵维度与向量长度不匹配")
    n_value = len(vector)
    if any(len(row) != n_value for row in matrix):
        raise ValueError("matrix 必须是 n x n 方阵")
    a_matrix = [row[:] for row in matrix]
    b_vector = vector[:]
    for pivot in range(n_value):
        best = max(range(pivot, n_value), key=lambda row: abs(a_matrix[row][pivot]))
        a_matrix[pivot], a_matrix[best] = a_matrix[best], a_matrix[pivot]
        b_vector[pivot], b_vector[best] = b_vector[best], b_vector[pivot]
        if a_matrix[pivot][pivot] == 0:
            raise ValueError("矩阵奇异，无法求解")
        for row in range(pivot + 1, n_value):
            factor = a_matrix[row][pivot] / a_matrix[pivot][pivot]
            for column in range(pivot, n_value):
                a_matrix[row][column] -= factor * a_matrix[pivot][column]
            b_vector[row] -= factor * b_vector[pivot]
    solution = [0.0] * n_value
    for row in range(n_value - 1, -1, -1):
        remaining = sum(
            a_matrix[row][column] * solution[column]
            for column in range(row + 1, n_value)
        )
        solution[row] = (b_vector[row] - remaining) / a_matrix[row][row]
    return solution


if __name__ == "__main__":
    solution = gaussian_elimination([[2.0, 1.0], [1.0, 3.0]], [1.0, 2.0])
    assert [round(value, 6) for value in solution] == [0.2, 0.6]
    assert gaussian_elimination([], []) == []
    pivot_solution = gaussian_elimination([[0.0, 1.0], [2.0, 3.0]], [4.0, 8.0])
    assert [round(value, 6) for value in pivot_solution] == [-2.0, 4.0]
    try:
        gaussian_elimination([[1.0], [2.0, 3.0]], [1.0, 2.0])
        raise AssertionError("非方阵输入应触发异常")
    except ValueError:
        pass

    print("014_gaussian_elimination: all examples passed")
