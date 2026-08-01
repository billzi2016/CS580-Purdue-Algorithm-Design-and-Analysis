"""
文件意图：手写 first-visit Monte Carlo 策略评估。
适用场景：已收集完整 episode，且无需已知环境转移模型时估计状态价值。
核心思想：从 episode 末尾累积折扣回报，每个状态每条 episode 仅使用其首次访问的回报。
输入输出：输入状态奖励轨迹，返回平均回报价值表。
时间复杂度：O(总轨迹长度)。空间复杂度：O(状态数)。
关键边界：空 episode 被忽略；discount 必须在 [0,1]。
"""


def monte_carlo_prediction(episodes: list[list[tuple[str, float]]], discount: float) -> dict[str, float]:
    """用 first-visit Monte Carlo 估计状态价值。

    参数：每条轨迹的项为 (state, reward_after_visit)；discount 为折扣因子。
    返回：已访问状态的平均首次访问回报。
    边界情况：空轨迹不影响结果；非法折扣抛出 ValueError。
    关键算法点：倒序累计回报后，只在该状态本条轨迹第一次出现的位置记录样本。
    """
    if not 0 <= discount <= 1:
        raise ValueError("discount 必须在 [0, 1] 内")
    totals: dict[str, float] = {}
    counts: dict[str, int] = {}
    for episode in episodes:
        returns = [0.0] * len(episode)
        accumulated = 0.0
        for index in range(len(episode) - 1, -1, -1):
            accumulated = episode[index][1] + discount * accumulated
            returns[index] = accumulated
        seen: set[str] = set()
        for index, (state, _) in enumerate(episode):
            if state not in seen:
                seen.add(state)
                totals[state] = totals.get(state, 0.0) + returns[index]
                counts[state] = counts.get(state, 0) + 1
    return {state: totals[state] / counts[state] for state in totals}


if __name__ == "__main__":
    values = monte_carlo_prediction([[('A', 0.0), ('B', 1.0)], [('A', 2.0)]], 1.0)
    assert values == {'A': 1.5, 'B': 1.0}
    assert monte_carlo_prediction([[]], 0.9) == {}
    print("004_monte_carlo_prediction: all examples passed")
