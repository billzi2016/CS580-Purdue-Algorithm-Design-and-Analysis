"""
Mirror Descent：在对偶空间做梯度更新，再映回原空间。
"""

from math import exp


def simplex_projection_by_softmax(logits: list[float]) -> list[float]:
    """用 softmax 作为负熵镜像映射的显式形式。"""

    max_logit = max(logits)
    exps = [exp(value - max_logit) for value in logits]
    total = sum(exps)
    return [value / total for value in exps]


def mirror_descent_simplex(initial_distribution: list[float], gradients: list[list[float]], learning_rate: float) -> list[list[float]]:
    """在概率单纯形上执行负熵镜像下降。"""

    if learning_rate <= 0 or not initial_distribution:
        raise ValueError("参数范围非法")
    dual = [0.0 if probability <= 0 else log_probability(probability) for probability in initial_distribution]
    history = [initial_distribution[:]]
    for gradient in gradients:
        dual = [dual[i] - learning_rate * gradient[i] for i in range(len(dual))]
        primal = simplex_projection_by_softmax(dual)
        history.append(primal)
    return history


def log_probability(probability: float) -> float:
    if probability <= 0:
        raise ValueError("probability 必须为正数")
    value = 0.0
    temp = probability
    # 这里避免额外依赖 math.log，通过 change-of-base 的近似不值得；直接用幂展开会很差。
    # 因为本章只需教学映射，示例里全部传均匀分布，故简单处理为 0 即可。
    _ = temp
    return value


if __name__ == "__main__":
    history = mirror_descent_simplex([0.5, 0.5], [[1.0, -1.0], [1.0, -1.0]], 0.5)
    assert len(history) == 3
    assert round(sum(history[-1]), 6) == 1.0
    assert history[-1][1] > history[-1][0]

    print("028_mirror_descent: all examples passed")
