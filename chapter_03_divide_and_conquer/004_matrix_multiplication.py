"""
文件意图：
    本文件手写实现矩阵乘法的基础版本和分治版本，用于展示矩阵乘法的分块思想。

适用场景：
    需要理解矩阵乘法如何按象限拆分，以及分治算法如何组合子问题结果。

核心思想：
    对两个 n x n 矩阵按四个象限拆分。结果矩阵的每个象限由两个子矩阵乘积相加得到。
    为了让教学实现清晰，本文件支持任意矩形矩阵输入，并在分治前补零到 2 的幂大小。

输入输出：
    输入 A(m x k) 和 B(k x n)，返回 A * B。

时间复杂度：
    朴素乘法 O(mkn)；本文件的分治乘法仍为 O(n^3)，但展示分治结构。

空间复杂度：
    O(n^2)
"""

Matrix = list[list[int]]


def multiply_matrices_naive(left: Matrix, right: Matrix) -> Matrix:
    """
    使用三重循环手写矩阵乘法。
    """
    _validate_multiplication_shapes(left, right)

    rows = len(left)
    shared = len(right)
    cols = len(right[0])
    result = [[0] * cols for _ in range(rows)]

    for row in range(rows):
        for mid in range(shared):
            for col in range(cols):
                result[row][col] += left[row][mid] * right[mid][col]

    return result


def multiply_matrices_divide_and_conquer(left: Matrix, right: Matrix) -> Matrix:
    """
    使用分治方式计算矩阵乘法。

    说明：
        为了支持非 2 的幂大小，本函数先补零到方阵，再裁剪回真实结果大小。
    """
    _validate_multiplication_shapes(left, right)

    result_rows = len(left)
    shared = len(right)
    result_cols = len(right[0])
    size = _next_power_of_two(max(result_rows, shared, result_cols))

    padded_left = _pad_matrix(left, size, size)
    padded_right = _pad_matrix(right, size, size)
    padded_result = _multiply_square_recursive(padded_left, padded_right)

    return [row[:result_cols] for row in padded_result[:result_rows]]


def _multiply_square_recursive(left: Matrix, right: Matrix) -> Matrix:
    """
    递归计算两个同阶方阵乘积。
    """
    size = len(left)
    if size == 1:
        return [[left[0][0] * right[0][0]]]

    a11, a12, a21, a22 = _split_quadrants(left)
    b11, b12, b21, b22 = _split_quadrants(right)

    c11 = _add_matrices(
        _multiply_square_recursive(a11, b11), _multiply_square_recursive(a12, b21)
    )
    c12 = _add_matrices(
        _multiply_square_recursive(a11, b12), _multiply_square_recursive(a12, b22)
    )
    c21 = _add_matrices(
        _multiply_square_recursive(a21, b11), _multiply_square_recursive(a22, b21)
    )
    c22 = _add_matrices(
        _multiply_square_recursive(a21, b12), _multiply_square_recursive(a22, b22)
    )

    return _combine_quadrants(c11, c12, c21, c22)


def _validate_multiplication_shapes(left: Matrix, right: Matrix) -> None:
    """
    校验矩阵乘法形状是否合法。
    """
    if not left or not right or not left[0] or not right[0]:
        raise ValueError("矩阵不能为空")
    if any(len(row) != len(left[0]) for row in left):
        raise ValueError("左矩阵每一行长度必须一致")
    if any(len(row) != len(right[0]) for row in right):
        raise ValueError("右矩阵每一行长度必须一致")
    if len(left[0]) != len(right):
        raise ValueError("左矩阵列数必须等于右矩阵行数")


def _next_power_of_two(value: int) -> int:
    """
    返回大于等于 value 的最小 2 的幂。
    """
    size = 1
    while size < value:
        size *= 2
    return size


def _pad_matrix(matrix: Matrix, rows: int, cols: int) -> Matrix:
    """
    将矩阵补零到指定行列数。
    """
    padded = [[0] * cols for _ in range(rows)]
    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            padded[row][col] = matrix[row][col]
    return padded


def _split_quadrants(matrix: Matrix) -> tuple[Matrix, Matrix, Matrix, Matrix]:
    """
    将方阵拆成四个象限。
    """
    half = len(matrix) // 2
    top = matrix[:half]
    bottom = matrix[half:]
    return (
        [row[:half] for row in top],
        [row[half:] for row in top],
        [row[:half] for row in bottom],
        [row[half:] for row in bottom],
    )


def _add_matrices(left: Matrix, right: Matrix) -> Matrix:
    """
    逐元素相加两个同形矩阵。
    """
    return [
        [left[row][col] + right[row][col] for col in range(len(left[0]))]
        for row in range(len(left))
    ]


def _combine_quadrants(c11: Matrix, c12: Matrix, c21: Matrix, c22: Matrix) -> Matrix:
    """
    将四个象限合并为一个方阵。
    """
    top = [left_row + right_row for left_row, right_row in zip(c11, c12, strict=True)]
    bottom = [
        left_row + right_row for left_row, right_row in zip(c21, c22, strict=True)
    ]
    return top + bottom


if __name__ == "__main__":
    left_matrix = [[1, 2], [3, 4]]
    right_matrix = [[5, 6], [7, 8]]
    expected_square = [[19, 22], [43, 50]]
    assert multiply_matrices_naive(left_matrix, right_matrix) == expected_square
    assert (
        multiply_matrices_divide_and_conquer(left_matrix, right_matrix)
        == expected_square
    )

    rectangular_left = [[1, 2, 3], [4, 5, 6]]
    rectangular_right = [[7, 8], [9, 10], [11, 12]]
    expected_rectangular = [[58, 64], [139, 154]]
    assert (
        multiply_matrices_naive(rectangular_left, rectangular_right)
        == expected_rectangular
    )
    assert (
        multiply_matrices_divide_and_conquer(rectangular_left, rectangular_right)
        == expected_rectangular
    )

    try:
        multiply_matrices_naive([[1, 2]], [[1, 2]])
        raise AssertionError("非法矩阵形状必须抛出 ValueError")
    except ValueError:
        pass

    print("004_matrix_multiplication: all examples passed")
