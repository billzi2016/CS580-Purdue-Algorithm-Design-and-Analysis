"""
LayerNorm 优化数学：对单个样本内部特征归一化。
"""

from math import sqrt


def layer_norm_forward(
    values: list[list[float]], epsilon: float = 1e-5
) -> tuple[list[list[float]], list[float], list[float]]:
    """返回逐样本归一化结果及每行均值、方差。"""

    if not values or not values[0] or epsilon <= 0:
        raise ValueError("输入不能为空，epsilon 必须为正数")
    normalized: list[list[float]] = []
    means: list[float] = []
    variances: list[float] = []
    for row in values:
        mean = sum(row) / len(row)
        variance = sum((item - mean) ** 2 for item in row) / len(row)
        means.append(mean)
        variances.append(variance)
        denominator = sqrt(variance + epsilon)
        normalized.append([(item - mean) / denominator for item in row])
    return normalized, means, variances


if __name__ == "__main__":
    normalized, means, variances = layer_norm_forward([[1.0, 3.0], [2.0, 4.0]])
    assert means == [2.0, 3.0]
    assert variances == [1.0, 1.0]
    assert round(normalized[0][0], 6) == -0.999995

    print("020_layer_normalization_math: all examples passed")
