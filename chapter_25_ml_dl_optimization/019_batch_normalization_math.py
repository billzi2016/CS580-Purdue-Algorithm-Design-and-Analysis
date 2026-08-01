"""
BatchNorm 优化数学：按 batch 维度归一化特征。
"""

from math import sqrt


def batch_norm_forward(
    values: list[list[float]], epsilon: float = 1e-5
) -> tuple[list[list[float]], list[float], list[float]]:
    """返回归一化结果、每列均值和方差。"""

    if not values or not values[0] or epsilon <= 0:
        raise ValueError("输入不能为空，epsilon 必须为正数")
    feature_count = len(values[0])
    means = []
    variances = []
    normalized = [[0.0] * feature_count for _ in values]
    for feature in range(feature_count):
        column = [row[feature] for row in values]
        mean = sum(column) / len(column)
        variance = sum((item - mean) ** 2 for item in column) / len(column)
        means.append(mean)
        variances.append(variance)
        denominator = sqrt(variance + epsilon)
        for row_index, item in enumerate(column):
            normalized[row_index][feature] = (item - mean) / denominator
    return normalized, means, variances


def running_stat_update(
    old_value: float, new_batch_value: float, momentum: float
) -> float:
    """BatchNorm 运行时统计的指数滑动平均更新。"""

    if not 0 <= momentum <= 1:
        raise ValueError("momentum 必须位于 [0,1]")
    return momentum * old_value + (1 - momentum) * new_batch_value


if __name__ == "__main__":
    normalized, means, variances = batch_norm_forward([[1.0, 2.0], [3.0, 4.0]])
    assert means == [2.0, 3.0]
    assert variances == [1.0, 1.0]
    assert round(normalized[0][0], 6) == -0.999995
    assert running_stat_update(10.0, 6.0, 0.9) == 9.6

    print("019_batch_normalization_math: all examples passed")
