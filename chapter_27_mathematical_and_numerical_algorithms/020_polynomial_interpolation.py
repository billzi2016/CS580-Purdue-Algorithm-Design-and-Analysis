"""
多项式插值：给出点集后构造通过所有点的多项式值计算器。
"""


def interpolate_by_vandermonde(xs: list[float], ys: list[float]) -> list[float]:
    """返回多项式系数，从常数项到高次项。"""

    if len(xs) != len(ys) or not xs:
        raise ValueError("xs 和 ys 必须等长且非空")
    if len(set(xs)) != len(xs):
        raise ValueError("插值节点 xs 必须两两不同")
    size = len(xs)
    matrix = [[xs[row] ** column for column in range(size)] for row in range(size)]
    return gaussian_elimination(matrix, ys)


def evaluate_polynomial(coefficients: list[float], x_value: float) -> float:
    """Horner 形式求值。"""

    result = 0.0
    for coefficient in reversed(coefficients):
        result = result * x_value + coefficient
    return result


def gaussian_elimination(matrix: list[list[float]], vector: list[float]) -> list[float]:
    size = len(vector)
    a_matrix = [row[:] for row in matrix]
    b_vector = vector[:]
    for pivot in range(size):
        best = max(range(pivot, size), key=lambda row: abs(a_matrix[row][pivot]))
        a_matrix[pivot], a_matrix[best] = a_matrix[best], a_matrix[pivot]
        b_vector[pivot], b_vector[best] = b_vector[best], b_vector[pivot]
        if a_matrix[pivot][pivot] == 0:
            raise ValueError("Vandermonde 矩阵奇异，无法求解唯一插值多项式")
        for row in range(pivot + 1, size):
            factor = a_matrix[row][pivot] / a_matrix[pivot][pivot]
            for column in range(pivot, size):
                a_matrix[row][column] -= factor * a_matrix[pivot][column]
            b_vector[row] -= factor * b_vector[pivot]
    result = [0.0] * size
    for row in range(size - 1, -1, -1):
        result[row] = (
            b_vector[row]
            - sum(a_matrix[row][col] * result[col] for col in range(row + 1, size))
        ) / a_matrix[row][row]
    return result


if __name__ == "__main__":
    coefficients = interpolate_by_vandermonde([0.0, 1.0, 2.0], [1.0, 2.0, 5.0])
    assert [round(value, 6) for value in coefficients] == [1.0, 0.0, 1.0]
    assert evaluate_polynomial(coefficients, 3.0) == 10.0
    try:
        interpolate_by_vandermonde([0.0, 1.0, 1.0], [1.0, 2.0, 3.0])
        raise AssertionError("重复插值点应触发异常")
    except ValueError:
        pass

    print("020_polynomial_interpolation: all examples passed")
