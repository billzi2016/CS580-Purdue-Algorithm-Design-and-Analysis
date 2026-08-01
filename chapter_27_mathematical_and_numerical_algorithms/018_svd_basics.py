"""
SVD 基础：对二维矩阵用 A^T A 的特征分解构造奇异值。

意图：教学展示 2x2 矩阵奇异值来自 A^T A 的非负特征值平方根。
输入是 2x2 实数矩阵，输出两个奇异值，按从大到小排列。

时间复杂度：O(1)。空间复杂度：O(1)。
边界情况：本文件只实现 2x2 基础版；其他尺寸或 ragged 输入会抛出 ValueError。
"""

from math import sqrt


def symmetric_2x2_eigenvalues(matrix: list[list[float]]) -> tuple[float, float]:
    """返回 2x2 对称矩阵的两个特征值。

    参数：matrix 必须是 2x2 对称矩阵；调用方负责保证对称性。
    返回值：两个实特征值，按较大值在前。
    关键算法点：直接使用二次特征方程，避免依赖线性代数库。
    """

    if len(matrix) != 2 or any(len(row) != 2 for row in matrix):
        raise ValueError("matrix 必须是 2x2 矩阵")
    trace = matrix[0][0] + matrix[1][1]
    determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    discriminant = sqrt(trace * trace - 4 * determinant)
    return (trace + discriminant) / 2, (trace - discriminant) / 2


def singular_values_2x2(matrix: list[list[float]]) -> tuple[float, float]:
    """返回 2x2 矩阵的两个奇异值。

    参数：matrix 是 2x2 实数矩阵。
    返回值：两个奇异值，按从大到小排列。
    边界情况：零矩阵返回两个 0。
    """

    if len(matrix) != 2 or any(len(row) != 2 for row in matrix):
        raise ValueError("matrix 必须是 2x2 矩阵")
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
    assert singular_values_2x2([[0.0, 0.0], [0.0, 0.0]]) == (0.0, 0.0)
    assert tuple(
        round(value, 6) for value in singular_values_2x2([[1.0, 0.0], [0.0, 1.0]])
    ) == (1.0, 1.0)
    try:
        singular_values_2x2([[1.0], [2.0, 3.0]])
        raise AssertionError("ragged 输入应触发异常")
    except ValueError:
        pass

    print("018_svd_basics: all examples passed")
