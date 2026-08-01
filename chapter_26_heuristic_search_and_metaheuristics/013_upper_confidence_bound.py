"""实现多臂老虎机的 UCB1 选择策略。

适用场景：在线探索—利用权衡与 MCTS 的子节点选择。核心思想：经验均值加上随访问次数下降的置信上界奖励。
输入输出：输入各臂累计回报和访问次数，输出应选择的臂下标。时间 O(K)，空间 O(1)。
边界：未访问臂优先返回；回报是测试样例，不是任何真实实验数据。
"""

from __future__ import annotations
import math


def ucb1_select(
    total_rewards: list[float], visits: list[int], exploration: float = math.sqrt(2)
) -> int:
    """按 UCB1 选择一个臂；未访问臂保证先被探索。"""
    if (
        not total_rewards
        or len(total_rewards) != len(visits)
        or any(count < 0 for count in visits)
    ):
        raise ValueError("回报与访问次数无效")
    for index, count in enumerate(visits):
        if count == 0:
            return index
    total = sum(visits)
    return max(
        range(len(visits)),
        key=lambda index: total_rewards[index] / visits[index]
        + exploration * math.sqrt(math.log(total) / visits[index]),
    )


if __name__ == "__main__":
    assert ucb1_select([10, 0], [5, 0]) == 1
    assert ucb1_select([9, 3], [3, 3], exploration=0) == 0
    print("013_upper_confidence_bound: all examples passed")
