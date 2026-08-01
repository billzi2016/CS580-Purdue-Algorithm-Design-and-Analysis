"""
文件意图：定义并验证有限马尔可夫决策过程（MDP）的教学数据模型。
适用场景：为动态规划和表格型强化学习算法提供明确的状态、动作、转移与奖励接口。
核心思想：在给定状态和动作后，下一状态分布与即时奖励只依赖当前状态动作对。
输入输出：用状态列表、可行动作和转移结果构造 MDP，并查询动作或转移。
时间复杂度：构造验证 O(T)，T 为转移项数；查询 O(1) 到 O(分支数)。
空间复杂度：O(T)。
关键边界：终止状态可无动作；非终止状态每个动作的概率必须归一化为一。
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Transition:
    """表示一次状态转移的概率、下一状态和即时奖励。"""

    probability: float
    next_state: str
    reward: float


class FiniteMDP:
    """有限状态、有限动作的 MDP 教学模型。"""

    def __init__(
        self,
        states: list[str],
        actions: dict[str, list[str]],
        transitions: dict[tuple[str, str], list[Transition]],
        terminal_states: set[str] | None = None,
    ) -> None:
        """构造并验证一个有限 MDP。

        参数：states 是唯一状态名列表；actions 映射状态到可行动作；transitions 映射 (state, action) 到结果列表；terminal_states 为可选终止状态集合。
        返回：无。
        边界情况：终止状态可以没有动作；非终止状态的每个动作必须有概率和为一的结果。
        关键算法点：提前验证转移闭包和概率归一化，避免后续算法在错误模型上静默计算。
        """
        if not states or len(set(states)) != len(states):
            raise ValueError("states 必须是非空且不重复的列表")
        self.states = states[:]
        self._state_set = set(states)
        self.terminal_states = set() if terminal_states is None else set(terminal_states)
        if not self.terminal_states.issubset(self._state_set):
            raise ValueError("terminal_states 包含未知状态")
        self.actions = {state: choices[:] for state, choices in actions.items()}
        self.transitions = {key: outcomes[:] for key, outcomes in transitions.items()}
        self._validate()

    def _validate(self) -> None:
        """验证所有非终止状态动作与转移分布。"""
        for state in self.states:
            choices = self.actions.get(state, [])
            if state not in self.terminal_states and not choices:
                raise ValueError("非终止状态必须至少有一个动作")
            for action in choices:
                outcomes = self.transitions.get((state, action))
                if not outcomes:
                    raise ValueError("每个声明动作必须拥有转移结果")
                probability_sum = 0.0
                for outcome in outcomes:
                    if outcome.probability < 0 or outcome.next_state not in self._state_set:
                        raise ValueError("转移概率或下一状态无效")
                    probability_sum += outcome.probability
                if abs(probability_sum - 1.0) > 1e-9:
                    raise ValueError("每个动作的转移概率之和必须为 1")

    def available_actions(self, state: str) -> list[str]:
        """返回 state 的可行动作副本。

        参数：state 为已知状态名。
        返回：可行动作列表；终止状态通常返回空列表。
        边界情况：未知状态抛出 KeyError。
        关键算法点：返回副本避免调用者修改 MDP 内部动作表。
        """
        if state not in self._state_set:
            raise KeyError("未知状态")
        return self.actions.get(state, [])[:]

    def outcomes(self, state: str, action: str) -> list[Transition]:
        """返回执行 state、action 后的转移结果副本。

        参数：state 和 action 指定一个已声明状态动作对。
        返回：每项包含概率、下一状态和即时奖励。
        边界情况：未声明状态动作对抛出 KeyError。
        关键算法点：后续 Bellman 更新直接枚举此结果列表的期望回报。
        """
        key = (state, action)
        if key not in self.transitions:
            raise KeyError("未知状态动作对")
        return self.transitions[key][:]


if __name__ == "__main__":
    mdp = FiniteMDP(
        states=["start", "goal"],
        actions={"start": ["go"], "goal": []},
        transitions={("start", "go"): [Transition(1.0, "goal", 1.0)]},
        terminal_states={"goal"},
    )
    assert mdp.available_actions("start") == ["go"]
    assert mdp.outcomes("start", "go") == [Transition(1.0, "goal", 1.0)]
    assert mdp.available_actions("goal") == []
    print("001_markov_decision_process: all examples passed")
