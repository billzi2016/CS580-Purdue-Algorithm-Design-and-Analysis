"""
用有限差分近似梯度、Jacobian 和 Hessian。
"""


Vector = list[float]


def gradient(function, point: Vector, step: float = 1e-5) -> Vector:
    """计算标量函数的梯度。"""

    result: Vector = []
    for index in range(len(point)):
        plus = point[:]
        minus = point[:]
        plus[index] += step
        minus[index] -= step
        result.append((function(plus) - function(minus)) / (2 * step))
    return result


def jacobian(functions: list, point: Vector, step: float = 1e-5) -> list[Vector]:
    """计算向量函数的 Jacobian。"""

    return [gradient(function, point, step) for function in functions]


def hessian(function, point: Vector, step: float = 1e-4) -> list[Vector]:
    """计算标量函数的 Hessian。"""

    matrix: list[Vector] = []
    for row in range(len(point)):
        matrix_row: Vector = []
        for column in range(len(point)):
            shifts = [point[:] for _ in range(4)]
            shifts[0][row] += step
            shifts[0][column] += step
            shifts[1][row] += step
            shifts[1][column] -= step
            shifts[2][row] -= step
            shifts[2][column] += step
            shifts[3][row] -= step
            shifts[3][column] -= step
            value = (
                function(shifts[0])
                - function(shifts[1])
                - function(shifts[2])
                + function(shifts[3])
            ) / (4 * step * step)
            matrix_row.append(value)
        matrix.append(matrix_row)
    return matrix


if __name__ == "__main__":
    scalar = lambda point: point[0] ** 2 + point[0] * point[1] + point[1] ** 2
    grad = gradient(scalar, [1.0, 2.0])
    assert [round(value, 3) for value in grad] == [4.0, 5.0]
    jac = jacobian([lambda point: point[0] + point[1], lambda point: point[0] * point[1]], [2.0, 3.0])
    assert [[round(value, 3) for value in row] for row in jac] == [[1.0, 1.0], [3.0, 2.0]]
    hes = hessian(scalar, [1.0, 2.0])
    assert [[round(value, 1) for value in row] for row in hes] == [[2.0, 1.0], [1.0, 2.0]]

    print("002_gradient_jacobian_hessian: all examples passed")
