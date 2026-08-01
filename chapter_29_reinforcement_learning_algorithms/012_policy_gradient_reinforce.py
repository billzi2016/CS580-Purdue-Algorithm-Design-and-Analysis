"""
文件意图：手写实现离散动作 softmax 策略的 REINFORCE 更新。
适用场景：仅有完整 episode 回报、没有环境模型时的蒙特卡罗策略梯度学习。
核心思想：对每步动作使用折扣回报加权 log pi(a|s) 的梯度；softmax 梯度为 one-hot 减概率。
输入输出：输入状态动作奖励轨迹与 logits 表，返回更新后的 logits。
时间复杂度：O(轨迹长度乘动作数)。空间复杂度：O(状态数乘动作数)。
关键边界：每个轨迹状态必须有动作 logits；非法动作、学习率或折扣会被拒绝。
"""

import math


def reinforce_update(
    episode: list[tuple[str, int, float]],
    logits: dict[str, list[float]],
    learning_rate: float,
    discount: float,
) -> dict[str, list[float]]:
    """对一个完整 episode 执行 REINFORCE logits 更新。

    参数：episode 项为 (state, action_index, reward_after_action)；logits 是每个状态的动作偏好；learning_rate、discount 为更新参数。
    返回：新的 logits 副本，输入字典及嵌套列表不会修改。
    边界情况：空 episode 原样返回；动作下标或参数非法时抛出 ValueError。
    关键算法点：先倒序计算每步回报，再使用动作 one-hot 与 softmax 概率的差作为 log 概率梯度。
    """
    if not 0 < learning_rate or not 0 <= discount <= 1:
        raise ValueError("学习率或折扣参数无效")
    updated = {state: values[:] for state, values in logits.items()}
    returns = [0.0] * len(episode)
    total = 0.0
    for index in range(len(episode) - 1, -1, -1):
        total = episode[index][2] + discount * total
        returns[index] = total
    for (state, action, _), return_value in zip(episode, returns):
        if (
            state not in updated
            or not updated[state]
            or action < 0
            or action >= len(updated[state])
        ):
            raise ValueError("状态 logits 或动作下标无效")
        maximum = max(updated[state])
        exponentials = [math.exp(value - maximum) for value in updated[state]]
        denominator = sum(exponentials)
        for index, exponential in enumerate(exponentials):
            probability = exponential / denominator
            gradient = (1.0 if index == action else 0.0) - probability
            updated[state][index] += learning_rate * return_value * gradient
    return updated


if __name__ == "__main__":
    updated = reinforce_update([("S", 1, 1.0)], {"S": [0.0, 0.0]}, 1.0, 1.0)
    assert updated["S"][1] > 0.0 and updated["S"][0] < 0.0
    assert reinforce_update([], {"S": [0.0]}, 0.1, 0.9) == {"S": [0.0]}
    print("012_policy_gradient_reinforce: all examples passed")
