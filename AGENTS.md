# AGENTS.md

本文件规定本仓库中 AI agent、代码助手或维护者的工作方式。任何后续修改都必须先阅读并遵守本文件。

## 项目定位

本仓库是一个面向 Purdue CS 课程体系、算法课程、LeetCode、Codeforces、数学算法、数值方法、机器学习优化、深度学习架构、生物信息学、数据库、编译器、分布式系统和操作系统算法的系统化实现仓库。

目标不是堆放题解，而是构建一个长期可维护、可运行、可测试、可审查的算法实现手册。

## 总体工作流

0. 开始任何实现前，必须先阅读 `README.md` 和必要时的 `README.cn.md`，以确认当前 chapter 顺序、checklist 状态、实现规范和项目范围。
1. 每次只实现一个明确 chapter 或一个明确小批次。
2. 实现前说明本批次准备修改什么、为什么修改、涉及哪些文件。
3. 不要随意扩大范围。
4. 每个算法实现完成后，必须更新 README checklist，把对应条目从 `- [ ]` 改成 `- [x]`。
5. 每个批次必须运行相关测试或脚本验证。
6. 验证通过后再提交。
7. commit 后是否 push 由用户明确决定；没有明确要求时不要 push。

## 继续执行触发词

如果用户只回复以下任一内容：

- `0`
- `ok`
- `OK`
- `继续`
- `continue`
- `Continue`

则表示用户要求 agent：

1. 先阅读 `README.md`，必要时对照 `README.cn.md`。
2. 找到 README checklist 中下一个未完成的 chapter 或明确小批次。
3. 按本文件规则继续实现。
4. 实现后运行测试。
5. 测试通过后更新 checklist。
6. 按需 commit；是否 push 仍取决于用户是否明确要求。

这些触发词不表示允许跳过测试、不表示允许 mock、不表示允许 push、不表示允许扩大范围。

如果当前任务边界已经明确，例如“继续 Chapter 02”，这些触发词表示继续该边界内的剩余工作。

## 文件与目录规则

- chapter 目录使用固定格式：`chapter_XX_topic_name/`。
- 算法文件使用固定格式：`NNN_algorithm_name.py`。
- 编号必须稳定，不要因为新增算法随意重排已有编号。
- 一个文件只实现一个核心算法或一组高度相关的变体。
- 示例、测试辅助函数和核心算法要分清职责。
- 不要把多个不相关算法塞进一个文件。
- 不要无故移动、重命名或删除已有文件。

## 手写实现规则

核心算法必须手写。

禁止“一击必杀”式库调用，即不能直接调用现成库完成目标算法。

禁止 mock、占位和功能不全实现冒充完成。这类行为会破坏学术端正性和仓库可信度，按重大质量问题处理。

允许：

- 使用 Python 标准库做基础容器、类型标注、数学常量和测试辅助。
- 使用 `numpy` 做数组存储和基础矩阵/向量计算。
- 使用 `torch` 做 tensor、autograd 实验和底层神经网络计算。

禁止：

- 用 `bisect` 冒充手写二分。
- 用 `sorted()` 冒充手写排序算法。
- 用 `heapq` 冒充手写堆。
- 用 `sklearn.svm.SVC` 冒充手写 SVM。
- 用 `torch.optim.Adam` 冒充手写 Adam。
- 用 `torch.nn.MultiheadAttention` 冒充手写 multi-head attention。
- 用现成 BLAST、FASTA、minimap2、BioPython 接口冒充生物信息学算法。
- 用数据库、图算法、优化器或密码学现成库直接完成目标算法。

如果某个库只是用于底层数值表示，核心算法步骤仍必须清楚写在源码里。

## 完整性与学术端正规则

任何算法实现都必须是完整、可运行、可验证的教学实现。

严禁：

- 用 `pass`、`TODO`、空函数或伪代码冒充完成。
- 只写 happy path，故意忽略必要边界情况。
- 写一个只能通过当前样例、不能表达真实算法逻辑的硬编码实现。
- 用 mock 数据、mock 返回值或占位结果冒充算法输出。
- 用简化到失去算法本质的版本冒充完整实现。
- 在 README checklist 中勾选未完成、未测试或测试失败的项目。
- 声称覆盖某个算法，但源码中没有该算法的核心步骤。

如果某个算法因为篇幅或教学目的只能实现基础版，必须在文件开头明确写清：

- 这是基础版还是完整版本；
- 支持哪些输入范围；
- 不支持哪些情况；
- 与工业级实现相比缺少什么；
- 为什么当前范围仍然足以说明算法核心。

禁止把基础版包装成完整工业实现。

涉及课程、论文、数据、实验结果、性能结论、密码学安全性或生物信息学结论时，不得编造来源、数据和结论。未经核实的内容不得写成确定事实。

## 中文注释规则

所有 Python 文件必须使用完整中文注释。

每个文件开头必须包含模块级 docstring，至少说明：

- 文件意图；
- 适用场景；
- 核心思想；
- 输入输出；
- 时间复杂度；
- 空间复杂度；
- 关键边界情况。

每个公开函数必须包含中文 docstring，至少说明：

- 函数意图；
- 参数；
- 返回值；
- 边界情况；
- 关键算法点。

代码内部必须在以下位置添加中文注释：

- 循环不变量；
- 难理解的条件分支；
- 容斥、转移、递推、松弛、剪枝等关键步骤；
- 复杂边界处理；
- 数学公式对应的实现；
- 算法正确性依赖的关键点。

注释必须解释“为什么这样做”，不要只重复代码表面含义。

## 代码质量规则

- 遵循 SOLID 和 DRY 原则。
- 函数职责要单一。
- 避免复制粘贴重复逻辑。
- 公共逻辑可以抽 helper，但不要过度抽象。
- 优先可读性，不追求竞赛式极限压缩。
- 变量名要表达含义，不使用无意义缩写。
- 类型标注应尽量完整。
- 错误输入应明确抛出异常或在 docstring 中说明假设。
- 不要引入不必要依赖。

## `__main__` 示例规则

每个算法文件必须包含：

```python
if __name__ == "__main__":
    assert ...

    print("NNN_algorithm_name: all examples passed")
```

`if __name__ == "__main__":` 代码块中必须包含多个示例，至少覆盖：

- 正常输入；
- 空输入或最小输入；
- 边界值；
- 重复值或特殊结构；
- 能体现算法关键性质的例子。

示例应使用 `assert` 验证结果，并在全部通过后输出清晰的 passed 信息。

测试入口必须放在文件底部，并使用标准 Python main guard。测试断言直接写在 `__main__` 代码块中，不再额外定义 `main()` 函数：

```python
if __name__ == "__main__":
    assert ...
```

禁止：

- 在文件顶层散落 `assert`。
- 为测试额外定义 `main()` 函数。
- 写了 `main()` 后再通过 `if __name__ == "__main__": main()` 调用。
- 使用非标准入口名称替代 `__main__` 代码块。
- 把测试逻辑藏在导入时自动执行的全局代码里。

标准形式示例：

```python
if __name__ == "__main__":
    assert factorial_recursive(0) == 1
    assert factorial_recursive(5) == 120
    assert factorial_iterative(5) == 120
    assert sum_recursive([1, 2, 3, 4]) == 10
    assert sum_iterative([1, 2, 3, 4]) == 10
    assert sum_iterative([]) == 0

    print("010_recursion_and_iteration: all examples passed")
```

## 测试规则

实现一个 chapter 后，必须运行该 chapter 下所有脚本：

```bash
for file in chapter_XX_topic_name/*.py; do python3 "$file"; done
```

提交前如需验证全仓所有 chapter 下的 Python 示例，必须运行：

```bash
bash scripts/run_all_python_examples.sh
```

该脚本会遍历所有 `chapter_*/*.py` 文件，并逐个执行文件底部的 `if __name__ == "__main__":` 测试块。

如果后续加入 `pytest`，则同时运行相关 pytest：

```bash
python3 -m pytest
```

测试失败时：

1. 不要提交。
2. 先定位失败文件和失败样例。
3. 修复后重新运行同一测试范围。
4. 在最终汇报中说明测试结果。

测试是硬性门槛：

- 测试不通过，不得 commit。
- 测试不通过，不得 push。
- 测试不通过，不得更新 checklist 为 `- [x]`。
- 测试不通过，不得声称该 chapter 已完成。
- 如果因环境缺失无法运行测试，必须明确说明缺失依赖和未验证范围，不能当作通过。
- 不允许删除失败样例来制造通过。
- 不允许降低断言强度来制造通过。
- 不允许跳过核心路径测试来制造通过。

## README checklist 规则

- 每实现一个算法文件，必须在 `README.md` 中把对应条目改成 `- [x]`。
- 中文版 `README.cn.md` 如果有 chapter 级 checklist，也必须同步更新。
- 不得提前勾选未实现或未验证的算法。
- 如果实现的是 chapter 级清单中的一部分，只能勾选具体文件，不能把整个 chapter 提前标记完成。

## Git 规则

Git 操作必须清晰、可审查。

提交前必须：

1. 运行相关测试。
2. 检查 `git status --short --branch`。
3. 只暂存本批次相关文件。
4. 不使用无脑 `git add .`，除非用户明确要求且确认范围安全。

commit 信息必须：

- 使用中文；
- 不超过 10 行；
- 标题具体，不写 “initial commit” 这类空泛信息；
- 正文用 bullet 列出主要变化；
- 清楚说明实现内容、README checklist 更新和测试情况。

推荐格式：

```text
实现 Chapter 01 基础算法

- 添加二分、前缀和、差分、双指针、滑动窗口和快速幂实现
- 为每个文件补充中文意图注释、函数注释和 main 示例
- 更新 README checklist 并验证 Chapter 01 脚本全部通过
```

未经用户明确要求，不要执行：

- `git push`
- `git pull`
- `git merge`
- `git rebase`
- `git reset`
- `git checkout`
- `git switch`
- 创建或删除分支
- 创建、编辑、关闭或合并 PR

如果用户明确要求 push，push 前说明远程和分支。

## 学术、课程和数据规则

- 涉及课程编号、课程名称、论文、数据、实验结论时，必须核实来源。
- 不得编造课程名、论文、数据或结论。
- 示例数据可以使用，但必须明显只是测试样例，不能伪装成真实实验数据。
- 生物信息学、密码学、机器学习等领域的事实性说明必须谨慎，避免过度声称。

## 安全与删除规则

- 不要删除文件，除非用户明确要求。
- 不要移动或重命名文件，除非用户明确要求。
- 删除、移动、覆盖、批量复制前必须说明目标、原因、影响范围和是否可恢复，并等待用户确认。
- 不要执行破坏性命令。

## 批次完成汇报

每个批次完成后，必须汇报：

- 新增或修改了哪些文件；
- 实现了哪些算法；
- README checklist 是否已更新；
- 执行了哪些测试；
- 测试是否通过；
- 是否已 commit；
- 是否尚未 push。

## 当前推荐执行顺序

1. Chapter 01 Foundations
2. Chapter 02 Sorting and Selection
3. Chapter 03 Divide and Conquer
4. Chapter 04 Graph Traversal
5. Chapter 05 Shortest Paths
6. Chapter 06 Minimum Spanning Trees
7. Chapter 07 Greedy Algorithms
8. Chapter 08 Dynamic Programming I
9. 后续按 README checklist 顺序推进

不得跳过基础章节直接实现高级章节，除非用户明确指定。
