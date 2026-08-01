"""
Monte Carlo 积分。
"""

from random import Random


def monte_carlo_integration(
    function, left: float, right: float, samples: int, seed: int | None = None
) -> float:
    """用均匀采样估计一维积分。"""

    if samples <= 0:
        raise ValueError("samples 必须为正数")
    rng = Random(seed)
    total = 0.0
    for _ in range(samples):
        x_value = rng.uniform(left, right)
        total += function(x_value)
    return (right - left) * total / samples


if __name__ == "__main__":
    estimate = monte_carlo_integration(
        lambda x_value: x_value * x_value, 0.0, 1.0, 100000, seed=7
    )
    assert abs(estimate - 1 / 3) < 0.01

    print("011_monte_carlo_integration: all examples passed")
