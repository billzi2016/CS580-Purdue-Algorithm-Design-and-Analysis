"""
文件意图：手写实现表格型 Double Q-learning。
适用场景：希望减少普通 Q-learning 最大化目标过估计偏差的离线转移更新。
核心思想：维护两张 Q 表，使用一张选择下一动作，另一张评估该动作的价值。
输入输出：输入转移、动作表和交替更新选择，返回两张 Q 表。
时间复杂度：O(样本数乘下一状态动作数)。空间复杂度：O(状态动作对数)。
关键边界：终止转移 bootstrap 为零；更新选择必须是 0 或 1。
"""


def double_q_learning(
    transitions: list[tuple[str, str, float, str | None]],
    actions: dict[str, list[str]],
    update_tables: list[int],
    learning_rate: float,
    discount: float,
) -> tuple[dict[tuple[str, str], float], dict[tuple[str, str], float]]:
    """按 update_tables 指定的顺序执行 Double Q-learning。

    参数：每项转移为 (state, action, reward, next_state_or_none)；update_tables 对应每步选择更新 Q1(0) 或 Q2(1)。
    返回：更新后的 (Q1, Q2)。
    边界情况：终止下一状态不查询动作；样本数与更新选择长度不等或参数非法时抛出 ValueError。
    关键算法点：被更新表负责 argmax，另一张表提供该动作的 bootstrap 估值。
    """
    if len(transitions) != len(update_tables) or not 0 < learning_rate <= 1 or not 0 <= discount <= 1:
        raise ValueError("样本长度、学习率或折扣参数无效")
    first: dict[tuple[str, str], float] = {}
    second: dict[tuple[str, str], float] = {}
    for (state, action, reward, next_state), selected in zip(transitions, update_tables):
        if selected not in (0, 1):
            raise ValueError("更新选择只能是 0 或 1")
        updated, evaluator = (first, second) if selected == 0 else (second, first)
        target = reward
        if next_state is not None:
            choices = actions.get(next_state, [])
            if choices:
                best_action = choices[0]
                best_value = updated.get((next_state, best_action), 0.0)
                for candidate in choices[1:]:
                    candidate_value = updated.get((next_state, candidate), 0.0)
                    if candidate_value > best_value:
                        best_action, best_value = candidate, candidate_value
                target += discount * evaluator.get((next_state, best_action), 0.0)
        key = (state, action)
        updated[key] = updated.get(key, 0.0) + learning_rate * (target - updated.get(key, 0.0))
    return first, second


if __name__ == "__main__":
    q1, q2 = double_q_learning(
        [('B', 'right', 2.0, None), ('A', 'go', 0.0, 'B'), ('B', 'right', 4.0, None), ('A', 'go', 0.0, 'B')],
        {'B': ['left', 'right']},
        [0, 1, 1, 0],
        1.0,
        0.5,
    )
    assert q1[('B', 'right')] == 2.0 and q2[('B', 'right')] == 4.0
    assert q1[('A', 'go')] == 2.0 and q2[('A', 'go')] == 0.0
    print("010_double_q_learning: all examples passed")
