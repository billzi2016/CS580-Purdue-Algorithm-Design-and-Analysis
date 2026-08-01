"""
文件意图：手写实现表格型 Dyna-Q 的真实经验与模型规划更新。
适用场景：可从环境交互中学习转移模型，并利用模型进行额外价值规划时。
核心思想：每个真实转移先更新 Q 与模型，再对已学习模型中的状态动作对执行规划 Q-learning 更新。
输入输出：输入真实转移及每步规划对，返回 Q 表和确定性模型表。
时间复杂度：O(真实样本数加规划更新数)。空间复杂度：O(状态动作对数)。
关键边界：终止转移下一状态为 None；规划对必须引用已由真实经验建立的模型项。
"""


def dyna_q(
    real_transitions: list[tuple[str, str, float, str | None]],
    actions: dict[str, list[str]],
    planning_pairs: list[list[tuple[str, str]]],
    learning_rate: float,
    discount: float,
) -> tuple[dict[tuple[str, str], float], dict[tuple[str, str], tuple[float, str | None]]]:
    """执行确定性模型的 Dyna-Q 更新。

    参数：real_transitions 是真实交互；planning_pairs[i] 是第 i 步真实交互后采用的模型状态动作对；actions 提供可行动作。
    返回：动作价值 Q 表和 (reward,next_state) 模型表。
    边界情况：规划批次数与真实样本数不等、参数非法或未知模型对时抛出 ValueError。
    关键算法点：真实与规划更新共用相同 Q-learning 备份，差异只在于样本来源。
    """
    if len(real_transitions) != len(planning_pairs) or not 0 < learning_rate <= 1 or not 0 <= discount <= 1:
        raise ValueError("输入长度、学习率或折扣参数无效")
    values: dict[tuple[str, str], float] = {}
    model: dict[tuple[str, str], tuple[float, str | None]] = {}

    def update(state: str, action: str, reward: float, next_state: str | None) -> None:
        """使用一条真实或模型转移执行 Q-learning 备份。"""
        target = reward
        if next_state is not None:
            choices = actions.get(next_state, [])
            if choices:
                best = values.get((next_state, choices[0]), 0.0)
                for next_action in choices[1:]:
                    best = max(best, values.get((next_state, next_action), 0.0))
                target += discount * best
        key = (state, action)
        values[key] = values.get(key, 0.0) + learning_rate * (target - values.get(key, 0.0))

    for transition, planned in zip(real_transitions, planning_pairs):
        state, action, reward, next_state = transition
        update(state, action, reward, next_state)
        model[(state, action)] = (reward, next_state)
        for planned_state, planned_action in planned:
            if (planned_state, planned_action) not in model:
                raise ValueError("规划对必须来自已学习模型")
            planned_reward, planned_next = model[(planned_state, planned_action)]
            update(planned_state, planned_action, planned_reward, planned_next)
    return values, model


if __name__ == "__main__":
    values, model = dyna_q(
        [('B', 'finish', 1.0, None), ('A', 'go', 0.0, 'B')],
        {'B': ['finish']},
        [[('B', 'finish')], [('A', 'go')]],
        1.0,
        0.9,
    )
    assert values == {('B', 'finish'): 1.0, ('A', 'go'): 0.9}
    assert model == {('B', 'finish'): (1.0, None), ('A', 'go'): (0.0, 'B')}
    print("011_dyna_q: all examples passed")
