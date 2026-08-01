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

### Chapter 01：基础方法

- [x] `chapter_01_foundations/001_binary_search.py` — 二分查找
- [x] `chapter_01_foundations/002_lower_bound_upper_bound.py` — 下界与上界
- [x] `chapter_01_foundations/003_prefix_sum.py` — 一维前缀和
- [x] `chapter_01_foundations/004_2d_prefix_sum.py` — 二维前缀和
- [x] `chapter_01_foundations/005_difference_array.py` — 差分数组
- [x] `chapter_01_foundations/006_two_pointers.py` — 双指针
- [x] `chapter_01_foundations/007_sliding_window.py` — 滑动窗口
- [x] `chapter_01_foundations/008_fast_power.py` — 二进制快速幂
- [x] `chapter_01_foundations/009_bit_operations.py` — 位运算
- [x] `chapter_01_foundations/010_recursion_and_iteration.py` — 递归与迭代模式

### Chapter 02：排序与选择

- [x] `chapter_02_sorting_and_selection/001_merge_sort.py` — 归并排序
- [x] `chapter_02_sorting_and_selection/002_quick_sort.py` — 快速排序
- [x] `chapter_02_sorting_and_selection/003_heap_sort.py` — 堆排序
- [x] `chapter_02_sorting_and_selection/004_counting_sort.py` — 计数排序
- [x] `chapter_02_sorting_and_selection/005_radix_sort.py` — 基数排序
- [x] `chapter_02_sorting_and_selection/006_bucket_sort.py` — 桶排序
- [x] `chapter_02_sorting_and_selection/007_quick_select.py` — 快速选择
- [x] `chapter_02_sorting_and_selection/008_median_of_medians.py` — 中位数的中位数选择算法

### Chapter 03：分治算法

- [x] `chapter_03_divide_and_conquer/001_count_inversions.py` — 逆序对计数
- [x] `chapter_03_divide_and_conquer/002_closest_pair_of_points.py` — 最近点对
- [x] `chapter_03_divide_and_conquer/003_karatsuba_multiplication.py` — Karatsuba 乘法
- [x] `chapter_03_divide_and_conquer/004_matrix_multiplication.py` — 分治矩阵乘法
- [x] `chapter_03_divide_and_conquer/005_master_theorem_examples.py` — Master Theorem 递归式示例

### Chapter 04：图遍历

- [x] `chapter_04_graph_traversal/001_bfs.py` — 广度优先搜索
- [x] `chapter_04_graph_traversal/002_dfs.py` — 深度优先搜索
- [x] `chapter_04_graph_traversal/003_connected_components.py` — 连通分量
- [x] `chapter_04_graph_traversal/004_topological_sort.py` — 拓扑排序
- [x] `chapter_04_graph_traversal/005_cycle_detection.py` — 环检测
- [x] `chapter_04_graph_traversal/006_bipartite_check.py` — 二分图检测

### Chapter 05：最短路径

- [ ] `chapter_05_shortest_paths/001_dijkstra.py` — Dijkstra 算法
- [ ] `chapter_05_shortest_paths/002_bellman_ford.py` — Bellman-Ford 算法
- [ ] `chapter_05_shortest_paths/003_floyd_warshall.py` — Floyd-Warshall 算法
- [ ] `chapter_05_shortest_paths/004_zero_one_bfs.py` — 0-1 BFS
- [ ] `chapter_05_shortest_paths/005_dag_shortest_path.py` — DAG 最短路
- [ ] `chapter_05_shortest_paths/006_johnson_algorithm.py` — Johnson 算法

### Chapter 06：最小生成树

- [ ] `chapter_06_minimum_spanning_trees/001_union_find.py` — 并查集
- [ ] `chapter_06_minimum_spanning_trees/002_kruskal.py` — Kruskal 算法
- [ ] `chapter_06_minimum_spanning_trees/003_prim.py` — Prim 算法
- [ ] `chapter_06_minimum_spanning_trees/004_cut_and_cycle_properties.py` — 割性质与环性质
- [ ] `chapter_06_minimum_spanning_trees/005_second_best_mst.py` — 次小生成树

### Chapter 07：贪心算法

- [ ] `chapter_07_greedy_algorithms/001_interval_scheduling.py` — 区间调度
- [ ] `chapter_07_greedy_algorithms/002_activity_selection.py` — 活动选择
- [ ] `chapter_07_greedy_algorithms/003_huffman_coding.py` — Huffman 编码
- [ ] `chapter_07_greedy_algorithms/004_fractional_knapsack.py` — 分数背包
- [ ] `chapter_07_greedy_algorithms/005_exchange_argument_examples.py` — 交换论证示例

### Chapter 08：动态规划 I

- [ ] `chapter_08_dynamic_programming_i/001_fibonacci_variants.py` — Fibonacci 变体
- [ ] `chapter_08_dynamic_programming_i/002_zero_one_knapsack.py` — 0/1 背包
- [ ] `chapter_08_dynamic_programming_i/003_unbounded_knapsack.py` — 完全背包
- [ ] `chapter_08_dynamic_programming_i/004_longest_increasing_subsequence.py` — 最长递增子序列
- [ ] `chapter_08_dynamic_programming_i/005_edit_distance.py` — 编辑距离
- [ ] `chapter_08_dynamic_programming_i/006_coin_change.py` — 零钱兑换
- [ ] `chapter_08_dynamic_programming_i/007_longest_common_subsequence.py` — 最长公共子序列

### Chapter 09：动态规划 II

- [ ] `chapter_09_dynamic_programming_ii/001_bitmask_dp.py` — 状压 DP
- [ ] `chapter_09_dynamic_programming_ii/002_tree_dp.py` — 树形 DP
- [ ] `chapter_09_dynamic_programming_ii/003_digit_dp.py` — 数位 DP
- [ ] `chapter_09_dynamic_programming_ii/004_interval_dp.py` — 区间 DP
- [ ] `chapter_09_dynamic_programming_ii/005_profile_dp.py` — 轮廓线 DP
- [ ] `chapter_09_dynamic_programming_ii/006_convex_hull_trick.py` — 凸包优化
- [ ] `chapter_09_dynamic_programming_ii/007_knuth_optimization.py` — Knuth 优化
- [ ] `chapter_09_dynamic_programming_ii/008_divide_and_conquer_dp.py` — 分治 DP 优化

### Chapter 10：网络流与匹配

- [ ] `chapter_10_network_flow_and_matching/001_ford_fulkerson.py` — Ford-Fulkerson
- [ ] `chapter_10_network_flow_and_matching/002_edmonds_karp.py` — Edmonds-Karp
- [ ] `chapter_10_network_flow_and_matching/003_dinic.py` — Dinic
- [ ] `chapter_10_network_flow_and_matching/004_min_cut.py` — 最小割
- [ ] `chapter_10_network_flow_and_matching/005_bipartite_matching.py` — 二分图匹配
- [ ] `chapter_10_network_flow_and_matching/006_hopcroft_karp.py` — Hopcroft-Karp
- [ ] `chapter_10_network_flow_and_matching/007_min_cost_max_flow.py` — 最小费用最大流

### Chapter 11：高级图算法

- [x] `chapter_11_advanced_graph_algorithms/001_tarjan_scc.py` — Tarjan 强连通分量
- [x] `chapter_11_advanced_graph_algorithms/002_kosaraju_scc.py` — Kosaraju 强连通分量
- [x] `chapter_11_advanced_graph_algorithms/003_bridges.py` — 桥
- [x] `chapter_11_advanced_graph_algorithms/004_articulation_points.py` — 割点
- [x] `chapter_11_advanced_graph_algorithms/005_euler_path.py` — 欧拉路径
- [x] `chapter_11_advanced_graph_algorithms/006_lca_binary_lifting.py` — 倍增 LCA

### Chapter 12：字符串算法

- [x] `chapter_12_string_algorithms/001_kmp.py` — KMP
- [x] `chapter_12_string_algorithms/002_z_algorithm.py` — Z Algorithm
- [x] `chapter_12_string_algorithms/003_rabin_karp.py` — Rabin-Karp
- [x] `chapter_12_string_algorithms/004_trie.py` — Trie
- [x] `chapter_12_string_algorithms/005_aho_corasick.py` — Aho-Corasick
- [x] `chapter_12_string_algorithms/006_suffix_array.py` — 后缀数组
- [x] `chapter_12_string_algorithms/007_lcp_array.py` — LCP 数组
- [x] `chapter_12_string_algorithms/008_manacher.py` — Manacher

### Chapter 13：数论

- [ ] `chapter_13_number_theory/001_gcd_lcm.py` — gcd 与 lcm
- [ ] `chapter_13_number_theory/002_extended_gcd.py` — 扩展 gcd
- [ ] `chapter_13_number_theory/003_modular_exponentiation.py` — 模快速幂
- [ ] `chapter_13_number_theory/004_modular_inverse.py` — 模逆元
- [ ] `chapter_13_number_theory/005_sieve_of_eratosthenes.py` — 埃氏筛
- [ ] `chapter_13_number_theory/006_prime_factorization.py` — 质因数分解
- [ ] `chapter_13_number_theory/007_chinese_remainder_theorem.py` — 中国剩余定理
- [ ] `chapter_13_number_theory/008_miller_rabin.py` — Miller-Rabin 素性测试

### Chapter 14：计算几何

- [ ] `chapter_14_computational_geometry/001_orientation.py` — 方向判断
- [ ] `chapter_14_computational_geometry/002_segment_intersection.py` — 线段相交
- [ ] `chapter_14_computational_geometry/003_polygon_area.py` — 多边形面积
- [ ] `chapter_14_computational_geometry/004_convex_hull.py` — 凸包
- [ ] `chapter_14_computational_geometry/005_rotating_calipers.py` — 旋转卡壳
- [ ] `chapter_14_computational_geometry/006_sweep_line.py` — 扫描线

### Chapter 15：数据结构

- [ ] `chapter_15_data_structures/001_heap.py` — 堆
- [ ] `chapter_15_data_structures/002_monotonic_stack.py` — 单调栈
- [ ] `chapter_15_data_structures/003_monotonic_queue.py` — 单调队列
- [ ] `chapter_15_data_structures/004_fenwick_tree.py` — Fenwick 树
- [ ] `chapter_15_data_structures/005_segment_tree.py` — 线段树
- [ ] `chapter_15_data_structures/006_lazy_segment_tree.py` — 懒标记线段树
- [ ] `chapter_15_data_structures/007_sparse_table.py` — 稀疏表
- [ ] `chapter_15_data_structures/008_disjoint_sparse_table.py` — 离散稀疏表

### Chapter 16：随机化算法

- [ ] `chapter_16_randomized_algorithms/001_randomized_quicksort.py` — 随机化快速排序
- [ ] `chapter_16_randomized_algorithms/002_randomized_select.py` — 随机化选择
- [ ] `chapter_16_randomized_algorithms/003_reservoir_sampling.py` — 蓄水池抽样
- [ ] `chapter_16_randomized_algorithms/004_universal_hashing.py` — 通用哈希
- [ ] `chapter_16_randomized_algorithms/005_monte_carlo_primality.py` — Monte Carlo 素性检查
### Chapter 17：近似算法与复杂性

- [ ] `chapter_17_approximation_and_hardness/001_vertex_cover_approximation.py` — 点覆盖近似
- [ ] `chapter_17_approximation_and_hardness/002_set_cover_greedy.py` — 集合覆盖贪心
- [ ] `chapter_17_approximation_and_hardness/003_bin_packing_heuristics.py` — 装箱启发式
- [ ] `chapter_17_approximation_and_hardness/004_reduction_examples.py` — 归约示例
- [ ] `chapter_17_approximation_and_hardness/005_np_completeness_notes.py` — NP 完全性笔记

### Chapter 18：竞赛常用模式

- [ ] `chapter_18_contest_patterns/001_coordinate_compression.py` — 坐标压缩
- [ ] `chapter_18_contest_patterns/002_offline_queries.py` — 离线查询
- [ ] `chapter_18_contest_patterns/003_binary_search_on_answer.py` — 答案二分
- [ ] `chapter_18_contest_patterns/004_meet_in_the_middle.py` — 折半搜索
- [ ] `chapter_18_contest_patterns/005_sweep_line_events.py` — 事件扫描线
- [ ] `chapter_18_contest_patterns/006_difference_constraints.py` — 差分约束
- [ ] `chapter_18_contest_patterns/007_constructive_patterns.py` — 构造题模式

### Chapter 19：高级竞赛数据结构

- [ ] `chapter_19_advanced_contest_data_structures/001_persistent_segment_tree.py` — 可持久化线段树
- [ ] `chapter_19_advanced_contest_data_structures/002_implicit_treap.py` — 隐式 Treap
- [ ] `chapter_19_advanced_contest_data_structures/003_li_chao_tree.py` — Li Chao Tree
- [ ] `chapter_19_advanced_contest_data_structures/004_order_statistic_tree.py` — 顺序统计树模式
- [ ] `chapter_19_advanced_contest_data_structures/005_rollback_union_find.py` — 可回滚并查集

### Chapter 20：高级树算法

- [x] `chapter_20_advanced_tree_algorithms/001_euler_tour.py` — Euler Tour
- [x] `chapter_20_advanced_tree_algorithms/002_binary_lifting.py` — 倍增
- [x] `chapter_20_advanced_tree_algorithms/003_heavy_light_decomposition.py` — 树链剖分
- [x] `chapter_20_advanced_tree_algorithms/004_dsu_on_tree.py` — DSU on Tree
- [x] `chapter_20_advanced_tree_algorithms/005_centroid_decomposition.py` — 点分治

### Chapter 21：离线与区间查询算法

- [ ] `chapter_21_offline_and_range_query_algorithms/001_mos_algorithm.py` — 莫队
- [ ] `chapter_21_offline_and_range_query_algorithms/002_mos_algorithm_on_tree.py` — 树上莫队
- [ ] `chapter_21_offline_and_range_query_algorithms/003_cdq_divide_and_conquer.py` — CDQ 分治
- [ ] `chapter_21_offline_and_range_query_algorithms/004_parallel_binary_search.py` — 整体二分
- [ ] `chapter_21_offline_and_range_query_algorithms/005_offline_dynamic_connectivity.py` — 离线动态连通性

### Chapter 22：组合数学与多项式算法

- [ ] `chapter_22_combinatorics_and_polynomial_algorithms/001_factorials_and_combinations.py` — 阶乘与组合数
- [ ] `chapter_22_combinatorics_and_polynomial_algorithms/002_inclusion_exclusion.py` — 容斥
- [ ] `chapter_22_combinatorics_and_polynomial_algorithms/003_catalan_numbers.py` — Catalan 数
- [ ] `chapter_22_combinatorics_and_polynomial_algorithms/004_generating_functions.py` — 生成函数
- [ ] `chapter_22_combinatorics_and_polynomial_algorithms/005_fft.py` — FFT
- [ ] `chapter_22_combinatorics_and_polynomial_algorithms/006_ntt.py` — NTT
- [ ] `chapter_22_combinatorics_and_polynomial_algorithms/007_subset_convolution_basics.py` — 子集卷积基础

### Chapter 23：博弈论与构造方法

- [ ] `chapter_23_game_theory_and_constructive_methods/001_nim.py` — Nim
- [ ] `chapter_23_game_theory_and_constructive_methods/002_sprague_grundy.py` — Sprague-Grundy 定理
- [ ] `chapter_23_game_theory_and_constructive_methods/003_mex.py` — mex
- [ ] `chapter_23_game_theory_and_constructive_methods/004_invariant_construction.py` — 不变量构造
- [ ] `chapter_23_game_theory_and_constructive_methods/005_extremal_construction.py` — 极值构造

### Chapter 24：生物信息学算法

- [ ] `chapter_24_bioinformatics/001_naive_dna_matching.py` — 朴素 DNA 精确匹配
- [ ] `chapter_24_bioinformatics/002_kmp_dna_matching.py` — KMP DNA 匹配
- [ ] `chapter_24_bioinformatics/003_rabin_karp_kmer_search.py` — Rabin-Karp k-mer 搜索
- [ ] `chapter_24_bioinformatics/004_aho_corasick_motif_matching.py` — 多模式 motif 匹配
- [ ] `chapter_24_bioinformatics/005_hamming_distance.py` — Hamming 距离
- [ ] `chapter_24_bioinformatics/006_edit_distance.py` — 编辑距离
- [ ] `chapter_24_bioinformatics/007_needleman_wunsch.py` — 全局序列比对
- [ ] `chapter_24_bioinformatics/008_smith_waterman.py` — 局部序列比对
- [ ] `chapter_24_bioinformatics/009_affine_gap_alignment.py` — affine gap 比对
- [ ] `chapter_24_bioinformatics/010_hirschberg_alignment.py` — 线性空间比对
- [ ] `chapter_24_bioinformatics/011_suffix_array.py` — 后缀数组
- [ ] `chapter_24_bioinformatics/012_lcp_array.py` — LCP 数组
- [ ] `chapter_24_bioinformatics/013_burrows_wheeler_transform.py` — Burrows-Wheeler Transform
- [ ] `chapter_24_bioinformatics/014_fm_index.py` — FM-index
- [ ] `chapter_24_bioinformatics/015_fasta_seed_lookup.py` — FASTA 风格 seed 查找
- [ ] `chapter_24_bioinformatics/016_blast_seed_extend.py` — BLAST 风格 seed-and-extend
- [ ] `chapter_24_bioinformatics/017_spaced_seeds.py` — spaced seeds
- [ ] `chapter_24_bioinformatics/018_minimizer_index.py` — minimizer index
- [ ] `chapter_24_bioinformatics/019_winnowing.py` — winnowing
- [ ] `chapter_24_bioinformatics/020_syncmers.py` — syncmers
- [ ] `chapter_24_bioinformatics/021_seed_chaining.py` — seed chaining
- [ ] `chapter_24_bioinformatics/022_banded_dynamic_programming.py` — 带状 DP 比对
- [ ] `chapter_24_bioinformatics/023_minimap2_style_mapping.py` — minimap2 风格长读段 mapping
- [ ] `chapter_24_bioinformatics/024_progressive_msa.py` — progressive MSA
- [ ] `chapter_24_bioinformatics/025_profile_alignment.py` — profile alignment
- [ ] `chapter_24_bioinformatics/026_partial_order_alignment.py` — partial-order alignment
- [ ] `chapter_24_bioinformatics/027_overlap_layout_consensus.py` — OLC 组装
- [ ] `chapter_24_bioinformatics/028_de_bruijn_graph_assembly.py` — de Bruijn graph 组装
- [ ] `chapter_24_bioinformatics/029_eulerian_assembly.py` — Eulerian path 组装建模
- [ ] `chapter_24_bioinformatics/030_string_graph_assembly.py` — string graph 组装
- [ ] `chapter_24_bioinformatics/031_unitig_compaction.py` — unitig 压缩
- [ ] `chapter_24_bioinformatics/032_viterbi_hmm_genotyping.py` — HMM genotyping 的 Viterbi 解码
- [ ] `chapter_24_bioinformatics/033_forward_backward.py` — Forward-Backward 算法
- [ ] `chapter_24_bioinformatics/034_upgma_tree.py` — UPGMA 系统发育树
- [ ] `chapter_24_bioinformatics/035_neighbor_joining.py` — neighbor joining
- [ ] `chapter_24_bioinformatics/036_maximum_parsimony.py` — maximum parsimony
- [ ] `chapter_24_bioinformatics/037_kmer_counting.py` — k-mer 计数
- [ ] `chapter_24_bioinformatics/038_bloom_filter_kmers.py` — k-mer Bloom Filter
- [ ] `chapter_24_bioinformatics/039_count_min_sketch_kmers.py` — k-mer Count-Min Sketch
- [ ] `chapter_24_bioinformatics/040_minhash_sequence_distance.py` — MinHash 序列距离
- [ ] `chapter_24_bioinformatics/041_mash_style_distance.py` — Mash 风格 sketch 距离
- [ ] `chapter_24_bioinformatics/042_variation_graph_basics.py` — variation graph 基础
- [ ] `chapter_24_bioinformatics/043_sequence_to_graph_alignment.py` — sequence-to-graph alignment
- [ ] `chapter_24_bioinformatics/044_graph_indexing_basics.py` — graph indexing 基础
- [ ] `chapter_24_bioinformatics/045_pangenome_mapping_basics.py` — pangenome mapping 基础

### Chapter 25：ML/DL 优化算法

- [ ] `chapter_25_ml_dl_optimization/001_gradient_descent.py` — batch gradient descent
- [ ] `chapter_25_ml_dl_optimization/002_stochastic_gradient_descent.py` — stochastic gradient descent
- [ ] `chapter_25_ml_dl_optimization/003_mini_batch_gradient_descent.py` — mini-batch gradient descent
- [ ] `chapter_25_ml_dl_optimization/004_momentum.py` — momentum
- [ ] `chapter_25_ml_dl_optimization/005_nesterov_accelerated_gradient.py` — Nesterov 加速梯度
- [ ] `chapter_25_ml_dl_optimization/006_adagrad.py` — AdaGrad
- [ ] `chapter_25_ml_dl_optimization/007_rmsprop.py` — RMSProp
- [ ] `chapter_25_ml_dl_optimization/008_adam.py` — Adam
- [ ] `chapter_25_ml_dl_optimization/009_adamw.py` — AdamW
- [ ] `chapter_25_ml_dl_optimization/010_nadam.py` — Nadam
- [ ] `chapter_25_ml_dl_optimization/011_amsgrad.py` — AMSGrad
- [ ] `chapter_25_ml_dl_optimization/012_learning_rate_decay.py` — 学习率衰减
- [ ] `chapter_25_ml_dl_optimization/013_cosine_annealing.py` — cosine annealing
- [ ] `chapter_25_ml_dl_optimization/014_warmup_schedule.py` — warmup schedule
- [ ] `chapter_25_ml_dl_optimization/015_gradient_clipping.py` — 梯度裁剪
- [ ] `chapter_25_ml_dl_optimization/016_weight_decay.py` — weight decay
- [ ] `chapter_25_ml_dl_optimization/017_l1_l2_regularization.py` — L1/L2 正则
- [ ] `chapter_25_ml_dl_optimization/018_early_stopping.py` — early stopping
- [ ] `chapter_25_ml_dl_optimization/019_batch_normalization_math.py` — BatchNorm 优化行为
- [ ] `chapter_25_ml_dl_optimization/020_layer_normalization_math.py` — LayerNorm 优化行为
- [ ] `chapter_25_ml_dl_optimization/021_newton_method.py` — Newton 方法
- [ ] `chapter_25_ml_dl_optimization/022_quasi_newton_bfgs.py` — BFGS
- [ ] `chapter_25_ml_dl_optimization/023_l_bfgs.py` — L-BFGS
- [ ] `chapter_25_ml_dl_optimization/024_conjugate_gradient.py` — 共轭梯度
- [ ] `chapter_25_ml_dl_optimization/025_coordinate_descent.py` — 坐标下降
- [ ] `chapter_25_ml_dl_optimization/026_projected_gradient_descent.py` — 投影梯度下降
- [ ] `chapter_25_ml_dl_optimization/027_proximal_gradient_method.py` — 近端梯度
- [ ] `chapter_25_ml_dl_optimization/028_mirror_descent.py` — mirror descent
- [ ] `chapter_25_ml_dl_optimization/029_dual_averaging.py` — dual averaging
- [ ] `chapter_25_ml_dl_optimization/030_gradient_checking.py` — 数值梯度检查
- [ ] `chapter_25_ml_dl_optimization/031_backtracking_line_search.py` — backtracking line search
- [ ] `chapter_25_ml_dl_optimization/032_hyperparameter_grid_search.py` — grid search
- [ ] `chapter_25_ml_dl_optimization/033_random_search.py` — random search
- [ ] `chapter_25_ml_dl_optimization/034_bayesian_optimization_basics.py` — Bayesian optimization 基础

### Chapter 26：启发式搜索与元启发式优化

- [ ] `chapter_26_heuristic_search_and_metaheuristics/001_hill_climbing.py` — 爬山法
- [ ] `chapter_26_heuristic_search_and_metaheuristics/002_random_restart_hill_climbing.py` — 随机重启爬山
- [ ] `chapter_26_heuristic_search_and_metaheuristics/003_simulated_annealing.py` — 模拟退火
- [ ] `chapter_26_heuristic_search_and_metaheuristics/004_particle_swarm_optimization.py` — 粒子群优化
- [ ] `chapter_26_heuristic_search_and_metaheuristics/005_genetic_algorithm.py` — 遗传算法
- [ ] `chapter_26_heuristic_search_and_metaheuristics/006_differential_evolution.py` — 差分进化
- [ ] `chapter_26_heuristic_search_and_metaheuristics/007_ant_colony_optimization.py` — 蚁群算法
- [ ] `chapter_26_heuristic_search_and_metaheuristics/008_tabu_search.py` — 禁忌搜索
- [ ] `chapter_26_heuristic_search_and_metaheuristics/009_beam_search.py` — Beam Search
- [ ] `chapter_26_heuristic_search_and_metaheuristics/010_a_star.py` — A* 搜索
- [ ] `chapter_26_heuristic_search_and_metaheuristics/011_ida_star.py` — IDA* 搜索
- [ ] `chapter_26_heuristic_search_and_metaheuristics/012_monte_carlo_tree_search.py` — Monte Carlo Tree Search
- [ ] `chapter_26_heuristic_search_and_metaheuristics/013_upper_confidence_bound.py` — UCB 选择
- [ ] `chapter_26_heuristic_search_and_metaheuristics/014_cross_entropy_method.py` — 交叉熵方法
- [ ] `chapter_26_heuristic_search_and_metaheuristics/015_covariance_matrix_adaptation.py` — CMA-ES 基础

### Chapter 27：数学与数值算法

- [ ] `chapter_27_mathematical_and_numerical_algorithms/001_finite_difference_derivative.py` — 有限差分求导
- [ ] `chapter_27_mathematical_and_numerical_algorithms/002_gradient_jacobian_hessian.py` — 梯度、Jacobian 与 Hessian
- [ ] `chapter_27_mathematical_and_numerical_algorithms/003_newton_root_finding.py` — Newton 求根
- [ ] `chapter_27_mathematical_and_numerical_algorithms/004_bisection_root_finding.py` — 二分求根
- [ ] `chapter_27_mathematical_and_numerical_algorithms/005_secant_method.py` — 割线法
- [ ] `chapter_27_mathematical_and_numerical_algorithms/006_fixed_point_iteration.py` — 不动点迭代
- [ ] `chapter_27_mathematical_and_numerical_algorithms/007_trapezoidal_rule.py` — 梯形积分
- [ ] `chapter_27_mathematical_and_numerical_algorithms/008_simpson_rule.py` — Simpson 积分
- [ ] `chapter_27_mathematical_and_numerical_algorithms/009_adaptive_simpson.py` — 自适应 Simpson
- [ ] `chapter_27_mathematical_and_numerical_algorithms/010_gaussian_quadrature.py` — Gaussian quadrature 基础
- [ ] `chapter_27_mathematical_and_numerical_algorithms/011_monte_carlo_integration.py` — Monte Carlo 积分
- [ ] `chapter_27_mathematical_and_numerical_algorithms/012_euler_method_ode.py` — Euler ODE 方法
- [ ] `chapter_27_mathematical_and_numerical_algorithms/013_runge_kutta_4.py` — RK4
- [ ] `chapter_27_mathematical_and_numerical_algorithms/014_gaussian_elimination.py` — Gaussian elimination
- [ ] `chapter_27_mathematical_and_numerical_algorithms/015_lu_decomposition.py` — LU 分解
- [ ] `chapter_27_mathematical_and_numerical_algorithms/016_qr_decomposition.py` — QR 分解
- [ ] `chapter_27_mathematical_and_numerical_algorithms/017_power_iteration.py` — 幂迭代
- [ ] `chapter_27_mathematical_and_numerical_algorithms/018_svd_basics.py` — SVD 基础
- [ ] `chapter_27_mathematical_and_numerical_algorithms/019_least_squares.py` — 最小二乘
- [ ] `chapter_27_mathematical_and_numerical_algorithms/020_polynomial_interpolation.py` — 多项式插值
- [ ] `chapter_27_mathematical_and_numerical_algorithms/021_lagrange_interpolation.py` — Lagrange 插值
- [ ] `chapter_27_mathematical_and_numerical_algorithms/022_newton_interpolation.py` — Newton 插值
- [ ] `chapter_27_mathematical_and_numerical_algorithms/023_spline_interpolation.py` — 样条插值基础
- [ ] `chapter_27_mathematical_and_numerical_algorithms/024_fast_fourier_transform_multiplication.py` — FFT 乘法
- [ ] `chapter_27_mathematical_and_numerical_algorithms/025_number_theoretic_transform_multiplication.py` — NTT 乘法

### Chapter 28：深度学习网络架构

- [ ] `chapter_28_deep_learning_architectures/001_perceptron.py` — Perceptron
- [ ] `chapter_28_deep_learning_architectures/002_multilayer_perceptron.py` — MLP
- [ ] `chapter_28_deep_learning_architectures/003_autoencoder.py` — Autoencoder
- [ ] `chapter_28_deep_learning_architectures/004_variational_autoencoder_core.py` — VAE core
- [ ] `chapter_28_deep_learning_architectures/005_manual_2d_convolution.py` — 手写 2D convolution
- [ ] `chapter_28_deep_learning_architectures/006_lenet.py` — LeNet
- [ ] `chapter_28_deep_learning_architectures/007_alexnet.py` — AlexNet
- [ ] `chapter_28_deep_learning_architectures/008_vgg_block.py` — VGG block
- [ ] `chapter_28_deep_learning_architectures/009_resnet_basic_block.py` — ResNet basic block
- [ ] `chapter_28_deep_learning_architectures/010_resnet_bottleneck_block.py` — ResNet bottleneck block
- [ ] `chapter_28_deep_learning_architectures/011_densenet_block.py` — DenseNet block
- [ ] `chapter_28_deep_learning_architectures/012_inception_block.py` — Inception block
- [ ] `chapter_28_deep_learning_architectures/013_depthwise_separable_convolution.py` — depthwise separable convolution
- [ ] `chapter_28_deep_learning_architectures/014_mobilenet_block.py` — MobileNet block
- [ ] `chapter_28_deep_learning_architectures/015_rnn_cell.py` — RNN cell
- [ ] `chapter_28_deep_learning_architectures/016_lstm_cell.py` — LSTM cell
- [ ] `chapter_28_deep_learning_architectures/017_gru_cell.py` — GRU cell
- [ ] `chapter_28_deep_learning_architectures/018_seq2seq_encoder_decoder.py` — Seq2Seq encoder-decoder
- [ ] `chapter_28_deep_learning_architectures/019_scaled_dot_product_attention.py` — scaled dot-product attention
- [ ] `chapter_28_deep_learning_architectures/020_multi_head_attention.py` — multi-head attention
- [ ] `chapter_28_deep_learning_architectures/021_positional_encoding.py` — positional encoding
- [ ] `chapter_28_deep_learning_architectures/022_transformer_encoder_block.py` — Transformer encoder block
- [ ] `chapter_28_deep_learning_architectures/023_transformer_decoder_block.py` — Transformer decoder block
- [ ] `chapter_28_deep_learning_architectures/024_vision_transformer_patch_embedding.py` — ViT patch embedding
- [ ] `chapter_28_deep_learning_architectures/025_vision_transformer_block.py` — ViT block
- [ ] `chapter_28_deep_learning_architectures/026_unet.py` — U-Net
- [ ] `chapter_28_deep_learning_architectures/027_gan_minimal.py` — minimal GAN
- [ ] `chapter_28_deep_learning_architectures/028_dcgan_blocks.py` — DCGAN blocks
- [ ] `chapter_28_deep_learning_architectures/029_diffusion_forward_process.py` — diffusion forward process
- [ ] `chapter_28_deep_learning_architectures/030_diffusion_reverse_step.py` — diffusion reverse step
- [ ] `chapter_28_deep_learning_architectures/031_graph_convolution_layer.py` — GCN layer
- [ ] `chapter_28_deep_learning_architectures/032_graph_attention_layer.py` — GAT layer

### Chapter 29：强化学习算法

- [ ] `chapter_29_reinforcement_learning_algorithms/001_markov_decision_process.py` — MDP 基础
- [ ] `chapter_29_reinforcement_learning_algorithms/002_value_iteration.py` — Value Iteration
- [ ] `chapter_29_reinforcement_learning_algorithms/003_policy_iteration.py` — Policy Iteration
- [ ] `chapter_29_reinforcement_learning_algorithms/004_monte_carlo_prediction.py` — Monte Carlo prediction
- [ ] `chapter_29_reinforcement_learning_algorithms/005_monte_carlo_control.py` — Monte Carlo control
- [ ] `chapter_29_reinforcement_learning_algorithms/006_temporal_difference_prediction.py` — TD(0)
- [ ] `chapter_29_reinforcement_learning_algorithms/007_sarsa.py` — SARSA
- [ ] `chapter_29_reinforcement_learning_algorithms/008_q_learning.py` — Q-learning
- [ ] `chapter_29_reinforcement_learning_algorithms/009_expected_sarsa.py` — Expected SARSA
- [ ] `chapter_29_reinforcement_learning_algorithms/010_double_q_learning.py` — Double Q-learning
- [ ] `chapter_29_reinforcement_learning_algorithms/011_dyna_q.py` — Dyna-Q
- [ ] `chapter_29_reinforcement_learning_algorithms/012_policy_gradient_reinforce.py` — REINFORCE
- [ ] `chapter_29_reinforcement_learning_algorithms/013_actor_critic_basics.py` — Actor-Critic 基础
- [ ] `chapter_29_reinforcement_learning_algorithms/014_upper_confidence_bound_bandit.py` — UCB bandit
- [ ] `chapter_29_reinforcement_learning_algorithms/015_thompson_sampling.py` — Thompson sampling

### Chapter 30：压缩与信息编码

- [x] `chapter_30_compression_and_information_coding/001_run_length_encoding.py` — RLE
- [x] `chapter_30_compression_and_information_coding/002_huffman_coding.py` — Huffman 编码
- [x] `chapter_30_compression_and_information_coding/003_canonical_huffman.py` — Canonical Huffman
- [ ] `chapter_30_compression_and_information_coding/004_arithmetic_coding.py` — Arithmetic Coding
- [ ] `chapter_30_compression_and_information_coding/005_lz77.py` — LZ77
- [ ] `chapter_30_compression_and_information_coding/006_lz78.py` — LZ78
- [ ] `chapter_30_compression_and_information_coding/007_lzw.py` — LZW
- [ ] `chapter_30_compression_and_information_coding/008_bwt_compression_pipeline.py` — BWT compression pipeline
- [ ] `chapter_30_compression_and_information_coding/009_move_to_front.py` — Move-to-Front
- [ ] `chapter_30_compression_and_information_coding/010_delta_encoding.py` — Delta Encoding
- [ ] `chapter_30_compression_and_information_coding/011_varint_encoding.py` — Varint
- [ ] `chapter_30_compression_and_information_coding/012_crc32.py` — CRC32
- [ ] `chapter_30_compression_and_information_coding/013_hamming_code.py` — Hamming Code
- [ ] `chapter_30_compression_and_information_coding/014_reed_solomon_basics.py` — Reed-Solomon 基础

### Chapter 31：密码学算法

- [ ] `chapter_31_cryptography_algorithms/001_caesar_cipher.py` — Caesar cipher
- [ ] `chapter_31_cryptography_algorithms/002_vigenere_cipher.py` — Vigenere cipher
- [ ] `chapter_31_cryptography_algorithms/003_diffie_hellman.py` — Diffie-Hellman
- [ ] `chapter_31_cryptography_algorithms/004_rsa_key_generation.py` — RSA key generation
- [ ] `chapter_31_cryptography_algorithms/005_rsa_encrypt_decrypt.py` — RSA encrypt/decrypt
- [ ] `chapter_31_cryptography_algorithms/006_elgamal.py` — ElGamal
- [ ] `chapter_31_cryptography_algorithms/007_sha256_core.py` — SHA-256 core
- [ ] `chapter_31_cryptography_algorithms/008_hmac.py` — HMAC
- [ ] `chapter_31_cryptography_algorithms/009_merkle_tree.py` — Merkle Tree
- [ ] `chapter_31_cryptography_algorithms/010_aes_sbox_and_rounds.py` — AES S-box 与 round
- [ ] `chapter_31_cryptography_algorithms/011_elliptic_curve_group.py` — 椭圆曲线群运算
- [ ] `chapter_31_cryptography_algorithms/012_ecdsa_basics.py` — ECDSA 基础

### Chapter 32：编译器算法

- [ ] `chapter_32_compiler_algorithms/001_regex_to_nfa.py` — Regex to NFA
- [ ] `chapter_32_compiler_algorithms/002_nfa_to_dfa.py` — NFA to DFA
- [ ] `chapter_32_compiler_algorithms/003_dfa_minimization.py` — DFA 最小化
- [ ] `chapter_32_compiler_algorithms/004_first_follow_sets.py` — FIRST/FOLLOW 集
- [ ] `chapter_32_compiler_algorithms/005_ll1_parsing_table.py` — LL(1) parsing table
- [ ] `chapter_32_compiler_algorithms/006_lr0_items.py` — LR(0) items
- [ ] `chapter_32_compiler_algorithms/007_slr_parsing.py` — SLR parsing
- [ ] `chapter_32_compiler_algorithms/008_shunting_yard.py` — Shunting-yard
- [ ] `chapter_32_compiler_algorithms/009_three_address_code.py` — Three-address Code
- [ ] `chapter_32_compiler_algorithms/010_basic_blocks_cfg.py` — Basic Blocks 与 CFG
- [ ] `chapter_32_compiler_algorithms/011_dominators.py` — Dominator 计算
- [ ] `chapter_32_compiler_algorithms/012_static_single_assignment.py` — SSA 构造基础
- [ ] `chapter_32_compiler_algorithms/013_liveness_analysis.py` — Liveness Analysis
- [ ] `chapter_32_compiler_algorithms/014_graph_coloring_register_allocation.py` — 图着色寄存器分配

### Chapter 33：数据库算法

- [ ] `chapter_33_database_algorithms/001_b_tree.py` — B-tree
- [ ] `chapter_33_database_algorithms/002_b_plus_tree.py` — B+ tree
- [ ] `chapter_33_database_algorithms/003_lsm_tree_basics.py` — LSM tree 基础
- [ ] `chapter_33_database_algorithms/004_hash_index.py` — Hash Index
- [ ] `chapter_33_database_algorithms/005_bitmap_index.py` — Bitmap Index
- [ ] `chapter_33_database_algorithms/006_nested_loop_join.py` — Nested-loop Join
- [ ] `chapter_33_database_algorithms/007_hash_join.py` — Hash Join
- [ ] `chapter_33_database_algorithms/008_sort_merge_join.py` — Sort-merge Join
- [ ] `chapter_33_database_algorithms/009_external_merge_sort.py` — External Merge Sort
- [ ] `chapter_33_database_algorithms/010_grace_hash_join.py` — Grace Hash Join
- [ ] `chapter_33_database_algorithms/011_volcano_iterator_model.py` — Volcano Iterator Model
- [ ] `chapter_33_database_algorithms/012_dynamic_programming_join_order.py` — DP Join Ordering
- [ ] `chapter_33_database_algorithms/013_two_phase_locking.py` — Two-phase Locking
- [ ] `chapter_33_database_algorithms/014_mvcc_basics.py` — MVCC 基础

### Chapter 34：分布式系统算法

- [ ] `chapter_34_distributed_systems_algorithms/001_consistent_hashing.py` — Consistent Hashing
- [ ] `chapter_34_distributed_systems_algorithms/002_rendezvous_hashing.py` — Rendezvous Hashing
- [ ] `chapter_34_distributed_systems_algorithms/003_vector_clock.py` — Vector Clock
- [ ] `chapter_34_distributed_systems_algorithms/004_lamport_clock.py` — Lamport Clock
- [ ] `chapter_34_distributed_systems_algorithms/005_gossip_protocol.py` — Gossip Protocol
- [ ] `chapter_34_distributed_systems_algorithms/006_leader_election_bully.py` — Bully Leader Election
- [ ] `chapter_34_distributed_systems_algorithms/007_leader_election_ring.py` — Ring Leader Election
- [ ] `chapter_34_distributed_systems_algorithms/008_two_phase_commit.py` — Two-phase Commit
- [ ] `chapter_34_distributed_systems_algorithms/009_three_phase_commit.py` — Three-phase Commit
- [ ] `chapter_34_distributed_systems_algorithms/010_paxos_basics.py` — Paxos 基础
- [ ] `chapter_34_distributed_systems_algorithms/011_raft_basics.py` — Raft 基础
- [ ] `chapter_34_distributed_systems_algorithms/012_crdt_g_counter.py` — CRDT G-Counter
- [ ] `chapter_34_distributed_systems_algorithms/013_merkle_tree_sync.py` — Merkle Tree Sync

### Chapter 35：操作系统调度算法

- [ ] `chapter_35_operating_system_scheduling/001_first_come_first_served.py` — FCFS
- [ ] `chapter_35_operating_system_scheduling/002_shortest_job_first.py` — SJF
- [ ] `chapter_35_operating_system_scheduling/003_shortest_remaining_time_first.py` — SRTF
- [ ] `chapter_35_operating_system_scheduling/004_round_robin.py` — Round Robin
- [ ] `chapter_35_operating_system_scheduling/005_priority_scheduling.py` — Priority Scheduling
- [ ] `chapter_35_operating_system_scheduling/006_multilevel_feedback_queue.py` — MLFQ
- [ ] `chapter_35_operating_system_scheduling/007_rate_monotonic_scheduling.py` — Rate Monotonic
- [ ] `chapter_35_operating_system_scheduling/008_earliest_deadline_first.py` — Earliest Deadline First
- [ ] `chapter_35_operating_system_scheduling/009_fifo_page_replacement.py` — FIFO Page Replacement
- [ ] `chapter_35_operating_system_scheduling/010_lru_page_replacement.py` — LRU
- [ ] `chapter_35_operating_system_scheduling/011_clock_page_replacement.py` — Clock
- [ ] `chapter_35_operating_system_scheduling/012_scan_disk_scheduling.py` — SCAN
- [ ] `chapter_35_operating_system_scheduling/013_c_scan_disk_scheduling.py` — C-SCAN

### Chapter 36：图机器学习采样算法

- [ ] `chapter_36_graph_machine_learning_sampling/001_random_walk.py` — Random Walk
- [ ] `chapter_36_graph_machine_learning_sampling/002_personalized_pagerank.py` — Personalized PageRank
- [ ] `chapter_36_graph_machine_learning_sampling/003_deepwalk_sampling.py` — DeepWalk Sampling
- [ ] `chapter_36_graph_machine_learning_sampling/004_node2vec_sampling.py` — Node2Vec Sampling
- [ ] `chapter_36_graph_machine_learning_sampling/005_negative_sampling.py` — Negative Sampling
- [ ] `chapter_36_graph_machine_learning_sampling/006_graphsage_neighbor_sampling.py` — GraphSAGE Neighbor Sampling
- [ ] `chapter_36_graph_machine_learning_sampling/007_ladies_sampling_basics.py` — LADIES Sampling 基础
- [ ] `chapter_36_graph_machine_learning_sampling/008_random_edge_sampling.py` — Random Edge Sampling
- [ ] `chapter_36_graph_machine_learning_sampling/009_subgraph_sampling.py` — Subgraph Sampling

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
