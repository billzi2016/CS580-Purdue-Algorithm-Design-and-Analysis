"""
文件意图：手写实现表格型 TD(0) 策略评估。
适用场景：交互尚未结束时在线估计状态价值。
核心思想：每一步用 reward + gamma*V(next_state) 作为一步 bootstrap 目标更新当前状态。
输入输出：输入转移样本与学习率，返回价值表。
时间复杂度：O(样本数)。空间复杂度：O(状态数)。
关键边界：终止转移的下一状态价值定义为零。
"""

Transition = tuple[str, float, str | None]


def td_zero_prediction(transitions: list[Transition], learning_rate: float, discount: float) -> dict[str, float]:
    """按给定时间顺序执行 TD(0) 状态价值更新。

    参数：项为 (state, reward, next_state_or_none)，learning_rate 在 (0,1]，discount 在 [0,1]。
    返回：更新后的状态价值表。
    边界情况：终止项 next_state 为 None；非法参数抛出 ValueError。
    关键算法点：目标使用当前下一状态估计，而不是等待完整 episode 回报。
    """
    if not 0 < learning_rate <= 1 or not 0 <= discount <= 1:
        raise ValueError("学习率或折扣参数无效")
    values: dict[str, float] = {}
    for state, reward, next_state in transitions:
        current = values.get(state, 0.0)
        target = reward + (discount * values.get(next_state, 0.0) if next_state is not None else 0.0)
        values[state] = current + learning_rate * (target - current)
    return values


if __name__ == "__main__":
    assert td_zero_prediction([('A', 0.0, 'B'), ('B', 1.0, None)], 1.0, 0.9) == {'A': 0.0, 'B': 1.0}
    assert td_zero_prediction([('A', 0.0, 'B'), ('B', 1.0, None), ('A', 0.0, 'B')], 1.0, 0.9)['A'] == 0.9
    print("006_temporal_difference_prediction: all examples passed")
