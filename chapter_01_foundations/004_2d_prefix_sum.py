"""
文件意图：
    本文件手写实现二维前缀和，用于 O(1) 查询矩阵子区域和。

适用场景：
    矩阵静态不变，但需要多次查询任意矩形区域的元素和。

核心思想：
    prefix[r][c] 表示原矩阵左上角到 (r - 1, c - 1) 的区域和。
    查询矩形时使用容斥：总区域 - 上方区域 - 左侧区域 + 重复扣掉的左上区域。

预处理复杂度：
    O(mn)

单次查询复杂度：
    O(1)
"""


def build_2d_prefix_sum(matrix: list[list[int]]) -> list[list[int]]:
    """
    构建二维前缀和矩阵。

    参数：
        matrix: m x n 的整数矩阵。

    返回：
        (m + 1) x (n + 1) 的前缀和矩阵，第一行和第一列作为哨兵。
    """
    if not matrix or not matrix[0]:
        return [[0]]

    rows, cols = len(matrix), len(matrix[0])
    prefix = [[0] * (cols + 1) for _ in range(rows + 1)]

    for row in range(rows):
        for col in range(cols):
            prefix[row + 1][col + 1] = (
                matrix[row][col]
                + prefix[row][col + 1]
                + prefix[row + 1][col]
                - prefix[row][col]
            )

    return prefix


def region_sum(
    prefix: list[list[int]], top: int, left: int, bottom: int, right: int
) -> int:
    """
    查询闭矩形区域 [(top, left), (bottom, right)] 的元素和。

    边界要求：
        top <= bottom 且 left <= right。
    """
    if top > bottom or left > right:
        raise ValueError("矩形区域必须满足 top <= bottom 且 left <= right")

    return (
        prefix[bottom + 1][right + 1]
        - prefix[top][right + 1]
        - prefix[bottom + 1][left]
        + prefix[top][left]
    )


if __name__ == "__main__":
    matrix = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ]
    prefix = build_2d_prefix_sum(matrix)

    assert region_sum(prefix, 0, 0, 0, 0) == 1
    assert region_sum(prefix, 0, 0, 2, 2) == 45
    assert region_sum(prefix, 1, 1, 2, 2) == 28
    assert build_2d_prefix_sum([]) == [[0]]

    print("004_2d_prefix_sum: all examples passed")
