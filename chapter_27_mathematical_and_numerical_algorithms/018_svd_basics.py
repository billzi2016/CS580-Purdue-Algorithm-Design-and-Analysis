"""
SVD 基础：对二维矩阵用 A^T A 的特征分解构造奇异值。
"""

from math import sqrt


def symmetric_2x2_eigenvalues(matrix: list[list[float]]) -> tuple[float, float]:
    """返回 2x2 对称矩阵的两个特征值。"""

    trace = matrix[0][0] + matrix[1][1]
    determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    discriminant = sqrt(trace * trace - 4 * determinant)
    return (trace + discriminant) / 2, (trace - discriminant) / 2


def singular_values_2x2(matrix: list[list[float]]) -> tuple[float, float]:
    """返回 2x2 矩阵的两个奇异值。"""

    ata = [
        [
            matrix[0][0] ** 2 + matrix[1][0] ** 2,
            matrix[0][0] * matrix[0][1] + matrix[1][0] * matrix[1][1],
        ],
        [
            matrix[0][0] * matrix[0][1] + matrix[1][0] * matrix[1][1],
            matrix[0][1] ** 2 + matrix[1][1] ** 2,
        ],
    ]
    eigen1, eigen2 = symmetric_2x2_eigenvalues(ata)
    return sqrt(max(eigen1, 0.0)), sqrt(max(eigen2, 0.0))


if __name__ == "__main__":
    values = singular_values_2x2([[3.0, 0.0], [0.0, 4.0]])
    assert tuple(round(value, 6) for value in values) == (4.0, 3.0)

    print("018_svd_basics: all examples passed")
