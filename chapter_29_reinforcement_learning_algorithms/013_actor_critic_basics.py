"""
文件意图：手写实现表格 critic 与 softmax actor 的一步 Actor-Critic 更新。
适用场景：在线交互中同时学习状态价值基线与参数化离散策略。
核心思想：TD 误差既更新 critic 的 V(s)，也作为 actor 的近似优势权重。
输入输出：输入转移样本、价值表和 logits 表，返回更新后的两张表。
时间复杂度：O(样本数乘动作数)。空间复杂度：O(状态数乘动作数)。
关键边界：终止样本 next_state 为 None；状态 logits 或动作下标无效会被拒绝。
"""

import math


def actor_critic_update(
    transitions: list[tuple[str, int, float, str | None]],
    values: dict[str, float],
    logits: dict[str, list[float]],
    actor_learning_rate: float,
    critic_learning_rate: float,
    discount: float,
) -> tuple[dict[str, float], dict[str, list[float]]]:
    """对给定转移序列执行一步表格 Actor-Critic 更新。

    参数：项为 (state, action_index, reward, next_state_or_none)；values 与 logits 是初始表；两个学习率分别控制 actor 和 critic。
    返回：新的 (价值表, logits 表) 副本。
    边界情况：空样本保持原表；非法学习率、折扣、状态或动作抛出 ValueError。
    关键算法点：TD 误差 reward+gamma*V(s')-V(s) 是策略梯度的低方差优势近似。
    """
    if (
        not 0 < actor_learning_rate
        or not 0 < critic_learning_rate
        or not 0 <= discount <= 1
    ):
        raise ValueError("学习率或折扣参数无效")
    updated_values = values.copy()
    updated_logits = {state: row[:] for state, row in logits.items()}
    for state, action, reward, next_state in transitions:
        if (
            state not in updated_logits
            or not updated_logits[state]
            or action < 0
            or action >= len(updated_logits[state])
        ):
            raise ValueError("状态 logits 或动作下标无效")
        current = updated_values.get(state, 0.0)
        next_value = (
            updated_values.get(next_state, 0.0) if next_state is not None else 0.0
        )
        advantage = reward + discount * next_value - current
        updated_values[state] = current + critic_learning_rate * advantage
        maximum = max(updated_logits[state])
        exponentials = [math.exp(value - maximum) for value in updated_logits[state]]
        denominator = sum(exponentials)
        for index, exponential in enumerate(exponentials):
            gradient = (1.0 if index == action else 0.0) - exponential / denominator
            updated_logits[state][index] += actor_learning_rate * advantage * gradient
    return updated_values, updated_logits


if __name__ == "__main__":
    values, logits = actor_critic_update(
        [("S", 1, 2.0, None)], {}, {"S": [0.0, 0.0]}, 1.0, 0.5, 0.9
    )
    assert values == {"S": 1.0}
    assert logits["S"][1] > 0.0 and logits["S"][0] < 0.0
    print("013_actor_critic_basics: all examples passed")
