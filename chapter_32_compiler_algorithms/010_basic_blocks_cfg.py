"""从带标签的简化三地址代码划分基本块并构造控制流图。

适用场景：优化器和数据流分析的前处理。核心思想：跳转目标、跳转后的指令与首指令都是 leader；leader 间区间即基本块。
输入输出：输入 ``Instruction`` 列表，输出基本块列表和后继邻接表。时间 O(n)，空间 O(n)。
边界：支持 ``label``、``goto``、``if_goto``、``return`` 和普通语句；不是完整汇编或 IR 解析器。
"""

from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class Instruction:
    """简化控制流指令；跳转类指令的 ``target`` 为标签名。"""
    op: str
    text: str
    target: str | None = None


@dataclass
class BasicBlock:
    """一个单入口、无内部跳转目标的最大指令区间。"""
    identifier: int
    instructions: list[Instruction]


def build_basic_blocks_and_cfg(instructions: list[Instruction]) -> tuple[list[BasicBlock], dict[int, set[int]]]:
    """划分基本块并返回其 CFG。

    参数：指令序列；返回值为块列表与 ``块号 -> 后继块号``。空输入返回两个空容器。
    边界：未知跳转标签会报错。关键点：条件跳转同时保留目标边和自然落空边。
    """
    if not instructions:
        return [], {}
    labels = {item.text: index for index, item in enumerate(instructions) if item.op == "label"}
    leaders = {0}
    for index, item in enumerate(instructions):
        if item.op in {"goto", "if_goto"}:
            if item.target not in labels:
                raise ValueError(f"跳转目标不存在：{item.target!r}")
            leaders.add(labels[item.target])
            if index + 1 < len(instructions):
                leaders.add(index + 1)
    starts = sorted(leaders)
    blocks: list[BasicBlock] = []
    instruction_to_block: dict[int, int] = {}
    for block_id, start in enumerate(starts):
        end = starts[block_id + 1] if block_id + 1 < len(starts) else len(instructions)
        blocks.append(BasicBlock(block_id, instructions[start:end]))
        for index in range(start, end):
            instruction_to_block[index] = block_id
    cfg = {block.identifier: set() for block in blocks}
    for block in blocks:
        last = block.instructions[-1]
        if last.op in {"goto", "if_goto"}:
            cfg[block.identifier].add(instruction_to_block[labels[last.target]])
        if last.op not in {"goto", "return"} and block.identifier + 1 < len(blocks):
            cfg[block.identifier].add(block.identifier + 1)
    return blocks, cfg


if __name__ == "__main__":
    program = [
        Instruction("assign", "x = 0"), Instruction("label", "loop"),
        Instruction("if_goto", "if x < 3 goto done", "done"), Instruction("assign", "x = x + 1"),
        Instruction("goto", "goto loop", "loop"), Instruction("label", "done"), Instruction("return", "return x"),
    ]
    blocks, cfg = build_basic_blocks_and_cfg(program)
    assert len(blocks) == 4
    assert cfg == {0: {1}, 1: {2, 3}, 2: {1}, 3: set()}
    assert build_basic_blocks_and_cfg([]) == ([], {})
    print("010_basic_blocks_cfg: all examples passed")
