"""
文件意图：手写实现 Bernoulli bandit 的 Thompson sampling 后验维护与选择。
适用场景：奖励为 0/1 的多臂 bandit，需要基于不确定性进行概率匹配探索。
核心思想：每臂使用 Beta(alpha,beta) 后验，采样每个臂的成功率并选择最大样本。
输入输出：支持 select_arm 与 update。
时间复杂度：选择 O(K)，更新 O(1)。空间复杂度：O(K)。
关键边界：先验参数均为一；奖励必须严格为 0 或 1。
"""

import random


class ThompsonSamplingBandit:
    """使用 Beta-Bernoulli 后验的多臂 Thompson sampling bandit。"""

    def __init__(self, arm_count: int, seed: int = 0) -> None:
        """创建 arm_count 个 Beta(1,1) 先验臂。

        参数：arm_count 为正整数，seed 控制可复现的随机采样。
        返回：无。
        边界情况：非正臂数抛出 ValueError。
        关键算法点：alpha 累积成功次数加先验，beta 累积失败次数加先验。
        """
        if arm_count <= 0:
            raise ValueError("arm_count 必须为正")
        self.alpha = [1.0] * arm_count
        self.beta = [1.0] * arm_count
        self._random = random.Random(seed)

    def select_arm(self) -> int:
        """从各臂当前 Beta 后验采样并返回最大样本的臂编号。

        参数：无。
        返回：从零开始的臂编号。
        边界情况：相同样本时保留较小编号。
        关键算法点：随机后验样本把当前均值和不确定性共同编码进选择概率。
        """
        best_arm = 0
        best_sample = self._random.betavariate(self.alpha[0], self.beta[0])
        for arm in range(1, len(self.alpha)):
            sample = self._random.betavariate(self.alpha[arm], self.beta[arm])
            if sample > best_sample:
                best_arm, best_sample = arm, sample
        return best_arm

    def update(self, arm: int, reward: int) -> None:
        """以一次 Bernoulli 奖励更新 arm 的 Beta 后验。

        参数：arm 是有效编号，reward 必须为 0 或 1。
        返回：无。
        边界情况：非法臂或非二元奖励抛出 ValueError。
        关键算法点：共轭 Beta-Bernoulli 更新只需将成功加到 alpha、失败加到 beta。
        """
        if arm < 0 or arm >= len(self.alpha) or reward not in (0, 1):
            raise ValueError("臂编号或 Bernoulli 奖励无效")
        if reward == 1:
            self.alpha[arm] += 1.0
        else:
            self.beta[arm] += 1.0


if __name__ == "__main__":
    bandit = ThompsonSamplingBandit(2, seed=7)
    bandit.update(0, 1)
    bandit.update(1, 0)
    assert bandit.alpha == [2.0, 1.0] and bandit.beta == [1.0, 2.0]
    assert bandit.select_arm() in (0, 1)
    print("015_thompson_sampling: all examples passed")
