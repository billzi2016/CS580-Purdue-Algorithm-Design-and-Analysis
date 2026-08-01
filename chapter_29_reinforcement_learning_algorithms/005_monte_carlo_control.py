"""
文件意图：手写 first-visit Monte Carlo 控制的动作价值更新。
适用场景：从完整带动作 episode 中估计 Q，并提取每个状态的贪心动作。
核心思想：首次访问的状态动作对以其完整折扣回报作样本平均。
输入输出：输入带奖励轨迹，返回 Q 表与贪心策略。
时间复杂度：O(总轨迹长度)。空间复杂度：O(访问过的状态动作对数)。
关键边界：空 episode 忽略；同价值时保留先出现动作以保持确定性。
"""


def monte_carlo_control(episodes: list[list[tuple[str, str, float]]], discount: float) -> tuple[dict[tuple[str, str], float], dict[str, str]]:
    """从完整 episode 估计动作价值并提取贪心策略。

    参数：轨迹项是 (state, action, reward_after_action)，discount 为折扣。
    返回：状态动作 Q 字典与访问状态的贪心动作字典。
    边界情况：空轨迹不产生 Q 项；非法折扣抛出 ValueError。
    关键算法点：first-visit 以状态动作对而非仅状态作为去重键。
    """
    if not 0 <= discount <= 1:
        raise ValueError("discount 必须在 [0, 1] 内")
    totals: dict[tuple[str, str], float] = {}
    counts: dict[tuple[str, str], int] = {}
    for episode in episodes:
        returns = [0.0] * len(episode)
        accumulated = 0.0
        for index in range(len(episode) - 1, -1, -1):
            accumulated = episode[index][2] + discount * accumulated
            returns[index] = accumulated
        seen: set[tuple[str, str]] = set()
        for index, (state, action, _) in enumerate(episode):
            key = (state, action)
            if key not in seen:
                seen.add(key)
                totals[key] = totals.get(key, 0.0) + returns[index]
                counts[key] = counts.get(key, 0) + 1
    values = {key: totals[key] / counts[key] for key in totals}
    policy: dict[str, str] = {}
    for (state, action), value in values.items():
        if state not in policy or value > values[(state, policy[state])]:
            policy[state] = action
    return values, policy


if __name__ == "__main__":
    values, policy = monte_carlo_control([[('S', 'left', 1.0)], [('S', 'right', 2.0)]], 1.0)
    assert values == {('S', 'left'): 1.0, ('S', 'right'): 2.0}
    assert policy == {'S': 'right'}
    print("005_monte_carlo_control: all examples passed")
