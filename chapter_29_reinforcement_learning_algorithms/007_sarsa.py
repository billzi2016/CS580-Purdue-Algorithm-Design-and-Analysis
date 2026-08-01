"""
文件意图：手写实现表格型 SARSA 更新。
适用场景：需要按实际行为策略进行 on-policy 时序差分控制。
核心思想：用下一实际动作的 Q 值构造 reward+gamma*Q(s',a') 目标。
输入输出：输入五元组交互轨迹，返回动作价值表。
时间复杂度：O(样本数)。空间复杂度：O(状态动作对数)。
关键边界：终止转移的 next_action 为 None，bootstrap 项为零。
"""


def sarsa(
    transitions: list[tuple[str, str, float, str | None, str | None]],
    learning_rate: float,
    discount: float,
) -> dict[tuple[str, str], float]:
    """按样本顺序执行 SARSA 动作价值更新。

    参数：项为 (state, action, reward, next_state, next_action)；终止时后两项可为 None。
    返回：更新后的 Q 表。
    边界情况：学习率不在 (0,1] 或折扣不在 [0,1] 时抛出 ValueError。
    关键算法点：下一动作来自行为轨迹本身，因此是 on-policy 更新。
    """
    if not 0 < learning_rate <= 1 or not 0 <= discount <= 1:
        raise ValueError("学习率或折扣参数无效")
    values: dict[tuple[str, str], float] = {}
    for state, action, reward, next_state, next_action in transitions:
        key = (state, action)
        next_value = (
            values.get((next_state, next_action), 0.0)
            if next_state is not None and next_action is not None
            else 0.0
        )
        values[key] = values.get(key, 0.0) + learning_rate * (
            reward + discount * next_value - values.get(key, 0.0)
        )
    return values


if __name__ == "__main__":
    q_values = sarsa(
        [
            ("A", "go", 0.0, "B", "finish"),
            ("B", "finish", 1.0, None, None),
            ("A", "go", 0.0, "B", "finish"),
        ],
        1.0,
        0.9,
    )
    assert q_values == {("A", "go"): 0.9, ("B", "finish"): 1.0}
    print("007_sarsa: all examples passed")
