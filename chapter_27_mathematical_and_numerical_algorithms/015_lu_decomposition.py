"""
LU 分解：把矩阵分解为下三角 L 和上三角 U。
"""


def lu_decomposition(matrix: list[list[float]]) -> tuple[list[list[float]], list[list[float]]]:
    """Doolittle 形式 LU 分解。"""

    n_value = len(matrix)
    if any(len(row) != n_value for row in matrix):
        raise ValueError("矩阵必须是方阵")
    l_matrix = [[0.0] * n_value for _ in range(n_value)]
    u_matrix = [[0.0] * n_value for _ in range(n_value)]
    for index in range(n_value):
        l_matrix[index][index] = 1.0
    for column in range(n_value):
        for row in range(column + 1):
            u_matrix[row][column] = matrix[row][column] - sum(
                l_matrix[row][k] * u_matrix[k][column] for k in range(row)
            )
        for row in range(column + 1, n_value):
            if u_matrix[column][column] == 0:
                raise ValueError("零主元，需引入 pivoting")
            l_matrix[row][column] = (
                matrix[row][column] - sum(l_matrix[row][k] * u_matrix[k][column] for k in range(column))
            ) / u_matrix[column][column]
    return l_matrix, u_matrix


def multiply(left: list[list[float]], right: list[list[float]]) -> list[list[float]]:
    size = len(left)
    return [[sum(left[i][k] * right[k][j] for k in range(size)) for j in range(size)] for i in range(size)]


if __name__ == "__main__":
    l_matrix, u_matrix = lu_decomposition([[4.0, 3.0], [6.0, 3.0]])
    rebuilt = multiply(l_matrix, u_matrix)
    assert [[round(value, 6) for value in row] for row in rebuilt] == [[4.0, 3.0], [6.0, 3.0]]

    print("015_lu_decomposition: all examples passed")
