"""
NP 完全性检查清单：把证明步骤结构化，防止遗漏关键条件。

本文件的意图：
1. 用代码化 checklist 表达 NP-completeness 证明需要哪些组成部分。
2. 区分“属于 NP”“从已知 NP-hard 问题多项式归约”“目标问题结论”。
3. 避免把复杂性证明写成空泛笔记；每个字段都能被程序验证是否填写。

注意：
这不是自动定理证明器。它只帮助维护课程笔记和 README 中的复杂性证明结构。
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class NPCompletenessProofSketch:
    """一个 NP 完全性证明草图。"""

    problem_name: str
    certificate_description: str
    verifier_runtime: str
    source_np_complete_problem: str
    reduction_mapping: str
    reduction_runtime: str


def validate_np_completeness_sketch(sketch: NPCompletenessProofSketch) -> list[str]:
    """返回证明草图中缺失的关键字段名称。"""

    missing: list[str] = []
    for field_name, value in sketch.__dict__.items():
        if not value.strip():
            missing.append(field_name)
    return missing


def is_structurally_complete(sketch: NPCompletenessProofSketch) -> bool:
    """判断证明草图是否至少具备 NP-completeness 的结构要件。"""

    return not validate_np_completeness_sketch(sketch)


def summarize_proof_obligations(sketch: NPCompletenessProofSketch) -> list[str]:
    """把证明义务转换成可读步骤。"""

    return [
        f"证明 {sketch.problem_name} 属于 NP：给出证书 {sketch.certificate_description}",
        f"证明验证器在 {sketch.verifier_runtime} 内运行",
        f"从 {sketch.source_np_complete_problem} 构造归约",
        f"说明实例映射：{sketch.reduction_mapping}",
        f"证明归约运行时间为 {sketch.reduction_runtime}",
    ]


if __name__ == "__main__":
    sketch = NPCompletenessProofSketch(
        problem_name="Vertex Cover",
        certificate_description="一个大小不超过 k 的顶点集合",
        verifier_runtime="O(V + E)",
        source_np_complete_problem="Independent Set",
        reduction_mapping="把 (G, k) 映射为 (G, |V|-k)",
        reduction_runtime="O(1) 额外构造时间，不复制图时只改参数",
    )
    assert validate_np_completeness_sketch(sketch) == []
    assert is_structurally_complete(sketch)
    assert len(summarize_proof_obligations(sketch)) == 5

    incomplete = NPCompletenessProofSketch("X", "", "O(n)", "SAT", "mapping", "poly")
    assert validate_np_completeness_sketch(incomplete) == ["certificate_description"]

    print("005_np_completeness_notes: all examples passed")
