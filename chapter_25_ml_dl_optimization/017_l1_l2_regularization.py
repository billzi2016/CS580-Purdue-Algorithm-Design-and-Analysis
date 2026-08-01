"""
L1/L2 正则：通过惩罚项约束参数规模，改善泛化。
"""


def l1_penalty(weights: list[float], lambda_l1: float) -> float:
    """返回 L1 正则项。"""

    if lambda_l1 < 0:
        raise ValueError("lambda_l1 不能为负数")
    return lambda_l1 * sum(abs(weight) for weight in weights)


def l2_penalty(weights: list[float], lambda_l2: float) -> float:
    """返回 0.5 * lambda * ||w||^2。"""

    if lambda_l2 < 0:
        raise ValueError("lambda_l2 不能为负数")
    return 0.5 * lambda_l2 * sum(weight * weight for weight in weights)


def l1_subgradient(weight: float, lambda_l1: float) -> float:
    """返回 L1 的一个常用次梯度。"""

    if weight > 0:
        return lambda_l1
    if weight < 0:
        return -lambda_l1
    return 0.0


def l2_gradient(weight: float, lambda_l2: float) -> float:
    """返回 L2 正则对单个参数的梯度。"""

    return lambda_l2 * weight


if __name__ == "__main__":
    weights = [1.0, -2.0, 0.5]
    assert abs(l1_penalty(weights, 0.1) - 0.35) < 1e-12
    assert abs(l2_penalty(weights, 0.2) - 0.525) < 1e-12
    assert l1_subgradient(-2.0, 0.1) == -0.1
    assert abs(l2_gradient(3.0, 0.2) - 0.6) < 1e-12

    print("017_l1_l2_regularization: all examples passed")
