# CS 580：算法设计与分析

本仓库用于整理 **Purdue University CS 580: Algorithm Design and Analysis** 相关的算法实现、学习笔记和可运行示例，并把实现规划扩展映射到更多 Purdue Computer Science 课程。同时覆盖 LeetCode 常见题型、Codeforces 竞赛算法、数学算法、启发式优化、蒙特卡洛树搜索、机器学习优化、深度学习网络架构，以及非 AI 生物信息学算法。目标是构建一个结构清晰、按章节组织的算法参考仓库，将 Purdue 课程主题与实际刷题、竞赛、数学计算、优化实现和工程化实现结合起来。

在过去八年里，我作为 TA 参与了七门 Purdue CS 课程，并基于这些教学和课程支持经历整理出这些笔记与实现：**Numerical Methods**、**Data Mining and Machine Learning**、**Introduction to Cryptography**、**Algorithm Design, Analysis, and Implementation**、**Programming Languages**、**Statistical Machine Learning** 和 **Database Systems**。本仓库希望把这些方向中的核心方法系统整理成一个可维护、以实现为核心的算法手册。

仓库会按照章节划分主题，使每个算法都便于查找、测试和扩展。每个实现都应包含简明说明、复杂度分析，以及可以直接运行的本地 `main` 示例。

## 仓库结构

算法按 chapter 分组。每个 chapter 目录对应一个主要主题，目录中的算法文件使用编号前缀，保证顺序稳定、查找方便。

```text
chapter_01_foundations/
  001_binary_search.py
  002_prefix_sum.py
  003_two_pointers.py

chapter_02_sorting_and_selection/
  001_merge_sort.py
  002_quick_sort.py
  003_quick_select.py

chapter_03_divide_and_conquer/
  001_count_inversions.py
  002_closest_pair_of_points.py

main.py
```

推荐文件格式：

```text
chapter_XX_topic_name/
  001_algorithm_name.py
  002_algorithm_name.py
  003_algorithm_name.py
```

每个算法文件应包含：

- 清晰的算法实现；
- 若干个示例测试用例；
- 时间复杂度和空间复杂度；
- 边界情况覆盖；
- 一个 `main` 入口或可调用的 demo 函数，用于快速验证。

## Purdue 课程覆盖映射

本仓库从 CS 580 出发，扩展成一个覆盖 Purdue 多门 CS 课程主题的算法实现地图。它不是官方 syllabus 的替代品，而是面向实现、注释、测试和工程维护的算法参考仓库。

| Purdue 课程 | 课程名称 | 仓库覆盖方向 |
|---|---|---|
| CS 18000 | Problem Solving and Object-Oriented Programming | 基础编程模式、递归、迭代、测试示例 |
| CS 18200 | Foundations of Computer Science | 离散数学基础、证明思路、递推分析、组合数学 |
| CS 24000 | Programming Laboratory in C | 底层实现纪律、内存意识、偏系统的算法实现 |
| CS 25000 | Computer Architecture | 位运算、整数表示、缓存意识、底层性能分析 |
| CS 25100 | Data Structures and Algorithms | 数组、链表、栈、队列、树、堆、哈希表、图、并查集 |
| CS 25200 | Systems Programming | 系统编程相关数据结构、文件处理示例、调度模拟 |
| CS 25300 | Data Structures and Algorithms for DS/AI | 数据科学和 AI pipeline 中常用的数据结构 |
| CS 31100 | Competitive Programming II | 竞赛模式、图算法、DP、数论、数据结构 |
| CS 31400 | Numerical Methods | 数值微分、数值积分、求根、ODE、数值线性代数 |
| CS 33400 | Fundamentals of Computer Graphics | 计算几何、变换、插值、空间算法 |
| CS 34800 | Information Systems | 数据库索引、查询执行、join 算法、事务概念 |
| CS 35200 | Compilers: Principles and Practice | 自动机、解析、CFG、SSA、活跃变量分析、寄存器分配 |
| CS 35400 | Operating Systems | 调度算法、页面置换、磁盘调度、并发相关模型 |
| CS 35500 | Introduction to Cryptography | 模运算、RSA、Diffie-Hellman、哈希、Merkle Tree、ECC 基础 |
| CS 37300 | Data Mining and Machine Learning | 优化、采样、聚类基础组件、机器学习算法基础 |
| CS 38100 | Introduction to the Analysis of Algorithms | 排序、分治、贪心、DP、图算法、网络流、NP 完全性 |
| CS 41100 | Competitive Programming III | 高级竞赛数据结构、树链剖分、莫队、CDQ、FFT/NTT、构造题 |
| CS 42200 | Computer Networks | 图路由思想、分布式协调、哈希、协议状态算法 |
| CS 42600 | Computer Security | 密码学原语、哈希、Merkle Tree、安全算法基础 |
| CS 44000 | Large Scale Data Analytics | sketch、流式算法、采样、外存算法、大规模处理 |
| CS 44800 | Introduction to Relational Database Systems | B-tree、B+ tree、join、查询规划、索引、MVCC 基础 |
| CS 47100 | Introduction to Artificial Intelligence | 搜索算法、A*、IDA*、MCTS、优化、规划基础 |
| CS 47800 | Introduction to Bioinformatics | DNA 匹配、序列比对、BLAST/FASTA 风格搜索、基因组组装、pangenome graph |
| CS 48900 | Embedded Systems | 位级算法、调度、内存敏感实现 |
| CS 53000 | Introduction to Scientific Visualization | 数值方法、几何、插值、图和网格算法 |
| CS 53500 | Interactive Computer Graphics | 几何、空间数据结构、插值、变换 |
| CS 53600 | Data Communication and Computer Networks | 最短路、路由、哈希、分布式算法 |
| CS 54100 | Database Systems | 存储结构、查询优化、join、并发控制 |
| CS 55100 | Cloud Computing Fundamentals | 分布式算法、一致性哈希、复制、共识基础 |
| CS 55800 | Introduction to Robot Learning | 优化、搜索、规划、强化学习基础 |
| CS 56500 | Programming Languages | 解析、自动机、程序分析、编译器算法 |
| CS 57800 | Statistical Machine Learning | 优化算法、梯度方法、正则化、模型训练基础组件 |
| CS 58000 | Algorithm Design, Analysis, and Implementation | 图算法、网络流、线性规划思想、近似、随机化算法、NP 完全性 |
| CS 58400 | Theory of Computation and Computational Complexity | 自动机、归约、复杂性、NP 完全性 |
| CS 58500 | Theoretical Computer Science Toolkit | 数学工具、概率、组合、证明技巧 |
| CS 53100 | Computational Geometry | 几何基础操作、凸包、扫描线、最近点对、空间算法 |
| CS 55500 | Cryptography | 数论、公钥密码、哈希、认证原语 |
| CS 590AA | Approximation Algorithms | 近似算法、LP rounding 思路、贪心近似模式 |
| CS 590RA | Randomized Algorithms | 随机化算法、哈希、采样、Monte Carlo 方法 |
| CS 65500 | Advanced Cryptology | 高级密码学基础和数论原语 |

## 算法任务清单

章节设计同时覆盖标准算法设计课程内容、LeetCode 常见题型、Codeforces 竞赛算法、数学算法、非 AI 生物信息学算法、启发式搜索与优化、ML/DL 优化算法、深度学习网络架构、压缩与信息编码、密码学、编译器、数据库、分布式系统、操作系统调度、强化学习和图机器学习采样。完成后可把对应条目从 `- [ ]` 改成 `- [x]`。

- [ ] `chapter_01_foundations/`：二分查找、上下界、前缀和、二维前缀和、差分数组、双指针、滑动窗口、快速幂、位运算、递归与迭代模式
- [ ] `chapter_02_sorting_and_selection/`：归并排序、快速排序、堆排序、计数排序、基数排序、桶排序、快速选择、中位数的中位数
- [ ] `chapter_03_divide_and_conquer/`：逆序对计数、最近点对、Karatsuba 乘法、分治矩阵乘法、递归式示例
- [ ] `chapter_04_graph_traversal/`：BFS、DFS、连通分量、拓扑排序、环检测、二分图检测
- [ ] `chapter_05_shortest_paths/`：Dijkstra、Bellman-Ford、Floyd-Warshall、0-1 BFS、DAG 最短路、Johnson 算法
- [ ] `chapter_06_minimum_spanning_trees/`：并查集、Kruskal、Prim、割性质、环性质、次小生成树
- [ ] `chapter_07_greedy_algorithms/`：区间调度、活动选择、Huffman 编码、分数背包、交换论证
- [ ] `chapter_08_dynamic_programming_i/`：Fibonacci 变体、0/1 背包、完全背包、LIS、编辑距离、零钱兑换、LCS
- [ ] `chapter_09_dynamic_programming_ii/`：状压 DP、树形 DP、数位 DP、区间 DP、轮廓线 DP、凸包优化、Knuth 优化、分治 DP 优化
- [ ] `chapter_10_network_flow_and_matching/`：Ford-Fulkerson、Edmonds-Karp、Dinic、最小割、二分图匹配、Hopcroft-Karp、最小费用最大流
- [ ] `chapter_11_advanced_graph_algorithms/`：Tarjan SCC、Kosaraju SCC、桥、割点、欧拉路径、LCA
- [ ] `chapter_12_string_algorithms/`：KMP、Z Algorithm、Rabin-Karp、Trie、Aho-Corasick、后缀数组、LCP、Manacher
- [ ] `chapter_13_number_theory/`：gcd、扩展 gcd、快速幂、模逆元、筛法、质因数分解、中国剩余定理、Miller-Rabin
- [ ] `chapter_14_computational_geometry/`：方向判断、线段相交、多边形面积、凸包、旋转卡壳、扫描线
- [ ] `chapter_15_data_structures/`：堆、单调栈、单调队列、Fenwick 树、线段树、懒标记线段树、稀疏表、离散稀疏表
- [ ] `chapter_16_randomized_algorithms/`：随机化快速排序、随机选择、蓄水池抽样、通用哈希、Monte Carlo 素性检测
- [ ] `chapter_17_approximation_and_hardness/`：点覆盖近似、集合覆盖贪心、装箱启发式、归约示例、NP 完全性笔记
- [ ] `chapter_18_contest_patterns/`：坐标压缩、离线查询、答案二分、折半搜索、事件扫描线、差分约束、构造题模式
- [ ] `chapter_19_advanced_contest_data_structures/`：可持久化线段树、隐式 Treap、Li Chao Tree、顺序统计树模式、可回滚并查集
- [ ] `chapter_20_advanced_tree_algorithms/`：Euler Tour、倍增、树链剖分、DSU on Tree、点分治
- [ ] `chapter_21_offline_and_range_query_algorithms/`：莫队、树上莫队、CDQ 分治、整体二分、离线动态连通性
- [ ] `chapter_22_combinatorics_and_polynomial_algorithms/`：阶乘与组合数、容斥、Catalan 数、生成函数、FFT、NTT、子集卷积基础
- [ ] `chapter_23_game_theory_and_constructive_methods/`：Nim、Sprague-Grundy、mex、不变量构造、极值构造
- [ ] `chapter_24_bioinformatics/`：DNA 精确匹配、KMP、Rabin-Karp、Aho-Corasick、编辑距离、Needleman-Wunsch、Smith-Waterman、Hirschberg、BWT、FM-index、FASTA、BLAST、spaced seeds、minimizer、syncmer、seed chaining、de Bruijn graph、OLC、HMM、系统发育树、MinHash、pangenome graph
- [ ] `chapter_25_ml_dl_optimization/`：GD、SGD、mini-batch GD、Momentum、Nesterov、AdaGrad、RMSProp、Adam、AdamW、Nadam、AMSGrad、学习率衰减、cosine annealing、warmup、梯度裁剪、weight decay、L1/L2 正则、early stopping、Newton、BFGS、L-BFGS、共轭梯度、坐标下降、投影梯度、近端梯度、mirror descent、dual averaging、梯度检查、line search、grid search、random search、Bayesian optimization
- [ ] `chapter_26_heuristic_search_and_metaheuristics/`：爬山法、随机重启爬山、模拟退火、粒子群优化、遗传算法、差分进化、蚁群算法、禁忌搜索、Beam Search、A*、IDA*、MCTS、UCB、交叉熵方法、CMA-ES 基础
- [ ] `chapter_27_mathematical_and_numerical_algorithms/`：有限差分求导、梯度/Jacobian/Hessian、Newton 求根、二分求根、割线法、不动点迭代、梯形积分、Simpson 积分、自适应 Simpson、高斯求积、Monte Carlo 积分、Euler ODE、RK4、Gaussian elimination、LU、QR、幂迭代、SVD 基础、最小二乘、插值、样条、FFT 乘法、NTT 乘法
- [ ] `chapter_28_deep_learning_architectures/`：Perceptron、MLP、Autoencoder、VAE core、手写 2D convolution、LeNet、AlexNet、VGG block、ResNet block、DenseNet block、Inception block、depthwise separable convolution、MobileNet block、RNN、LSTM、GRU、Seq2Seq、Attention、Multi-Head Attention、Positional Encoding、Transformer Encoder/Decoder、ViT、U-Net、GAN、DCGAN、Diffusion forward/reverse、GCN、GAT
- [ ] `chapter_29_reinforcement_learning_algorithms/`：MDP、Value Iteration、Policy Iteration、Monte Carlo Prediction/Control、TD(0)、SARSA、Q-learning、Expected SARSA、Double Q-learning、Dyna-Q、REINFORCE、Actor-Critic、UCB Bandit、Thompson Sampling
- [ ] `chapter_30_compression_and_information_coding/`：RLE、Huffman、Canonical Huffman、Arithmetic Coding、LZ77、LZ78、LZW、BWT compression pipeline、Move-to-Front、Delta Encoding、Varint、CRC32、Hamming Code、Reed-Solomon 基础
- [ ] `chapter_31_cryptography_algorithms/`：Caesar、Vigenere、Diffie-Hellman、RSA key generation、RSA encrypt/decrypt、ElGamal、SHA-256 core、HMAC、Merkle Tree、AES S-box/rounds、ECC group operation、ECDSA 基础
- [ ] `chapter_32_compiler_algorithms/`：Regex to NFA、NFA to DFA、DFA minimization、FIRST/FOLLOW、LL(1)、LR(0)、SLR、Shunting-yard、Three-address Code、Basic Blocks、CFG、Dominator、SSA、Liveness Analysis、Graph Coloring Register Allocation
- [ ] `chapter_33_database_algorithms/`：B-tree、B+ tree、LSM tree、Hash Index、Bitmap Index、Nested-loop Join、Hash Join、Sort-merge Join、External Merge Sort、Grace Hash Join、Volcano Iterator、DP Join Ordering、Two-phase Locking、MVCC
- [ ] `chapter_34_distributed_systems_algorithms/`：Consistent Hashing、Rendezvous Hashing、Vector Clock、Lamport Clock、Gossip、Bully Election、Ring Election、Two-phase Commit、Three-phase Commit、Paxos、Raft、CRDT G-Counter、Merkle Tree Sync
- [ ] `chapter_35_operating_system_scheduling/`：FCFS、SJF、SRTF、Round Robin、Priority Scheduling、MLFQ、Rate Monotonic、Earliest Deadline First、FIFO Page Replacement、LRU、Clock、SCAN、C-SCAN
- [ ] `chapter_36_graph_machine_learning_sampling/`：Random Walk、Personalized PageRank、DeepWalk Sampling、Node2Vec Sampling、Negative Sampling、GraphSAGE Neighbor Sampling、LADIES Sampling、Random Edge Sampling、Subgraph Sampling

## 实现规范

每个 Python 实现必须遵守以下规则：

- 核心算法逻辑必须手写实现。
- 不能使用“一击必杀”的库调用直接完成目标算法。
- 标准库只能用于基础容器、类型标注、简单数学工具和测试辅助。
- 可以使用 `numpy` 做数组存储和基础向量化计算，但不能用它替代目标算法本身。
- 可以使用 `torch` 做 tensor、autograd 实验和底层神经网络计算，但不能用高层模块一行替代目标结构。
- 如果文件目标是 heap、binary search、FFT、SVM、ResNet block、BLAST seed extension 等命名算法，源码里必须清楚写出该算法的核心逻辑。
- 不允许用 `heapq` 直接冒充手写堆实现。
- 不允许用 `bisect` 直接冒充手写二分实现。
- 不允许用 `sorted()` 直接冒充手写排序算法。
- 不允许用 `sklearn.svm.SVC` 直接冒充手写 SVM。
- 不允许用 `torch.optim.Adam` 直接冒充手写 Adam。
- 不允许用 `torch.nn.MultiheadAttention` 直接冒充手写 multi-head attention。
- 不允许调用现成 BLAST、FASTA、minimap2、BioPython 接口冒充生信算法实现。
- 每个源码文件开头必须有中文“文件意图”注释，说明实现什么、为什么重要、输入输出、适用场景和复杂度。
- 每个公开函数必须有中文 docstring，说明参数、返回值、边界情况和核心思路。
- 长逻辑、难理解条件分支、循环不变量、证明关键点、边界处理必须写中文注释。
- 实现要遵循 SOLID 和 DRY：函数职责单一，避免复制粘贴，公共逻辑可以抽 helper，但不要过度抽象。
- 每个算法文件必须包含若干个 `main()` 可运行示例。
- 完成一个实现后，把任务清单中的对应条目从 `- [ ]` 改成 `- [x]`。

推荐文件模板：

```python
"""
文件意图：
    本文件手写实现二分查找，用于在有序数组中查找目标值的位置。

适用场景：
    输入数组必须已经按非递减顺序排列。

核心思想：
    每次检查当前区间的中点，根据中点值与目标值的大小关系排除一半搜索空间。

时间复杂度：
    O(log n)

空间复杂度：
    O(1)
"""


def binary_search(nums: list[int], target: int) -> int:
    """
    在有序数组 nums 中查找 target。

    参数：
        nums: 已按非递减顺序排列的整数数组。
        target: 需要查找的目标值。

    返回：
        如果找到 target，返回其下标；否则返回 -1。

    边界情况：
        空数组直接返回 -1。

    关键点：
        循环过程中始终维护闭区间 [left, right]。
    """
    left, right = 0, len(nums) - 1

    # 循环不变量：如果 target 存在，它一定在当前闭区间 [left, right] 中。
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


def main() -> None:
    examples = [
        ([1, 3, 5, 7, 9], 5, 2),
        ([1, 3, 5, 7, 9], 4, -1),
        ([], 10, -1),
    ]

    for nums, target, expected in examples:
        result = binary_search(nums, target)
        assert result == expected, (nums, target, result, expected)

    print("binary_search examples passed")


if __name__ == "__main__":
    main()
```

## 运行示例

运行单个算法文件：

```bash
python3 chapter_01_foundations/001_binary_search.py
```

运行仓库级测试入口：

```bash
python3 main.py
```

随着仓库内容增加，`main.py` 可以作为轻量级 smoke test 入口，从每个章节中导入部分示例进行快速验证。

## 测试要求

每个算法都应包含多个测试用例，而不是只覆盖最简单的正常情况。

建议覆盖：

- 空输入；
- 单元素输入；
- 重复值；
- 已排序输入和逆序输入；
- 图算法中的非连通图；
- 适用场景下的负权边；
- 模运算和下标边界；
- 能体现算法正确性的关键样例。

## 复杂度说明

每个实现都应说明：

- 输入假设；
- 时间复杂度；
- 空间复杂度；
- 关键不变量；
- 算法为什么正确；
- 该算法不适用的场景。

例如，Dijkstra 算法应明确说明标准版本要求边权非负；Bellman-Ford 可以处理负权边，但不能处理从源点可达的负环。

## 开发路线

初始建设顺序：

1. 创建 chapter 目录结构。
2. 添加基础算法和直接可运行的示例。
3. 添加图算法和动态规划实现。
4. 添加竞赛中常用的数据结构。
5. 添加网络流、匹配、字符串算法、计算几何等高级主题。
6. 添加高级竞赛算法，例如树链剖分、DSU on Tree、CDQ、莫队、FFT、NTT。
7. 添加非 AI 生物信息学算法。
8. 添加 ML/DL 优化算法。
9. 添加启发式优化、MCTS 和数学/数值算法。
10. 添加深度学习网络架构的手写核心实现。
11. 添加强化学习、压缩、密码学、编译器、数据库、分布式和操作系统调度算法。
12. 添加图机器学习采样算法。
13. 添加仓库级 `main.py` smoke test 入口。
14. 当实现数量增加后，再补充可选的 `pytest` 测试。

## Commit 信息规范

Commit 信息必须具体、清晰、可审查，总长度不超过 10 行。

推荐格式：

```text
完善算法任务清单与实现规范

- 扩展课程、竞赛、数学、生信和 ML/DL 算法章节
- 明确核心算法必须手写，禁止一击必杀式库调用
- 补充中文注释、测试、SOLID 和 DRY 规范
```

## 项目原则

- 优先保证实现可读，而不是追求过度压缩代码。
- 每个算法尽量自包含，只有在共享工具确实能减少重复时才抽取公共逻辑。
- 示例应能体现边界情况。
- 使用稳定的编号文件名，保持仓库结构容易浏览。
- 说明保持简洁，但技术表述必须准确。

## License

本仓库使用 [MIT License](LICENSE) 开源。
