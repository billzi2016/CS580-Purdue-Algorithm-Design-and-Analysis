"""使用子集构造法把 ε-NFA 转换为完整 DFA。

适用场景：词法分析器将非确定自动机预处理为可在线性扫描中执行的确定自动机。
核心思想：每个 DFA 状态对应一组 NFA 状态；先求 ε 闭包，再按每个字母扩展该集合。
输入输出：输入 NFA 的起点、接受状态、转移表和字母表；输出以 frozenset 表示状态的 DFA。
时间复杂度：最坏 O(2^V × |Σ| × (V + E))；空间复杂度最坏 O(2^V × |Σ|)。
边界情况：空子集作为显式死状态，使输出在给定字母表上保持完整；ε 边只用 ``None`` 表示。
"""

from __future__ import annotations

from dataclasses import dataclass


EPSILON = None
DFAState = frozenset[int]


@dataclass
class DFA:
    """以 NFA 状态子集作为状态名的完整确定有限自动机。"""

    start: DFAState
    accepts: set[DFAState]
    transitions: dict[DFAState, dict[str, DFAState]]
    alphabet: set[str]


def epsilon_closure(
    transitions: dict[int, dict[str | None, set[int]]], states: set[int]
) -> set[int]:
    """返回 ``states`` 经任意条 ε 边可达的全部状态。

    参数：``transitions`` 为 NFA 邻接表，``states`` 为起始状态集合。
    返回值：包含原集合的 ε 闭包。
    边界情况：没有 ε 边时原样返回；环不会导致无限循环。
    关键点：状态首次发现时立即记录，保证每个状态只处理一次。
    """
    closure = set(states)
    pending = list(states)
    while pending:
        state = pending.pop()
        for target in transitions.get(state, {}).get(EPSILON, set()):
            if target not in closure:
                closure.add(target)
                pending.append(target)
    return closure


def nfa_to_dfa(
    start: int,
    accepts: set[int],
    transitions: dict[int, dict[str | None, set[int]]],
    alphabet: set[str],
) -> DFA:
    """用子集构造法将 ε-NFA 转为给定字母表上的完整 DFA。

    参数：NFA 起点 ``start``、接受状态集合 ``accepts``、转移表和非空单字符字母表。
    返回值：每个 DFA 状态均为一个不可变 NFA 状态集合的 ``DFA``。
    边界情况：转移为空的子集保留为死状态；若起点 ε 闭包含接受状态，DFA 起点即接受。
    关键点：对每个子集及字母先做 move，再做 ε 闭包，这是子集构造的核心定义。
    """
    _validate_alphabet(alphabet)
    start_subset = frozenset(epsilon_closure(transitions, {start}))
    pending = [start_subset]
    discovered = {start_subset}
    dfa_transitions: dict[DFAState, dict[str, DFAState]] = {}

    while pending:
        subset = pending.pop()
        row: dict[str, DFAState] = {}
        for symbol in alphabet:
            moved_states: set[int] = set()
            for nfa_state in subset:
                moved_states.update(transitions.get(nfa_state, {}).get(symbol, set()))
            target_subset = frozenset(epsilon_closure(transitions, moved_states))
            row[symbol] = target_subset
            if target_subset not in discovered:
                discovered.add(target_subset)
                pending.append(target_subset)
        dfa_transitions[subset] = row

    dfa_accepts = {subset for subset in discovered if subset & accepts}
    return DFA(start_subset, dfa_accepts, dfa_transitions, set(alphabet))


def dfa_accepts(dfa: DFA, text: str) -> bool:
    """判断完整 DFA 是否接受文本。

    参数：``dfa`` 是子集构造结果，``text`` 是待识别字符串。
    返回值：读完文本后是否处于接受状态。
    边界情况：字母表外字符返回 ``False``；空串只检查起始状态。
    关键点：DFA 每个状态、每个合法字母只有一个后继，因而无需维护状态集合。
    """
    state = dfa.start
    for symbol in text:
        if symbol not in dfa.alphabet:
            return False
        state = dfa.transitions[state][symbol]
    return state in dfa.accepts


def _validate_alphabet(alphabet: set[str]) -> None:
    """确保字母表元素能与单字符字符串输入一一对应。"""
    if any(not isinstance(symbol, str) or len(symbol) != 1 for symbol in alphabet):
        raise ValueError("字母表必须只包含单字符字符串")


if __name__ == "__main__":
    # 起点通过 ε 边分叉，因此该 NFA 接受单字符 a 或 b。
    sample_transitions = {
        0: {EPSILON: {1, 2}},
        1: {"a": {3}},
        2: {"b": {3}},
    }
    sample_dfa = nfa_to_dfa(0, {3}, sample_transitions, {"a", "b"})
    assert dfa_accepts(sample_dfa, "a")
    assert dfa_accepts(sample_dfa, "b")
    assert not dfa_accepts(sample_dfa, "")
    assert not dfa_accepts(sample_dfa, "ab")
    assert not dfa_accepts(sample_dfa, "c")

    empty_word_dfa = nfa_to_dfa(0, {1}, {0: {EPSILON: {1}}}, {"x"})
    assert dfa_accepts(empty_word_dfa, "")
    assert not dfa_accepts(empty_word_dfa, "x")
    assert frozenset() in empty_word_dfa.transitions

    print("002_nfa_to_dfa: all examples passed")
