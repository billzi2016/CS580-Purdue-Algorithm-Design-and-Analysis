"""
Gaussian elimination：高斯消元求解线性方程组。
"""


def gaussian_elimination(matrix: list[list[float]], vector: list[float]) -> list[float]:
    """用部分选主元高斯消元求解 Ax=b。"""

    if len(matrix) != len(vector):
        raise ValueError("矩阵维度与向量长度不匹配")
    n_value = len(vector)
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
        remaining = sum(a_matrix[row][column] * solution[column] for column in range(row + 1, n_value))
        solution[row] = (b_vector[row] - remaining) / a_matrix[row][row]
    return solution


if __name__ == "__main__":
    solution = gaussian_elimination([[2.0, 1.0], [1.0, 3.0]], [1.0, 2.0])
    assert [round(value, 6) for value in solution] == [0.2, 0.6]

    print("014_gaussian_elimination: all examples passed")
