"""
Random Search：在连续或离散搜索空间内随机采样超参数。
"""

from random import Random


def sample_uniform(low: float, high: float, rng: Random) -> float:
    if low > high:
        raise ValueError("low 不能大于 high")
    return rng.uniform(low, high)


def random_search(
    trials: int,
    seed: int,
    score_function,
) -> tuple[dict[str, float], float]:
    """随机采样学习率和权重衰减，返回最优结果。"""

    if trials < 0:
        raise ValueError("trials 不能为负数")
    rng = Random(seed)
    best_params = {"lr": 0.0, "wd": 0.0}
    best_score = float("-inf")
    for _ in range(trials):
        params = {
            "lr": sample_uniform(0.001, 0.2, rng),
            "wd": sample_uniform(0.0, 0.2, rng),
        }
        score = score_function(params)
        if score > best_score:
            best_score = score
            best_params = params
    return best_params, best_score


if __name__ == "__main__":
    params, score = random_search(
        20, 7, lambda item: -((item["lr"] - 0.1) ** 2) - item["wd"]
    )
    assert 0.001 <= params["lr"] <= 0.2
    assert 0.0 <= params["wd"] <= 0.2
    assert score <= 0.0

    print("033_random_search: all examples passed")
