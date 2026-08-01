"""
BFGS：用梯度差和步长差迭代近似 Hessian 逆矩阵。
"""

Vector = list[float]
Matrix = list[list[float]]


def quadratic_value(point: Vector) -> float:
    """目标函数 f(x,y)=(x-1)^2 + 2(y+2)^2。"""

    return (point[0] - 1.0) ** 2 + 2.0 * (point[1] + 2.0) ** 2


def quadratic_gradient(point: Vector) -> Vector:
    """目标函数梯度。"""

    return [2 * (point[0] - 1.0), 4 * (point[1] + 2.0)]


def bfgs_optimize(
    initial_point: Vector, learning_rate: float, steps: int
) -> list[Vector]:
    """执行教学版 BFGS，返回点轨迹。"""

    if len(initial_point) != 2 or learning_rate <= 0 or steps < 0:
        raise ValueError("参数范围非法")
    point = initial_point[:]
    inverse_hessian = [[1.0, 0.0], [0.0, 1.0]]
    history = [point[:]]
    for _ in range(steps):
        gradient = quadratic_gradient(point)
        direction = multiply_matrix_vector(
            inverse_hessian, [-gradient[0], -gradient[1]]
        )
        next_point = [point[i] + learning_rate * direction[i] for i in range(2)]
        s_vec = [next_point[i] - point[i] for i in range(2)]
        y_vec = [quadratic_gradient(next_point)[i] - gradient[i] for i in range(2)]
        ys = dot(y_vec, s_vec)
        if ys != 0:
            rho = 1.0 / ys
            identity = [[1.0, 0.0], [0.0, 1.0]]
            left = subtract_matrix(identity, scalar_outer_product(rho, s_vec, y_vec))
            right = subtract_matrix(identity, scalar_outer_product(rho, y_vec, s_vec))
            temp = multiply_matrix(multiply_matrix(left, inverse_hessian), right)
            inverse_hessian = add_matrix(temp, scalar_outer_product(rho, s_vec, s_vec))
        point = next_point
        history.append(point[:])
    return history


def dot(left: Vector, right: Vector) -> float:
    return sum(x_value * y_value for x_value, y_value in zip(left, right, strict=True))


def multiply_matrix_vector(matrix: Matrix, vector: Vector) -> Vector:
    return [
        sum(item * component for item, component in zip(row, vector, strict=True))
        for row in matrix
    ]


def scalar_outer_product(scale: float, left: Vector, right: Vector) -> Matrix:
    return [[scale * left[i] * right[j] for j in range(2)] for i in range(2)]


def multiply_matrix(left: Matrix, right: Matrix) -> Matrix:
    return [
        [sum(left[i][k] * right[k][j] for k in range(2)) for j in range(2)]
        for i in range(2)
    ]


def add_matrix(left: Matrix, right: Matrix) -> Matrix:
    return [[left[i][j] + right[i][j] for j in range(2)] for i in range(2)]


def subtract_matrix(left: Matrix, right: Matrix) -> Matrix:
    return [[left[i][j] - right[i][j] for j in range(2)] for i in range(2)]


if __name__ == "__main__":
    history = bfgs_optimize([4.0, 2.0], learning_rate=0.5, steps=5)
    assert quadratic_value(history[-1]) < quadratic_value(history[0])
    assert len(history) == 6

    print("022_quasi_newton_bfgs: all examples passed")
