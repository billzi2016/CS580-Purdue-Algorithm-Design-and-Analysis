"""对 CFG 执行反向活跃变量（liveness）数据流分析。

适用场景：寄存器分配、死代码消除。核心思想：OUT[n] 是后继 IN 的并集，IN[n] = USE[n] ∪ (OUT[n] - DEF[n])。
输入输出：输入 CFG 与每个节点 USE/DEF 集，输出稳定的 IN、OUT 集。时间 O(V²E) 量级，空间 O(V×变量数)。
边界：没有后继的节点 OUT 为空；没有 USE/DEF 条目的节点按空集处理。
"""

from __future__ import annotations


def liveness_analysis(cfg: dict[int, set[int]], uses: dict[int, set[str]], definitions: dict[int, set[str]]) -> tuple[dict[int, set[str]], dict[int, set[str]]]:
    """计算每个 CFG 节点前后的活跃变量集合。

    关键点：这是反向问题，先由后继汇总 OUT，随后删除本节点定义的旧值再加入使用值。
    """
    nodes = set(cfg) | set(uses) | set(definitions) | {target for targets in cfg.values() for target in targets}
    live_in = {node: set() for node in nodes}
    live_out = {node: set() for node in nodes}
    changed = True
    while changed:
        changed = False
        for node in nodes:
            new_out = set().union(*(live_in[successor] for successor in cfg.get(node, set()))) if cfg.get(node, set()) else set()
            new_in = uses.get(node, set()) | (new_out - definitions.get(node, set()))
            if new_out != live_out[node] or new_in != live_in[node]:
                live_out[node], live_in[node] = new_out, new_in
                changed = True
    return live_in, live_out


if __name__ == "__main__":
    cfg = {0: {1}, 1: {2}, 2: set()}
    live_in, live_out = liveness_analysis(cfg, {0: {"a", "b"}, 1: {"x", "c"}, 2: {"y"}}, {0: {"x"}, 1: {"y"}, 2: set()})
    assert live_in[2] == {"y"}
    assert live_out[1] == {"y"}
    assert live_in[1] == {"x", "c"}
    assert live_in[0] == {"a", "b", "c"}
    print("013_liveness_analysis: all examples passed")
