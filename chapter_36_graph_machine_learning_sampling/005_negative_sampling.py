"""
Negative Sampling：按词/节点频率分布抽取负样本。

意图：
- 手写 word2vec / 图表示学习中常用的 unigram^0.75 负采样。
- 排除正样本集合，避免把真实上下文当负例。
- 使用 seed 保证测试可复现。
"""

from random import Random


def negative_sampling(
    frequencies: dict[str, int],
    positive_items: set[str],
    sample_count: int,
    exponent: float = 0.75,
    seed: int | None = None,
) -> list[str]:
    """从频率分布中抽取负样本，允许重复抽样。"""

    if sample_count < 0:
        raise ValueError("sample_count 不能为负数")
    if exponent <= 0:
        raise ValueError("exponent 必须为正数")

    candidates = [item for item in sorted(frequencies) if item not in positive_items and frequencies[item] > 0]
    if not candidates and sample_count:
        raise ValueError("没有可用负样本候选")

    weights = [frequencies[item] ** exponent for item in candidates]
    rng = Random(seed)
    return [_weighted_choice(candidates, weights, rng) for _ in range(sample_count)]


def _weighted_choice(items: list[str], weights: list[float], rng: Random) -> str:
    """按 weights 从 items 中抽取一个元素。"""

    total = sum(weights)
    threshold = rng.random() * total
    cumulative = 0.0
    for item, weight in zip(items, weights, strict=True):
        cumulative += weight
        if cumulative >= threshold:
            return item
    return items[-1]


if __name__ == "__main__":
    frequencies = {"A": 10, "B": 1, "C": 5, "D": 20}
    samples = negative_sampling(frequencies, {"A"}, 5, seed=2)
    assert samples == ["D", "D", "B", "C", "D"]
    assert "A" not in samples
    assert negative_sampling(frequencies, set(), 0, seed=1) == []

    print("005_negative_sampling: all examples passed")
