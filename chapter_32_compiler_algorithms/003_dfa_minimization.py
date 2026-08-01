"""用分区细化法最小化完整确定有限自动机。

适用场景：编译器词法分析器压缩状态数，或讲解 Myhill–Nerode 等价关系的构造过程。
核心思想：先把接受与非接受状态分开；再按每个字母的目标分区反复细分，直至稳定。
输入输出：输入以整数编号、转移完整的 DFA；输出仅含可达状态且状态数最少的等价 DFA。
时间复杂度：本教学实现为 O(|Σ| × V²) 量级；空间复杂度为 O(|Σ| × V)。
边界情况：不可达状态会被移除；缺少转移或字母表不合法会抛出 ``ValueError``。
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class DFA:
    """完整 DFA：每个状态对字母表中每个符号都有唯一后继。"""

    start: int
    accepts: set[int]
    transitions: dict[int, dict[str, int]]
    alphabet: set[str]


def minimize_dfa(dfa: DFA) -> DFA:
    """返回与输入 DFA 等价、且只含可达最少状态的 DFA。

    参数：``dfa`` 必须是转移完整、以整数编号状态的 DFA。
    返回值：状态重新编号为 ``0..k-1`` 的最小 DFA。
    边界情况：不可达状态不参与分区；全接受或全拒绝时初始仅有一个分区。
    关键点：两个状态仅在每个字母都落入相同分区时才可继续保持等价。
    """
    reachable = _reachable_states(dfa)
    _validate_complete_dfa(dfa, reachable)

    accepting = reachable & dfa.accepts
    rejecting = reachable - accepting
    partitions = [group for group in (accepting, rejecting) if group]

    while True:
        state_to_group = _group_index(partitions)
        refined: list[set[int]] = []
        changed = False

        for group in partitions:
            buckets: dict[tuple[int, ...], set[int]] = {}
            for state in group:
                # 同一签名意味着该状态在所有字符下都转向同一组等价类。
                signature = tuple(
                    state_to_group[dfa.transitions[state][symbol]]
                    for symbol in sorted(dfa.alphabet)
                )
                buckets.setdefault(signature, set()).add(state)
            refined.extend(buckets.values())
            changed = changed or len(buckets) > 1

        partitions = refined
        if not changed:
            break

    return _build_minimized_dfa(dfa, partitions)


def dfa_accepts(dfa: DFA, text: str) -> bool:
    """模拟 DFA 是否接受文本。

    参数：``dfa`` 为完整 DFA，``text`` 为待识别字符串。
    返回值：文本读完后所在状态是否为接受状态。
    边界情况：输入包含字母表外字符时返回 ``False``。
    关键点：确定性保证每次读取只需跟随一条转移。
    """
    state = dfa.start
    for symbol in text:
        if symbol not in dfa.alphabet:
            return False
        state = dfa.transitions[state][symbol]
    return state in dfa.accepts


def _reachable_states(dfa: DFA) -> set[int]:
    """从起点遍历可达状态，避免无用状态影响最小化结果。"""
    reached = {dfa.start}
    pending = [dfa.start]
    while pending:
        state = pending.pop()
        for target in dfa.transitions.get(state, {}).values():
            if target not in reached:
                reached.add(target)
                pending.append(target)
    return reached


def _validate_complete_dfa(dfa: DFA, reachable: set[int]) -> None:
    """验证已访问区域满足完整 DFA 的前提条件。"""
    if any(not isinstance(symbol, str) or len(symbol) != 1 for symbol in dfa.alphabet):
        raise ValueError("字母表必须只包含单字符字符串")
    for state in reachable:
        row = dfa.transitions.get(state)
        if row is None or set(row) != dfa.alphabet:
            raise ValueError("DFA 的每个可达状态必须包含字母表上的完整转移")
        if any(target not in reachable for target in row.values()):
            raise ValueError("可达状态的后继必须也可达")


def _group_index(partitions: list[set[int]]) -> dict[int, int]:
    """建立状态到当前分区编号的映射，供签名比较使用。"""
    mapping: dict[int, int] = {}
    for index, group in enumerate(partitions):
        for state in group:
            mapping[state] = index
    return mapping


def _build_minimized_dfa(dfa: DFA, partitions: list[set[int]]) -> DFA:
    """将稳定分区收缩为新状态，任取组内代表状态生成转移。"""
    state_to_group = _group_index(partitions)
    new_transitions: dict[int, dict[str, int]] = {}
    new_accepts: set[int] = set()

    for group_index, group in enumerate(partitions):
        representative = next(iter(group))
        new_transitions[group_index] = {
            symbol: state_to_group[dfa.transitions[representative][symbol]]
            for symbol in dfa.alphabet
        }
        if group & dfa.accepts:
            new_accepts.add(group_index)

    return DFA(
        start=state_to_group[dfa.start],
        accepts=new_accepts,
        transitions=new_transitions,
        alphabet=set(dfa.alphabet),
    )


if __name__ == "__main__":
    # 状态 1 与 2 同为接受吸收态，最小化后应合并；状态 4 不可达。
    redundant_dfa = DFA(
        start=0,
        accepts={1, 2},
        transitions={
            0: {"a": 1, "b": 2},
            1: {"a": 1, "b": 1},
            2: {"a": 2, "b": 2},
            3: {"a": 3, "b": 3},
            4: {"a": 4, "b": 4},
        },
        alphabet={"a", "b"},
    )
    minimized = minimize_dfa(redundant_dfa)
    assert len(minimized.transitions) == 2
    assert dfa_accepts(minimized, "a")
    assert dfa_accepts(minimized, "bb")
    assert not dfa_accepts(minimized, "")
    assert not dfa_accepts(minimized, "c")

    all_accepting = DFA(
        start=0,
        accepts={0, 1},
        transitions={0: {"x": 1}, 1: {"x": 0}},
        alphabet={"x"},
    )
    one_state = minimize_dfa(all_accepting)
    assert len(one_state.transitions) == 1
    assert dfa_accepts(one_state, "")
    assert dfa_accepts(one_state, "xxxx")

    print("003_dfa_minimization: all examples passed")
