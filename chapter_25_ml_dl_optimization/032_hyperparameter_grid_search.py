"""
Grid Search：穷举离散超参数网格并选择最优配置。
"""

from itertools import product


def grid_search(
    space: dict[str, list[float]], score_function
) -> tuple[dict[str, float], float]:
    """遍历参数网格，返回最优参数和分数。"""

    if not space:
        raise ValueError("space 不能为空")
    names = list(space)
    values = [space[name] for name in names]
    best_params: dict[str, float] = {}
    best_score = float("-inf")
    for candidate in product(*values):
        params = dict(zip(names, candidate, strict=True))
        score = score_function(params)
        if score > best_score:
            best_score = score
            best_params = params
    return best_params, best_score


if __name__ == "__main__":
    params, score = grid_search(
        {"lr": [0.01, 0.1], "wd": [0.0, 0.1]},
        lambda item: -((item["lr"] - 0.1) ** 2) - item["wd"],
    )
    assert params == {"lr": 0.1, "wd": 0.0}
    assert score == 0.0

    print("032_hyperparameter_grid_search: all examples passed")
