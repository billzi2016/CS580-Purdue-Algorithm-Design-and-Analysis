"""
文件意图：用奇偶不变量判断二进制状态的可达性，并手写构造一条合法操作序列。
适用场景：每一步恰好翻转两个二进制位置的变换问题，以及“先找不变量、再构造”的证明型算法练习。
核心思想：一次翻转两位使 1 的个数变化只能是 -2、0、2，故其奇偶性不变；反过来，相异位置可成对翻转以完成任意同奇偶目标。
输入输出：输入等长 0/1 列表 source、target，输出可达性或一系列待翻转的下标对。
时间复杂度：O(n)，空间复杂度 O(n)，其中 n 是序列长度。
关键边界情况：空序列允许；长度不等或非二进制值拒绝；不同奇偶性的目标无法到达。
"""


def has_same_parity_invariant(source: list[int], target: list[int]) -> bool:
    """判断 source 到 target 是否满足两位翻转操作的必要且充分不变量。

    参数：source 和 target 是等长的二进制状态列表。
    返回：两者 1 的数量同奇偶时返回真。
    边界情况：空状态返回真；长度不等或含非 0/1 值时抛出 ValueError。
    关键算法点：操作每次只改变偶数个比特，因此总和模 2 保持不变；该条件也是充分条件。
    """
    _validate_binary_states(source, target)
    return sum(source) % 2 == sum(target) % 2


def construct_pair_flip_sequence(source: list[int], target: list[int]) -> list[tuple[int, int]] | None:
    """构造从 source 到 target 的两位翻转序列。

    参数：source 和 target 是等长二进制状态；一次操作翻转两个不同下标。
    返回：下标对列表；若不可达返回 None。
    边界情况：相同状态返回空列表；奇偶不变量不一致时返回 None。
    关键算法点：不同的位置必须有偶数个，任意两两配对翻转就会恰好修正这些位置。
    """
    if not has_same_parity_invariant(source, target):
        return None
    mismatches = [index for index, (current, desired) in enumerate(zip(source, target)) if current != desired]
    if len(mismatches) % 2:
        raise AssertionError("同奇偶状态的不同位置数量必须为偶数")
    operations: list[tuple[int, int]] = []
    for index in range(0, len(mismatches), 2):
        # 每次翻转两个当前仍不匹配的位置，不会破坏此前已经修正的位置。
        operations.append((mismatches[index], mismatches[index + 1]))
    return operations


def apply_pair_flips(state: list[int], operations: list[tuple[int, int]]) -> list[int]:
    """执行下标对翻转操作，供构造结果验证使用。

    参数：state 是初始二进制状态；operations 是每步的两个不同有效下标。
    返回：执行所有操作后的新状态，不修改原列表。
    边界情况：非法状态值、重复下标或越界下标抛出 ValueError。
    关键算法点：复制输入，确保构造器和验证器职责独立且调用方状态不被意外改写。
    """
    if any(value not in (0, 1) for value in state):
        raise ValueError("state 必须只包含 0 和 1")
    result = state.copy()
    for first, second in operations:
        if first == second or not 0 <= first < len(result) or not 0 <= second < len(result):
            raise ValueError("每个操作必须给出两个不同的有效下标")
        result[first] ^= 1
        result[second] ^= 1
    return result


def _validate_binary_states(source: list[int], target: list[int]) -> None:
    """验证两个用于可达性判断的二进制状态格式。"""
    if len(source) != len(target):
        raise ValueError("source 和 target 必须等长")
    if any(value not in (0, 1) for value in source + target):
        raise ValueError("状态必须只包含 0 和 1")


if __name__ == "__main__":
    source_state = [0, 1, 0, 1]
    target_state = [1, 0, 1, 0]
    sequence = construct_pair_flip_sequence(source_state, target_state)
    assert sequence is not None
    assert apply_pair_flips(source_state, sequence) == target_state
    assert has_same_parity_invariant([], [])
    assert construct_pair_flip_sequence([0], [1]) is None
    assert construct_pair_flip_sequence([1, 0], [1, 0]) == []
    print("004_invariant_construction: all examples passed")
