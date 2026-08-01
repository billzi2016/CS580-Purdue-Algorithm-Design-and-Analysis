"""
文件意图：手写实现有限 MDP 的策略迭代。
适用场景：已知完整模型时，通过交替策略评估和策略改进求最优确定性策略。
核心思想：固定策略时反复 Bellman 期望备份；评估收敛后把每个状态替换为贪心动作。
输入输出：输入有限状态动作转移模型，返回状态价值与稳定策略。
时间复杂度：每次评估迭代 O(T)，策略改进 O(T)，总轮数依赖模型。空间复杂度：O(S)。
关键边界：无动作状态被视为终止状态；非法参数或缺失动作转移会被拒绝。
"""

Transition = tuple[float, str, float]


def policy_iteration(
    states: list[str],
    actions: dict[str, list[str]],
    transitions: dict[tuple[str, str], list[Transition]],
    discount: float,
    tolerance: float = 1e-9,
    max_policy_iterations: int = 1_000,
    max_evaluation_iterations: int = 10_000,
) -> tuple[dict[str, float], dict[str, str | None]]:
    """求解有限 MDP 的最优确定性策略。

    参数：states、actions、transitions 描述有限模型；discount 在 [0,1)；两个最大迭代参数限制外层和内层循环。
    返回：近似最优价值字典和稳定贪心策略，终止状态的策略为 None。
    边界情况：无动作状态价值固定为零；非法参数、重复状态或缺失转移抛出 ValueError。
    关键算法点：只有策略评估充分收敛后才进行改进，稳定策略即满足 Bellman 最优性条件。
    """
    if (
        not 0 <= discount < 1
        or tolerance <= 0
        or max_policy_iterations <= 0
        or max_evaluation_iterations <= 0
    ):
        raise ValueError("迭代参数或 discount 无效")
    if len(set(states)) != len(states):
        raise ValueError("states 不能重复")
    state_set = set(states)

    def expected_return(state: str, action: str, values: dict[str, float]) -> float:
        outcomes = transitions.get((state, action))
        if not outcomes:
            raise ValueError("动作缺少转移结果")
        result = 0.0
        probability_sum = 0.0
        for probability, next_state, reward in outcomes:
            if probability < 0 or next_state not in state_set:
                raise ValueError("转移结果无效")
            probability_sum += probability
            result += probability * (reward + discount * values[next_state])
        if abs(probability_sum - 1.0) > 1e-9:
            raise ValueError("转移概率必须归一化")
        return result

    policy = {
        state: (actions.get(state, [None])[0] if actions.get(state, []) else None)
        for state in states
    }
    values = {state: 0.0 for state in states}
    for _ in range(max_policy_iterations):
        for _ in range(max_evaluation_iterations):
            updated = values.copy()
            maximum_change = 0.0
            for state in states:
                action = policy[state]
                if action is None:
                    updated[state] = 0.0
                else:
                    updated[state] = expected_return(state, action, values)
                maximum_change = max(
                    maximum_change, abs(updated[state] - values[state])
                )
            values = updated
            if maximum_change <= tolerance:
                break
        else:
            raise RuntimeError("策略评估在限制内未收敛")

        stable = True
        for state in states:
            choices = actions.get(state, [])
            if not choices:
                continue
            best_action = choices[0]
            best_return = expected_return(state, best_action, values)
            for action in choices[1:]:
                candidate = expected_return(state, action, values)
                if candidate > best_return:
                    best_action, best_return = action, candidate
            if policy[state] != best_action:
                policy[state] = best_action
                stable = False
        if stable:
            return values, policy
    raise RuntimeError("策略迭代在 max_policy_iterations 内未稳定")


if __name__ == "__main__":
    states = ["start", "mid", "terminal"]
    actions = {"start": ["short", "long"], "mid": ["finish"], "terminal": []}
    transitions = {
        ("start", "short"): [(1.0, "terminal", 1.0)],
        ("start", "long"): [(1.0, "mid", 0.0)],
        ("mid", "finish"): [(1.0, "terminal", 2.0)],
    }
    values, policy = policy_iteration(states, actions, transitions, 0.9)
    assert abs(values["start"] - 1.8) < 1e-8
    assert policy == {"start": "long", "mid": "finish", "terminal": None}
    print("003_policy_iteration: all examples passed")
