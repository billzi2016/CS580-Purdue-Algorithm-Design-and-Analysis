"""
QR 分解：这里用 Gram-Schmidt 正交化。
"""

from math import sqrt


Vector = list[float]


def qr_decomposition(matrix: list[list[float]]) -> tuple[list[list[float]], list[list[float]]]:
    """对列向量做 Modified Gram-Schmidt，返回 Q 和 R。"""

    row_count = len(matrix)
    column_count = len(matrix[0])
    columns = [[matrix[row][column] for row in range(row_count)] for column in range(column_count)]
    q_columns: list[Vector] = []
    r_matrix = [[0.0] * column_count for _ in range(column_count)]
    for j in range(column_count):
        vector = columns[j][:]
        for i in range(j):
            # Modified Gram-Schmidt 对当前剩余向量逐步正交化，数值上比经典写法更稳。
            r_matrix[i][j] = dot(q_columns[i], vector)
            vector = [vector[k] - r_matrix[i][j] * q_columns[i][k] for k in range(row_count)]
        norm = sqrt(dot(vector, vector))
        if norm == 0:
            raise ValueError("列向量线性相关")
        r_matrix[j][j] = norm
        q_columns.append([value / norm for value in vector])
    q_matrix = [[q_columns[column][row] for column in range(column_count)] for row in range(row_count)]
    return q_matrix, r_matrix


def dot(left: Vector, right: Vector) -> float:
    return sum(x_value * y_value for x_value, y_value in zip(left, right, strict=True))


if __name__ == "__main__":
    q_matrix, r_matrix = qr_decomposition([[1.0, 1.0], [1.0, -1.0]])
    assert round(q_matrix[0][0], 6) == 0.707107
    assert round(r_matrix[0][0], 6) == 1.414214
    q_near, _ = qr_decomposition([[1.0, 1.0], [1.0, 1.000001]])
    dot_product = q_near[0][0] * q_near[0][1] + q_near[1][0] * q_near[1][1]
    assert abs(dot_product) < 1e-5

    print("016_qr_decomposition: all examples passed")
