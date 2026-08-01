"""
Bayesian Optimization 基础：用简单代理模型和采集函数选择下一个点。

文件意图：
- 这里只讲算法骨架，不引入高斯过程库。
- 用“离散候选点 + 已观测点均值/距离启发式”的极简代理，强调流程而非统计精度。
"""


def surrogate_mean(candidate: float, observations: list[tuple[float, float]]) -> float:
    """教学版代理均值：对最近观测做距离加权平均。"""

    if not observations:
        return 0.0
    numerator = 0.0
    denominator = 0.0
    for x_value, y_value in observations:
        weight = 1.0 / (abs(candidate - x_value) + 1e-6)
        numerator += weight * y_value
        denominator += weight
    return numerator / denominator


def upper_confidence_bound(
    candidate: float, observations: list[tuple[float, float]], exploration: float
) -> float:
    """极简 UCB：均值加上与最近观测距离相关的探索项。"""

    if exploration < 0:
        raise ValueError("exploration 不能为负数")
    if not observations:
        return exploration
    nearest = min(abs(candidate - x_value) for x_value, _ in observations)
    return surrogate_mean(candidate, observations) + exploration * nearest


def bayesian_optimization_step(
    candidates: list[float],
    observations: list[tuple[float, float]],
    exploration: float,
) -> float:
    """在离散候选集中选择下一评估点。"""

    if not candidates:
        raise ValueError("candidates 不能为空")
    return max(
        candidates,
        key=lambda candidate: upper_confidence_bound(
            candidate, observations, exploration
        ),
    )


if __name__ == "__main__":
    observations = [(0.0, 0.0), (1.0, 0.8)]
    next_x = bayesian_optimization_step([0.2, 0.5, 2.0], observations, exploration=0.5)
    assert next_x == 2.0
    assert round(surrogate_mean(0.5, observations), 6) == 0.4

    print("034_bayesian_optimization_basics: all examples passed")
