"""
文件意图：手写实现多臂 Bernoulli bandit 的 UCB1 选择与均值更新。
适用场景：在线探索利用权衡，奖励被规范化在 [0,1] 的多臂 bandit。
核心思想：先保证每个臂被尝试一次，再最大化经验均值加 sqrt(2 log t / n) 置信奖励。
输入输出：支持 select_arm 与 update。
时间复杂度：选择 O(K)，更新 O(1)。空间复杂度：O(K)。
关键边界：未尝试臂优先选择；奖励超出 [0,1] 被拒绝。
"""

import math


class UCBBandit:
    """使用 UCB1 规则的固定臂数 bandit。"""

    def __init__(self, arm_count: int) -> None:
        """创建 arm_count 个尚未尝试的臂。

        参数：arm_count 为正整数。
        返回：无。
        边界情况：非正臂数抛出 ValueError。
        关键算法点：分别维护每臂样本数和奖励和，均值无需保存为独立可变状态。
        """
        if arm_count <= 0:
            raise ValueError("arm_count 必须为正")
        self.counts = [0] * arm_count
        self.reward_sums = [0.0] * arm_count
        self.total_pulls = 0

    def select_arm(self) -> int:
        """返回当前 UCB1 值最大的臂。

        参数：无。
        返回：从零开始的臂编号。
        边界情况：存在未尝试臂时返回最小编号未尝试臂，避免除零且保证初始探索。
        关键算法点：已尝试臂的分数是经验均值与随样本数递减的置信奖励之和。
        """
        for arm, count in enumerate(self.counts):
            if count == 0:
                return arm
        best_arm = 0
        best_score = self._score(0)
        for arm in range(1, len(self.counts)):
            score = self._score(arm)
            if score > best_score:
                best_arm, best_score = arm, score
        return best_arm

    def _score(self, arm: int) -> float:
        """计算已尝试臂的 UCB1 分数。"""
        mean = self.reward_sums[arm] / self.counts[arm]
        return mean + math.sqrt(2.0 * math.log(self.total_pulls) / self.counts[arm])

    def update(self, arm: int, reward: float) -> None:
        """记录 arm 的一次 [0,1] 奖励观察。

        参数：arm 是有效臂编号，reward 在 [0,1]。
        返回：无。
        边界情况：非法臂或奖励抛出 ValueError。
        关键算法点：本次观察同时更新该臂均值分子和总试验轮数。
        """
        if arm < 0 or arm >= len(self.counts) or reward < 0 or reward > 1:
            raise ValueError("臂编号或奖励无效")
        self.counts[arm] += 1
        self.reward_sums[arm] += reward
        self.total_pulls += 1


if __name__ == "__main__":
    bandit = UCBBandit(2)
    assert bandit.select_arm() == 0
    bandit.update(0, 1.0)
    assert bandit.select_arm() == 1
    bandit.update(1, 0.0)
    assert bandit.select_arm() == 0
    print("014_upper_confidence_bound_bandit: all examples passed")
