"""
共轭梯度：求解对称正定线性系统 Ax=b。
"""

Vector = list[float]
Matrix = list[list[float]]


def conjugate_gradient(
    matrix: Matrix, vector: Vector, steps: int
) -> tuple[Vector, list[float]]:
    """从零向量开始求解，返回解和残差范数轨迹。"""

    if len(matrix) != len(vector) or steps < 0:
        raise ValueError("参数范围非法")
    solution = [0.0 for _ in vector]
    residual = vector[:]
    direction = residual[:]
    history = [squared_norm(residual)]
    for _ in range(steps):
        mat_dir = multiply(matrix, direction)
        denominator = dot(direction, mat_dir)
        if denominator == 0:
            break
        alpha = dot(residual, residual) / denominator
        solution = [solution[i] + alpha * direction[i] for i in range(len(vector))]
        next_residual = [residual[i] - alpha * mat_dir[i] for i in range(len(vector))]
        history.append(squared_norm(next_residual))
        if history[-1] == 0:
            residual = next_residual
            break
        beta = dot(next_residual, next_residual) / dot(residual, residual)
        direction = [next_residual[i] + beta * direction[i] for i in range(len(vector))]
        residual = next_residual
    return solution, history


def multiply(matrix: Matrix, vector: Vector) -> Vector:
    return [
        sum(item * component for item, component in zip(row, vector, strict=True))
        for row in matrix
    ]


def dot(left: Vector, right: Vector) -> float:
    return sum(x_value * y_value for x_value, y_value in zip(left, right, strict=True))


def squared_norm(vector: Vector) -> float:
    return dot(vector, vector)


if __name__ == "__main__":
    solution, residuals = conjugate_gradient(
        [[4.0, 1.0], [1.0, 3.0]], [1.0, 2.0], steps=3
    )
    assert round(solution[0], 6) == 0.090909
    assert round(solution[1], 6) == 0.636364
    assert residuals[-1] <= residuals[0]

    print("024_conjugate_gradient: all examples passed")
