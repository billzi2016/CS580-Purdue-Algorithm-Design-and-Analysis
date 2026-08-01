"""
文件意图：手写实现有限 MDP 的价值迭代。
适用场景：已知完整转移模型时，求解折扣无限时域的最优状态价值和贪心策略。
核心思想：反复执行 Bellman 最优备份，直到所有状态价值的最大改变量不超过容差。
输入输出：输入状态、动作、转移和折扣因子，输出价值字典与最优动作字典。
时间复杂度：每轮 O(T)，T 为全部转移项数；轮数由收敛速度决定。空间复杂度：O(S)。
关键边界：终止状态无动作且价值保持零；概率分布和输入引用必须由调用者保证合法。
"""

Transition = tuple[float, str, float]


def value_iteration(
    states: list[str],
    actions: dict[str, list[str]],
    transitions: dict[tuple[str, str], list[Transition]],
    discount: float,
    tolerance: float = 1e-9,
    max_iterations: int = 10_000,
) -> tuple[dict[str, float], dict[str, str | None]]:
    """计算有限 MDP 的近似最优价值与对应贪心策略。

    参数：states 是状态列表；actions 给出可行动作；transitions 的结果是 (概率, 下一状态, 奖励)；discount 在 [0,1)；tolerance 为停止阈值。
    返回：状态价值字典和动作字典，终止状态的动作值为 None。
    边界情况：无动作状态视为终止状态；非法折扣、容差或迭代次数抛出 ValueError。
    关键算法点：每轮用上一轮完整价值表计算新表，避免状态遍历顺序改变 Bellman 同步备份语义。
    """
    if not 0 <= discount < 1 or tolerance <= 0 or max_iterations <= 0:
        raise ValueError("discount、tolerance 和 max_iterations 参数无效")
    state_set = set(states)
    if len(state_set) != len(states):
        raise ValueError("states 不能包含重复状态")
    values = {state: 0.0 for state in states}

    def action_value(state: str, action: str, reference: dict[str, float]) -> float:
        """根据 reference 计算一个状态动作对的 Bellman 期望回报。"""
        outcomes = transitions.get((state, action))
        if not outcomes:
            raise ValueError("每个动作必须有至少一个转移结果")
        total = 0.0
        for probability, next_state, reward in outcomes:
            if probability < 0 or next_state not in state_set:
                raise ValueError("转移结果无效")
            total += probability * (reward + discount * reference[next_state])
        return total

    for _ in range(max_iterations):
        updated: dict[str, float] = {}
        maximum_change = 0.0
        for state in states:
            choices = actions.get(state, [])
            if not choices:
                updated[state] = 0.0
                continue
            best = action_value(state, choices[0], values)
            for action in choices[1:]:
                candidate = action_value(state, action, values)
                if candidate > best:
                    best = candidate
            updated[state] = best
            maximum_change = max(maximum_change, abs(best - values[state]))
        values = updated
        if maximum_change <= tolerance:
            break
    else:
        raise RuntimeError("价值迭代在 max_iterations 内未收敛")

    policy: dict[str, str | None] = {}
    for state in states:
        choices = actions.get(state, [])
        if not choices:
            policy[state] = None
            continue
        best_action = choices[0]
        best_value = action_value(state, best_action, values)
        for action in choices[1:]:
            candidate = action_value(state, action, values)
            if candidate > best_value:
                best_action, best_value = action, candidate
        policy[state] = best_action
    return values, policy


if __name__ == "__main__":
    states = ["start", "mid", "terminal"]
    actions = {"start": ["short", "long"], "mid": ["finish"], "terminal": []}
    transitions = {
        ("start", "short"): [(1.0, "terminal", 1.0)],
        ("start", "long"): [(1.0, "mid", 0.0)],
        ("mid", "finish"): [(1.0, "terminal", 2.0)],
    }
    values, policy = value_iteration(states, actions, transitions, 0.9)
    assert abs(values["start"] - 1.8) < 1e-8
    assert policy == {"start": "long", "mid": "finish", "terminal": None}
    print("002_value_iteration: all examples passed")
