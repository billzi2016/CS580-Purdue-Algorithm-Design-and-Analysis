"""
文件意图：手写实现表格型 Expected SARSA 更新。
适用场景：已知下一状态行为策略分布，需以动作价值期望进行 on-policy 控制。
核心思想：目标使用 reward + gamma * sum_a pi(a|s')Q(s',a)，降低单动作采样方差。
输入输出：输入转移与策略分布，返回动作价值表。
时间复杂度：O(样本数乘下一状态动作数)。空间复杂度：O(状态动作对数)。
关键边界：终止状态的 bootstrap 为零；每个使用的策略概率必须归一化。
"""


def expected_sarsa(
    transitions: list[tuple[str, str, float, str | None]],
    policy: dict[str, dict[str, float]],
    learning_rate: float,
    discount: float,
) -> dict[tuple[str, str], float]:
    """按样本顺序执行 Expected SARSA 动作价值更新。

    参数：项为 (state, action, reward, next_state_or_none)；policy 映射状态到动作概率；learning_rate 和 discount 为更新参数。
    返回：更新后的 Q 表。
    边界情况：终止转移没有下一状态期望；概率缺失、非负性或归一化错误抛出 ValueError。
    关键算法点：下一状态目标是当前 Q 值在策略分布下的加权和，而非单动作或最大动作值。
    """
    if not 0 < learning_rate <= 1 or not 0 <= discount <= 1:
        raise ValueError("学习率或折扣参数无效")
    values: dict[tuple[str, str], float] = {}
    for state, action, reward, next_state in transitions:
        expected_value = 0.0
        if next_state is not None:
            distribution = policy.get(next_state)
            if not distribution:
                raise ValueError("非终止下一状态必须有策略分布")
            probability_sum = 0.0
            for next_action, probability in distribution.items():
                if probability < 0:
                    raise ValueError("策略概率不能为负")
                probability_sum += probability
                expected_value += probability * values.get(
                    (next_state, next_action), 0.0
                )
            if abs(probability_sum - 1.0) > 1e-9:
                raise ValueError("策略概率必须归一化")
        key = (state, action)
        values[key] = values.get(key, 0.0) + learning_rate * (
            reward + discount * expected_value - values.get(key, 0.0)
        )
    return values


if __name__ == "__main__":
    policy = {"B": {"left": 0.5, "right": 0.5}}
    q_values = expected_sarsa(
        [("B", "left", 2.0, None), ("B", "right", 4.0, None), ("A", "go", 0.0, "B")],
        policy,
        1.0,
        0.9,
    )
    assert q_values == {("B", "left"): 2.0, ("B", "right"): 4.0, ("A", "go"): 2.7}
    print("009_expected_sarsa: all examples passed")
