"""
文件意图：手写实现表格型 Q-learning 更新。
适用场景：从探索行为数据学习贪心目标策略的 off-policy 控制。
核心思想：目标使用下一状态所有可行动作 Q 值的最大值。
输入输出：输入四元组转移与下一状态动作表，返回动作价值表。
时间复杂度：O(样本数乘下一状态动作数)。空间复杂度：O(状态动作对数)。
关键边界：终止转移没有下一状态，最大 bootstrap 项为零。
"""


def q_learning(
    transitions: list[tuple[str, str, float, str | None]],
    actions: dict[str, list[str]],
    learning_rate: float,
    discount: float,
) -> dict[tuple[str, str], float]:
    """按样本顺序执行 Q-learning 更新。

    参数：项为 (state, action, reward, next_state_or_none)，actions 提供每个状态的可行动作。
    返回：更新后的 Q 表。
    边界情况：终止 next_state 为 None；非法学习率或折扣抛出 ValueError。
    关键算法点：bootstrap 取 max_a Q(next_state,a)，因而目标不依赖实际下一动作。
    """
    if not 0 < learning_rate <= 1 or not 0 <= discount <= 1:
        raise ValueError("学习率或折扣参数无效")
    values: dict[tuple[str, str], float] = {}
    for state, action, reward, next_state in transitions:
        if next_state is None:
            best_next = 0.0
        else:
            best_next = 0.0
            choices = actions.get(next_state, [])
            if choices:
                best_next = values.get((next_state, choices[0]), 0.0)
                for next_action in choices[1:]:
                    best_next = max(best_next, values.get((next_state, next_action), 0.0))
        key = (state, action)
        values[key] = values.get(key, 0.0) + learning_rate * (reward + discount * best_next - values.get(key, 0.0))
    return values


if __name__ == "__main__":
    actions = {'A': ['go'], 'B': ['left', 'right']}
    q_values = q_learning([('B', 'right', 2.0, None), ('A', 'go', 0.0, 'B')], actions, 1.0, 0.9)
    assert q_values == {('B', 'right'): 2.0, ('A', 'go'): 1.8}
    print("008_q_learning: all examples passed")
