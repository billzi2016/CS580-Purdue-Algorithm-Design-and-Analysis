# CS 580: Algorithm Design and Analysis

中文版本: [README.cn.md](README.cn.md)

This repository organizes implementations, notes, and runnable examples for **Purdue University CS 580: Algorithm Design and Analysis**, while also mapping the implementation plan to a broader set of Purdue Computer Science courses. It additionally covers LeetCode patterns, Codeforces-style competitive programming, mathematical algorithms, heuristic optimization, Monte Carlo Tree Search, machine-learning optimization, deep-learning architectures, and classical non-AI bioinformatics algorithms. The goal is to build a clean, chapter-based algorithm reference that connects Purdue course topics with practical implementation patterns.

Over the past eight years, I have organized these notes and implementations through my work as a TA for seven Purdue CS courses: **Numerical Methods**, **Data Mining and Machine Learning**, **Introduction to Cryptography**, **Algorithm Design, Analysis, and Implementation**, **Programming Languages**, **Statistical Machine Learning**, and **Database Systems**. The repository is intended to consolidate the core methods from those areas into a maintainable, implementation-first algorithm handbook.

The repository is structured so that each algorithm is easy to find, test, and extend. Every implementation should include a concise explanation, complexity analysis, and executable examples through a local `main` entry point.

## Repository Structure

Algorithms are grouped by chapter. Each chapter directory focuses on one major topic area, and each file inside the chapter uses a numbered prefix for stable ordering.

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

Recommended file format:

```text
chapter_XX_topic_name/
  001_algorithm_name.py
  002_algorithm_name.py
  003_algorithm_name.py
```

Each algorithm file should provide:

- a clear implementation;
- several example test cases;
- time and space complexity;
- edge case coverage;
- a `main` block or callable demo function for quick verification.

## Purdue Course Coverage Map

This repository starts from CS 580 and expands into a broader Purdue CS algorithm implementation map. It is not a replacement for official syllabi; it is an implementation-oriented reference that connects course topics to hand-written algorithms and runnable examples.

| Purdue Course | Course Name | Repository Coverage |
|---|---|---|
| CS 18000 | Problem Solving and Object-Oriented Programming | basic programming patterns, recursion, iteration, testing examples |
| CS 18200 | Foundations of Computer Science | discrete math foundations, proof ideas, recurrence reasoning, combinatorics |
| CS 24000 | Programming Laboratory in C | low-level implementation discipline, memory-aware algorithm examples |
| CS 25000 | Computer Architecture | bit operations, integer representation, cache-aware reasoning, low-level performance notes |
| CS 25100 | Data Structures and Algorithms | arrays, linked lists, stacks, queues, trees, heaps, hash tables, graphs, union-find |
| CS 25200 | Systems Programming | systems-oriented data structures, file-oriented examples, scheduling-related simulations |
| CS 25300 | Data Structures and Algorithms for DS/AI | data structures used in data science and AI pipelines |
| CS 31100 | Competitive Programming II | contest patterns, graph algorithms, DP, number theory, data structures |
| CS 31400 | Numerical Methods | numerical differentiation, integration, root finding, ODE solvers, numerical linear algebra |
| CS 33400 | Fundamentals of Computer Graphics | computational geometry, transformations, interpolation, spatial algorithms |
| CS 34800 | Information Systems | database indexing, query execution, join algorithms, transaction concepts |
| CS 35200 | Compilers: Principles and Practice | automata, parsing, CFGs, SSA, liveness analysis, register allocation |
| CS 35400 | Operating Systems | scheduling algorithms, page replacement, disk scheduling, concurrency-related models |
| CS 35500 | Introduction to Cryptography | modular arithmetic, RSA, Diffie-Hellman, hashing, Merkle trees, ECC basics |
| CS 37300 | Data Mining and Machine Learning | optimization, sampling, clustering-related primitives, ML algorithm foundations |
| CS 38100 | Introduction to the Analysis of Algorithms | sorting, divide and conquer, greedy, DP, graph algorithms, flows, NP-completeness |
| CS 41100 | Competitive Programming III | advanced contest data structures, HLD, Mo's algorithm, CDQ, FFT/NTT, constructive methods |
| CS 42200 | Computer Networks | graph routing ideas, distributed coordination, hashing, protocol-state algorithms |
| CS 42600 | Computer Security | cryptographic primitives, hashing, Merkle trees, security-related algorithm foundations |
| CS 44000 | Large Scale Data Analytics | sketches, streaming algorithms, sampling, external-memory and large-scale processing |
| CS 44800 | Introduction to Relational Database Systems | B-trees, B+ trees, joins, query planning, indexing, MVCC basics |
| CS 47100 | Introduction to Artificial Intelligence | search algorithms, A*, IDA*, MCTS, optimization, planning foundations |
| CS 47800 | Introduction to Bioinformatics | DNA matching, alignment, BLAST/FASTA-style search, genome assembly, pangenome graphs |
| CS 48900 | Embedded Systems | bit-level algorithms, scheduling, memory-aware implementations |
| CS 53000 | Introduction to Scientific Visualization | numerical methods, geometry, interpolation, graph and grid algorithms |
| CS 53500 | Interactive Computer Graphics | geometry, spatial data structures, interpolation, transformations |
| CS 53600 | Data Communication and Computer Networks | shortest paths, routing, hashing, distributed algorithms |
| CS 54100 | Database Systems | storage structures, query optimization, joins, concurrency control |
| CS 55100 | Cloud Computing Fundamentals | distributed algorithms, consistent hashing, replication, consensus basics |
| CS 55800 | Introduction to Robot Learning | optimization, search, planning, reinforcement-learning foundations |
| CS 56500 | Programming Languages | parsing, automata, program analysis, compiler algorithms |
| CS 57800 | Statistical Machine Learning | optimization algorithms, gradient methods, regularization, model-training primitives |
| CS 58000 | Algorithm Design, Analysis, and Implementation | full algorithm-design core: graph algorithms, flow, LP ideas, approximation, randomized algorithms, NP-completeness |
| CS 58400 | Theory of Computation and Computational Complexity | automata, reductions, complexity, NP-completeness |
| CS 58500 | Theoretical Computer Science Toolkit | mathematical toolkit, probability, combinatorics, proof techniques |
| CS 53100 | Computational Geometry | geometric primitives, convex hull, sweep line, closest pair, spatial algorithms |
| CS 55500 | Cryptography | number theory, public-key crypto, hashing, authentication primitives |
| CS 590AA | Approximation Algorithms | approximation, LP rounding ideas, greedy approximation patterns |
| CS 590RA | Randomized Algorithms | randomized algorithms, hashing, sampling, Monte Carlo methods |
| CS 65500 | Advanced Cryptology | advanced cryptographic foundations and number-theoretic primitives |

## Algorithm Task List

The chapter map is designed to cover standard algorithm-design material, LeetCode-style interview algorithms, Codeforces-style competitive-programming techniques, mathematical algorithms, classical non-AI bioinformatics algorithms, heuristic search and optimization, ML/DL optimization algorithms, deep-learning architectures, compression, cryptography, compiler algorithms, database algorithms, distributed systems algorithms, operating-system scheduling, reinforcement learning, and graph machine-learning sampling. Completed implementations can be marked with `- [x]`.

### Chapter 01: Foundations

- [x] `chapter_01_foundations/001_binary_search.py` — binary search
- [x] `chapter_01_foundations/002_lower_bound_upper_bound.py` — lower bound and upper bound
- [x] `chapter_01_foundations/003_prefix_sum.py` — prefix sum
- [x] `chapter_01_foundations/004_2d_prefix_sum.py` — 2D prefix sum
- [x] `chapter_01_foundations/005_difference_array.py` — difference array
- [x] `chapter_01_foundations/006_two_pointers.py` — two pointers
- [x] `chapter_01_foundations/007_sliding_window.py` — sliding window
- [x] `chapter_01_foundations/008_fast_power.py` — binary exponentiation
- [x] `chapter_01_foundations/009_bit_operations.py` — bit operations
- [x] `chapter_01_foundations/010_recursion_and_iteration.py` — recursion and iteration patterns

### Chapter 02: Sorting and Selection

- [x] `chapter_02_sorting_and_selection/001_merge_sort.py` — merge sort
- [x] `chapter_02_sorting_and_selection/002_quick_sort.py` — quick sort
- [x] `chapter_02_sorting_and_selection/003_heap_sort.py` — heap sort
- [x] `chapter_02_sorting_and_selection/004_counting_sort.py` — counting sort
- [x] `chapter_02_sorting_and_selection/005_radix_sort.py` — radix sort
- [x] `chapter_02_sorting_and_selection/006_bucket_sort.py` — bucket sort
- [x] `chapter_02_sorting_and_selection/007_quick_select.py` — quickselect
- [x] `chapter_02_sorting_and_selection/008_median_of_medians.py` — deterministic selection

### Chapter 03: Divide and Conquer

- [x] `chapter_03_divide_and_conquer/001_count_inversions.py` — inversion counting
- [x] `chapter_03_divide_and_conquer/002_closest_pair_of_points.py` — closest pair of points
- [x] `chapter_03_divide_and_conquer/003_karatsuba_multiplication.py` — Karatsuba multiplication
- [x] `chapter_03_divide_and_conquer/004_matrix_multiplication.py` — divide-and-conquer matrix multiplication
- [x] `chapter_03_divide_and_conquer/005_master_theorem_examples.py` — recurrence examples

### Chapter 04: Graph Traversal

- [x] `chapter_04_graph_traversal/001_bfs.py` — breadth-first search
- [x] `chapter_04_graph_traversal/002_dfs.py` — depth-first search
- [x] `chapter_04_graph_traversal/003_connected_components.py` — connected components
- [x] `chapter_04_graph_traversal/004_topological_sort.py` — topological sort
- [x] `chapter_04_graph_traversal/005_cycle_detection.py` — cycle detection
- [x] `chapter_04_graph_traversal/006_bipartite_check.py` — bipartite graph check

### Chapter 05: Shortest Paths

- [x] `chapter_05_shortest_paths/001_dijkstra.py` — Dijkstra
- [x] `chapter_05_shortest_paths/002_bellman_ford.py` — Bellman-Ford
- [x] `chapter_05_shortest_paths/003_floyd_warshall.py` — Floyd-Warshall
- [x] `chapter_05_shortest_paths/004_zero_one_bfs.py` — 0-1 BFS
- [x] `chapter_05_shortest_paths/005_dag_shortest_path.py` — shortest path in DAG
- [x] `chapter_05_shortest_paths/006_johnson_algorithm.py` — Johnson's algorithm

### Chapter 06: Minimum Spanning Trees

- [x] `chapter_06_minimum_spanning_trees/001_union_find.py` — union-find
- [x] `chapter_06_minimum_spanning_trees/002_kruskal.py` — Kruskal
- [x] `chapter_06_minimum_spanning_trees/003_prim.py` — Prim
- [x] `chapter_06_minimum_spanning_trees/004_cut_and_cycle_properties.py` — cut and cycle properties
- [x] `chapter_06_minimum_spanning_trees/005_second_best_mst.py` — second-best MST

### Chapter 07: Greedy Algorithms

- [x] `chapter_07_greedy_algorithms/001_interval_scheduling.py` — interval scheduling
- [x] `chapter_07_greedy_algorithms/002_activity_selection.py` — activity selection
- [x] `chapter_07_greedy_algorithms/003_huffman_coding.py` — Huffman coding
- [x] `chapter_07_greedy_algorithms/004_fractional_knapsack.py` — fractional knapsack
- [x] `chapter_07_greedy_algorithms/005_exchange_argument_examples.py` — exchange argument examples

### Chapter 08: Dynamic Programming I

- [x] `chapter_08_dynamic_programming_i/001_fibonacci_variants.py` — Fibonacci variants
- [x] `chapter_08_dynamic_programming_i/002_zero_one_knapsack.py` — 0/1 knapsack
- [x] `chapter_08_dynamic_programming_i/003_unbounded_knapsack.py` — unbounded knapsack
- [x] `chapter_08_dynamic_programming_i/004_longest_increasing_subsequence.py` — LIS
- [x] `chapter_08_dynamic_programming_i/005_edit_distance.py` — edit distance
- [x] `chapter_08_dynamic_programming_i/006_coin_change.py` — coin change
- [x] `chapter_08_dynamic_programming_i/007_longest_common_subsequence.py` — LCS

### Chapter 09: Dynamic Programming II

- [x] `chapter_09_dynamic_programming_ii/001_bitmask_dp.py` — bitmask DP
- [x] `chapter_09_dynamic_programming_ii/002_tree_dp.py` — tree DP
- [x] `chapter_09_dynamic_programming_ii/003_digit_dp.py` — digit DP
- [x] `chapter_09_dynamic_programming_ii/004_interval_dp.py` — interval DP
- [x] `chapter_09_dynamic_programming_ii/005_profile_dp.py` — profile DP
- [x] `chapter_09_dynamic_programming_ii/006_convex_hull_trick.py` — convex hull trick
- [x] `chapter_09_dynamic_programming_ii/007_knuth_optimization.py` — Knuth optimization
- [x] `chapter_09_dynamic_programming_ii/008_divide_and_conquer_dp.py` — divide-and-conquer DP optimization

### Chapter 10: Network Flow and Matching

- [ ] `chapter_10_network_flow_and_matching/001_ford_fulkerson.py` — Ford-Fulkerson
- [ ] `chapter_10_network_flow_and_matching/002_edmonds_karp.py` — Edmonds-Karp
- [ ] `chapter_10_network_flow_and_matching/003_dinic.py` — Dinic
- [ ] `chapter_10_network_flow_and_matching/004_min_cut.py` — minimum cut
- [ ] `chapter_10_network_flow_and_matching/005_bipartite_matching.py` — bipartite matching
- [ ] `chapter_10_network_flow_and_matching/006_hopcroft_karp.py` — Hopcroft-Karp
- [ ] `chapter_10_network_flow_and_matching/007_min_cost_max_flow.py` — min-cost max-flow

### Chapter 11: Advanced Graph Algorithms

- [x] `chapter_11_advanced_graph_algorithms/001_tarjan_scc.py` — Tarjan SCC
- [x] `chapter_11_advanced_graph_algorithms/002_kosaraju_scc.py` — Kosaraju SCC
- [x] `chapter_11_advanced_graph_algorithms/003_bridges.py` — bridges
- [x] `chapter_11_advanced_graph_algorithms/004_articulation_points.py` — articulation points
- [x] `chapter_11_advanced_graph_algorithms/005_euler_path.py` — Euler path
- [x] `chapter_11_advanced_graph_algorithms/006_lca_binary_lifting.py` — LCA by binary lifting

### Chapter 12: String Algorithms

- [x] `chapter_12_string_algorithms/001_kmp.py` — KMP
- [x] `chapter_12_string_algorithms/002_z_algorithm.py` — Z algorithm
- [x] `chapter_12_string_algorithms/003_rabin_karp.py` — Rabin-Karp
- [x] `chapter_12_string_algorithms/004_trie.py` — trie
- [x] `chapter_12_string_algorithms/005_aho_corasick.py` — Aho-Corasick
- [x] `chapter_12_string_algorithms/006_suffix_array.py` — suffix array
- [x] `chapter_12_string_algorithms/007_lcp_array.py` — LCP array
- [x] `chapter_12_string_algorithms/008_manacher.py` — Manacher

### Chapter 13: Number Theory

- [x] `chapter_13_number_theory/001_gcd_lcm.py` — gcd and lcm
- [x] `chapter_13_number_theory/002_extended_gcd.py` — extended gcd
- [x] `chapter_13_number_theory/003_modular_exponentiation.py` — modular exponentiation
- [x] `chapter_13_number_theory/004_modular_inverse.py` — modular inverse
- [x] `chapter_13_number_theory/005_sieve_of_eratosthenes.py` — sieve of Eratosthenes
- [x] `chapter_13_number_theory/006_prime_factorization.py` — prime factorization
- [x] `chapter_13_number_theory/007_chinese_remainder_theorem.py` — CRT
- [x] `chapter_13_number_theory/008_miller_rabin.py` — Miller-Rabin primality test

### Chapter 14: Computational Geometry

- [x] `chapter_14_computational_geometry/001_orientation.py` — orientation test
- [x] `chapter_14_computational_geometry/002_segment_intersection.py` — segment intersection
- [x] `chapter_14_computational_geometry/003_polygon_area.py` — polygon area
- [x] `chapter_14_computational_geometry/004_convex_hull.py` — convex hull
- [x] `chapter_14_computational_geometry/005_rotating_calipers.py` — rotating calipers
- [x] `chapter_14_computational_geometry/006_sweep_line.py` — sweep line

### Chapter 15: Data Structures

- [x] `chapter_15_data_structures/001_heap.py` — heap
- [x] `chapter_15_data_structures/002_monotonic_stack.py` — monotonic stack
- [x] `chapter_15_data_structures/003_monotonic_queue.py` — monotonic queue
- [x] `chapter_15_data_structures/004_fenwick_tree.py` — Fenwick tree
- [x] `chapter_15_data_structures/005_segment_tree.py` — segment tree
- [x] `chapter_15_data_structures/006_lazy_segment_tree.py` — lazy segment tree
- [x] `chapter_15_data_structures/007_sparse_table.py` — sparse table
- [x] `chapter_15_data_structures/008_disjoint_sparse_table.py` — disjoint sparse table

### Chapter 16: Randomized Algorithms

- [ ] `chapter_16_randomized_algorithms/001_randomized_quicksort.py` — randomized quicksort
- [ ] `chapter_16_randomized_algorithms/002_randomized_select.py` — randomized selection
- [ ] `chapter_16_randomized_algorithms/003_reservoir_sampling.py` — reservoir sampling
- [ ] `chapter_16_randomized_algorithms/004_universal_hashing.py` — universal hashing
- [ ] `chapter_16_randomized_algorithms/005_monte_carlo_primality.py` — Monte Carlo primality check

### Chapter 17: Approximation and Hardness

- [ ] `chapter_17_approximation_and_hardness/001_vertex_cover_approximation.py` — vertex cover approximation
- [ ] `chapter_17_approximation_and_hardness/002_set_cover_greedy.py` — greedy set cover
- [ ] `chapter_17_approximation_and_hardness/003_bin_packing_heuristics.py` — bin packing heuristics
- [ ] `chapter_17_approximation_and_hardness/004_reduction_examples.py` — reduction examples
- [ ] `chapter_17_approximation_and_hardness/005_np_completeness_notes.py` — NP-completeness notes

### Chapter 18: Contest Patterns

- [ ] `chapter_18_contest_patterns/001_coordinate_compression.py` — coordinate compression
- [ ] `chapter_18_contest_patterns/002_offline_queries.py` — offline queries
- [ ] `chapter_18_contest_patterns/003_binary_search_on_answer.py` — binary search on answer
- [ ] `chapter_18_contest_patterns/004_meet_in_the_middle.py` — meet-in-the-middle
- [ ] `chapter_18_contest_patterns/005_sweep_line_events.py` — event sweep
- [ ] `chapter_18_contest_patterns/006_difference_constraints.py` — difference constraints
- [ ] `chapter_18_contest_patterns/007_constructive_patterns.py` — constructive patterns

### Chapter 19: Advanced Contest Data Structures

- [ ] `chapter_19_advanced_contest_data_structures/001_persistent_segment_tree.py` — persistent segment tree
- [ ] `chapter_19_advanced_contest_data_structures/002_implicit_treap.py` — implicit treap
- [ ] `chapter_19_advanced_contest_data_structures/003_li_chao_tree.py` — Li Chao tree
- [ ] `chapter_19_advanced_contest_data_structures/004_order_statistic_tree.py` — order statistic tree pattern
- [ ] `chapter_19_advanced_contest_data_structures/005_rollback_union_find.py` — rollback union-find

### Chapter 20: Advanced Tree Algorithms

- [x] `chapter_20_advanced_tree_algorithms/001_euler_tour.py` — Euler tour
- [x] `chapter_20_advanced_tree_algorithms/002_binary_lifting.py` — binary lifting
- [x] `chapter_20_advanced_tree_algorithms/003_heavy_light_decomposition.py` — heavy-light decomposition
- [x] `chapter_20_advanced_tree_algorithms/004_dsu_on_tree.py` — DSU on tree
- [x] `chapter_20_advanced_tree_algorithms/005_centroid_decomposition.py` — centroid decomposition

### Chapter 21: Offline and Range Query Algorithms

- [x] `chapter_21_offline_and_range_query_algorithms/001_mos_algorithm.py` — Mo's algorithm
- [x] `chapter_21_offline_and_range_query_algorithms/002_mos_algorithm_on_tree.py` — Mo's algorithm on tree
- [x] `chapter_21_offline_and_range_query_algorithms/003_cdq_divide_and_conquer.py` — CDQ divide and conquer
- [x] `chapter_21_offline_and_range_query_algorithms/004_parallel_binary_search.py` — parallel binary search
- [x] `chapter_21_offline_and_range_query_algorithms/005_offline_dynamic_connectivity.py` — offline dynamic connectivity

### Chapter 22: Combinatorics and Polynomial Algorithms

- [ ] `chapter_22_combinatorics_and_polynomial_algorithms/001_factorials_and_combinations.py` — factorials and combinations
- [ ] `chapter_22_combinatorics_and_polynomial_algorithms/002_inclusion_exclusion.py` — inclusion-exclusion
- [ ] `chapter_22_combinatorics_and_polynomial_algorithms/003_catalan_numbers.py` — Catalan numbers
- [ ] `chapter_22_combinatorics_and_polynomial_algorithms/004_generating_functions.py` — generating functions
- [ ] `chapter_22_combinatorics_and_polynomial_algorithms/005_fft.py` — FFT
- [ ] `chapter_22_combinatorics_and_polynomial_algorithms/006_ntt.py` — NTT
- [ ] `chapter_22_combinatorics_and_polynomial_algorithms/007_subset_convolution_basics.py` — subset convolution basics

### Chapter 23: Game Theory and Constructive Methods

- [ ] `chapter_23_game_theory_and_constructive_methods/001_nim.py` — Nim
- [ ] `chapter_23_game_theory_and_constructive_methods/002_sprague_grundy.py` — Sprague-Grundy theorem
- [ ] `chapter_23_game_theory_and_constructive_methods/003_mex.py` — mex
- [ ] `chapter_23_game_theory_and_constructive_methods/004_invariant_construction.py` — invariant construction
- [ ] `chapter_23_game_theory_and_constructive_methods/005_extremal_construction.py` — extremal construction

### Chapter 24: Bioinformatics Algorithms

`chapter_24_bioinformatics/` focuses on classical bioinformatics algorithms and data structures. It intentionally excludes AI-based methods and focuses on algorithmic foundations that can be implemented directly.

- [ ] `chapter_24_bioinformatics/001_naive_dna_matching.py` — naive exact DNA matching
- [ ] `chapter_24_bioinformatics/002_kmp_dna_matching.py` — KMP DNA matching
- [ ] `chapter_24_bioinformatics/003_rabin_karp_kmer_search.py` — Rabin-Karp k-mer search
- [ ] `chapter_24_bioinformatics/004_aho_corasick_motif_matching.py` — multi-pattern motif matching
- [ ] `chapter_24_bioinformatics/005_hamming_distance.py` — Hamming distance
- [ ] `chapter_24_bioinformatics/006_edit_distance.py` — edit distance
- [ ] `chapter_24_bioinformatics/007_needleman_wunsch.py` — global alignment
- [ ] `chapter_24_bioinformatics/008_smith_waterman.py` — local alignment
- [ ] `chapter_24_bioinformatics/009_affine_gap_alignment.py` — affine gap alignment
- [ ] `chapter_24_bioinformatics/010_hirschberg_alignment.py` — linear-space alignment
- [ ] `chapter_24_bioinformatics/011_suffix_array.py` — suffix array
- [ ] `chapter_24_bioinformatics/012_lcp_array.py` — LCP array
- [ ] `chapter_24_bioinformatics/013_burrows_wheeler_transform.py` — Burrows-Wheeler Transform
- [ ] `chapter_24_bioinformatics/014_fm_index.py` — FM-index
- [ ] `chapter_24_bioinformatics/015_fasta_seed_lookup.py` — FASTA-style seed lookup
- [ ] `chapter_24_bioinformatics/016_blast_seed_extend.py` — BLAST-style seed-and-extend
- [ ] `chapter_24_bioinformatics/017_spaced_seeds.py` — spaced seeds
- [ ] `chapter_24_bioinformatics/018_minimizer_index.py` — minimizer index
- [ ] `chapter_24_bioinformatics/019_winnowing.py` — winnowing
- [ ] `chapter_24_bioinformatics/020_syncmers.py` — syncmers
- [ ] `chapter_24_bioinformatics/021_seed_chaining.py` — seed chaining
- [ ] `chapter_24_bioinformatics/022_banded_dynamic_programming.py` — banded DP alignment
- [ ] `chapter_24_bioinformatics/023_minimap2_style_mapping.py` — minimap2-style long-read mapping
- [ ] `chapter_24_bioinformatics/024_progressive_msa.py` — progressive multiple sequence alignment
- [ ] `chapter_24_bioinformatics/025_profile_alignment.py` — profile alignment
- [ ] `chapter_24_bioinformatics/026_partial_order_alignment.py` — partial-order alignment
- [ ] `chapter_24_bioinformatics/027_overlap_layout_consensus.py` — overlap-layout-consensus assembly
- [ ] `chapter_24_bioinformatics/028_de_bruijn_graph_assembly.py` — de Bruijn graph assembly
- [ ] `chapter_24_bioinformatics/029_eulerian_assembly.py` — Eulerian path assembly formulation
- [ ] `chapter_24_bioinformatics/030_string_graph_assembly.py` — string graph assembly
- [ ] `chapter_24_bioinformatics/031_unitig_compaction.py` — unitig compaction
- [ ] `chapter_24_bioinformatics/032_viterbi_hmm_genotyping.py` — Viterbi decoding for HMM genotyping
- [ ] `chapter_24_bioinformatics/033_forward_backward.py` — Forward-Backward algorithm
- [ ] `chapter_24_bioinformatics/034_upgma_tree.py` — UPGMA phylogenetic tree
- [ ] `chapter_24_bioinformatics/035_neighbor_joining.py` — neighbor joining
- [ ] `chapter_24_bioinformatics/036_maximum_parsimony.py` — maximum parsimony
- [ ] `chapter_24_bioinformatics/037_kmer_counting.py` — k-mer counting
- [ ] `chapter_24_bioinformatics/038_bloom_filter_kmers.py` — Bloom filter for k-mers
- [ ] `chapter_24_bioinformatics/039_count_min_sketch_kmers.py` — Count-Min Sketch for k-mers
- [ ] `chapter_24_bioinformatics/040_minhash_sequence_distance.py` — MinHash sequence distance
- [ ] `chapter_24_bioinformatics/041_mash_style_distance.py` — Mash-style sketch distance
- [ ] `chapter_24_bioinformatics/042_variation_graph_basics.py` — variation graph basics
- [ ] `chapter_24_bioinformatics/043_sequence_to_graph_alignment.py` — sequence-to-graph alignment
- [ ] `chapter_24_bioinformatics/044_graph_indexing_basics.py` — graph indexing basics
- [ ] `chapter_24_bioinformatics/045_pangenome_mapping_basics.py` — pangenome mapping basics

Bioinformatics implementations should clearly state whether an algorithm is exact or heuristic. For example, Needleman-Wunsch and Smith-Waterman are dynamic-programming algorithms that compute optimal alignments under a scoring model, while FASTA, BLAST, and minimizer-based mappers use seed-and-extend heuristics to scale to large sequence databases.

### Chapter 25: ML/DL Optimization Algorithms

`chapter_25_ml_dl_optimization/` focuses on optimization algorithms and numerical methods commonly used to train machine-learning and deep-learning models. This chapter covers the algorithmic side of optimization rather than model architecture.

- [ ] `chapter_25_ml_dl_optimization/001_gradient_descent.py` — batch gradient descent
- [ ] `chapter_25_ml_dl_optimization/002_stochastic_gradient_descent.py` — stochastic gradient descent
- [ ] `chapter_25_ml_dl_optimization/003_mini_batch_gradient_descent.py` — mini-batch gradient descent
- [ ] `chapter_25_ml_dl_optimization/004_momentum.py` — momentum
- [ ] `chapter_25_ml_dl_optimization/005_nesterov_accelerated_gradient.py` — Nesterov accelerated gradient
- [ ] `chapter_25_ml_dl_optimization/006_adagrad.py` — AdaGrad
- [ ] `chapter_25_ml_dl_optimization/007_rmsprop.py` — RMSProp
- [ ] `chapter_25_ml_dl_optimization/008_adam.py` — Adam
- [ ] `chapter_25_ml_dl_optimization/009_adamw.py` — AdamW
- [ ] `chapter_25_ml_dl_optimization/010_nadam.py` — Nadam
- [ ] `chapter_25_ml_dl_optimization/011_amsgrad.py` — AMSGrad
- [ ] `chapter_25_ml_dl_optimization/012_learning_rate_decay.py` — learning-rate decay
- [ ] `chapter_25_ml_dl_optimization/013_cosine_annealing.py` — cosine annealing
- [ ] `chapter_25_ml_dl_optimization/014_warmup_schedule.py` — warmup schedule
- [ ] `chapter_25_ml_dl_optimization/015_gradient_clipping.py` — gradient clipping
- [ ] `chapter_25_ml_dl_optimization/016_weight_decay.py` — weight decay
- [ ] `chapter_25_ml_dl_optimization/017_l1_l2_regularization.py` — L1 and L2 regularization
- [ ] `chapter_25_ml_dl_optimization/018_early_stopping.py` — early stopping
- [ ] `chapter_25_ml_dl_optimization/019_batch_normalization_math.py` — batch normalization optimization behavior
- [ ] `chapter_25_ml_dl_optimization/020_layer_normalization_math.py` — layer normalization optimization behavior
- [ ] `chapter_25_ml_dl_optimization/021_newton_method.py` — Newton's method
- [ ] `chapter_25_ml_dl_optimization/022_quasi_newton_bfgs.py` — BFGS
- [ ] `chapter_25_ml_dl_optimization/023_l_bfgs.py` — L-BFGS
- [ ] `chapter_25_ml_dl_optimization/024_conjugate_gradient.py` — conjugate gradient
- [ ] `chapter_25_ml_dl_optimization/025_coordinate_descent.py` — coordinate descent
- [ ] `chapter_25_ml_dl_optimization/026_projected_gradient_descent.py` — projected gradient descent
- [ ] `chapter_25_ml_dl_optimization/027_proximal_gradient_method.py` — proximal gradient method
- [ ] `chapter_25_ml_dl_optimization/028_mirror_descent.py` — mirror descent
- [ ] `chapter_25_ml_dl_optimization/029_dual_averaging.py` — dual averaging
- [ ] `chapter_25_ml_dl_optimization/030_gradient_checking.py` — numerical gradient checking
- [ ] `chapter_25_ml_dl_optimization/031_backtracking_line_search.py` — backtracking line search
- [ ] `chapter_25_ml_dl_optimization/032_hyperparameter_grid_search.py` — grid search
- [ ] `chapter_25_ml_dl_optimization/033_random_search.py` — random search
- [ ] `chapter_25_ml_dl_optimization/034_bayesian_optimization_basics.py` — Bayesian optimization basics

### Chapter 26: Heuristic Search and Metaheuristic Optimization

`chapter_26_heuristic_search_and_metaheuristics/` focuses on general-purpose search and optimization algorithms that are widely used when exact optimization is too expensive.

- [ ] `chapter_26_heuristic_search_and_metaheuristics/001_hill_climbing.py` — hill climbing
- [ ] `chapter_26_heuristic_search_and_metaheuristics/002_random_restart_hill_climbing.py` — random-restart hill climbing
- [ ] `chapter_26_heuristic_search_and_metaheuristics/003_simulated_annealing.py` — simulated annealing
- [ ] `chapter_26_heuristic_search_and_metaheuristics/004_particle_swarm_optimization.py` — particle swarm optimization
- [ ] `chapter_26_heuristic_search_and_metaheuristics/005_genetic_algorithm.py` — genetic algorithm
- [ ] `chapter_26_heuristic_search_and_metaheuristics/006_differential_evolution.py` — differential evolution
- [ ] `chapter_26_heuristic_search_and_metaheuristics/007_ant_colony_optimization.py` — ant colony optimization
- [ ] `chapter_26_heuristic_search_and_metaheuristics/008_tabu_search.py` — tabu search
- [ ] `chapter_26_heuristic_search_and_metaheuristics/009_beam_search.py` — beam search
- [ ] `chapter_26_heuristic_search_and_metaheuristics/010_a_star.py` — A* search
- [ ] `chapter_26_heuristic_search_and_metaheuristics/011_ida_star.py` — IDA* search
- [ ] `chapter_26_heuristic_search_and_metaheuristics/012_monte_carlo_tree_search.py` — Monte Carlo Tree Search
- [ ] `chapter_26_heuristic_search_and_metaheuristics/013_upper_confidence_bound.py` — UCB selection
- [ ] `chapter_26_heuristic_search_and_metaheuristics/014_cross_entropy_method.py` — cross-entropy method
- [ ] `chapter_26_heuristic_search_and_metaheuristics/015_covariance_matrix_adaptation.py` — CMA-ES basics

### Chapter 27: Mathematical and Numerical Algorithms

`chapter_27_mathematical_and_numerical_algorithms/` focuses on calculus, numerical analysis, linear algebra, and scientific-computing algorithms that are useful beyond contest settings.

- [ ] `chapter_27_mathematical_and_numerical_algorithms/001_finite_difference_derivative.py` — finite-difference derivative
- [ ] `chapter_27_mathematical_and_numerical_algorithms/002_gradient_jacobian_hessian.py` — gradient, Jacobian, and Hessian by finite differences
- [ ] `chapter_27_mathematical_and_numerical_algorithms/003_newton_root_finding.py` — Newton root finding
- [ ] `chapter_27_mathematical_and_numerical_algorithms/004_bisection_root_finding.py` — bisection root finding
- [ ] `chapter_27_mathematical_and_numerical_algorithms/005_secant_method.py` — secant method
- [ ] `chapter_27_mathematical_and_numerical_algorithms/006_fixed_point_iteration.py` — fixed-point iteration
- [ ] `chapter_27_mathematical_and_numerical_algorithms/007_trapezoidal_rule.py` — trapezoidal integration
- [ ] `chapter_27_mathematical_and_numerical_algorithms/008_simpson_rule.py` — Simpson integration
- [ ] `chapter_27_mathematical_and_numerical_algorithms/009_adaptive_simpson.py` — adaptive Simpson integration
- [ ] `chapter_27_mathematical_and_numerical_algorithms/010_gaussian_quadrature.py` — Gaussian quadrature basics
- [ ] `chapter_27_mathematical_and_numerical_algorithms/011_monte_carlo_integration.py` — Monte Carlo integration
- [ ] `chapter_27_mathematical_and_numerical_algorithms/012_euler_method_ode.py` — Euler method for ODEs
- [ ] `chapter_27_mathematical_and_numerical_algorithms/013_runge_kutta_4.py` — RK4 ODE solver
- [ ] `chapter_27_mathematical_and_numerical_algorithms/014_gaussian_elimination.py` — Gaussian elimination
- [ ] `chapter_27_mathematical_and_numerical_algorithms/015_lu_decomposition.py` — LU decomposition
- [ ] `chapter_27_mathematical_and_numerical_algorithms/016_qr_decomposition.py` — QR decomposition
- [ ] `chapter_27_mathematical_and_numerical_algorithms/017_power_iteration.py` — power iteration
- [ ] `chapter_27_mathematical_and_numerical_algorithms/018_svd_basics.py` — SVD basics
- [ ] `chapter_27_mathematical_and_numerical_algorithms/019_least_squares.py` — least squares
- [ ] `chapter_27_mathematical_and_numerical_algorithms/020_polynomial_interpolation.py` — polynomial interpolation
- [ ] `chapter_27_mathematical_and_numerical_algorithms/021_lagrange_interpolation.py` — Lagrange interpolation
- [ ] `chapter_27_mathematical_and_numerical_algorithms/022_newton_interpolation.py` — Newton interpolation
- [ ] `chapter_27_mathematical_and_numerical_algorithms/023_spline_interpolation.py` — spline interpolation basics
- [ ] `chapter_27_mathematical_and_numerical_algorithms/024_fast_fourier_transform_multiplication.py` — FFT-based multiplication
- [ ] `chapter_27_mathematical_and_numerical_algorithms/025_number_theoretic_transform_multiplication.py` — NTT-based multiplication

### Chapter 28: Deep Learning Architectures

`chapter_28_deep_learning_architectures/` focuses on hand-written educational implementations of neural-network architecture components. Tensor libraries such as `torch` may be used for tensors and automatic differentiation, but the target architecture logic must not be replaced by one-shot high-level modules.

- [ ] `chapter_28_deep_learning_architectures/001_perceptron.py` — perceptron
- [ ] `chapter_28_deep_learning_architectures/002_multilayer_perceptron.py` — multilayer perceptron
- [ ] `chapter_28_deep_learning_architectures/003_autoencoder.py` — autoencoder
- [ ] `chapter_28_deep_learning_architectures/004_variational_autoencoder_core.py` — VAE core
- [ ] `chapter_28_deep_learning_architectures/005_manual_2d_convolution.py` — manual 2D convolution
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
- [ ] `chapter_28_deep_learning_architectures/018_seq2seq_encoder_decoder.py` — seq2seq encoder-decoder
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
- [ ] `chapter_28_deep_learning_architectures/031_graph_convolution_layer.py` — graph convolution layer
- [ ] `chapter_28_deep_learning_architectures/032_graph_attention_layer.py` — graph attention layer

### Chapter 29: Reinforcement Learning Algorithms

`chapter_29_reinforcement_learning_algorithms/` focuses on classical reinforcement-learning algorithms and planning methods. Implementations should expose the update equations directly rather than delegating to RL libraries.

- [ ] `chapter_29_reinforcement_learning_algorithms/001_markov_decision_process.py` — MDP basics
- [ ] `chapter_29_reinforcement_learning_algorithms/002_value_iteration.py` — value iteration
- [ ] `chapter_29_reinforcement_learning_algorithms/003_policy_iteration.py` — policy iteration
- [ ] `chapter_29_reinforcement_learning_algorithms/004_monte_carlo_prediction.py` — Monte Carlo prediction
- [ ] `chapter_29_reinforcement_learning_algorithms/005_monte_carlo_control.py` — Monte Carlo control
- [ ] `chapter_29_reinforcement_learning_algorithms/006_temporal_difference_prediction.py` — TD(0)
- [ ] `chapter_29_reinforcement_learning_algorithms/007_sarsa.py` — SARSA
- [ ] `chapter_29_reinforcement_learning_algorithms/008_q_learning.py` — Q-learning
- [ ] `chapter_29_reinforcement_learning_algorithms/009_expected_sarsa.py` — Expected SARSA
- [ ] `chapter_29_reinforcement_learning_algorithms/010_double_q_learning.py` — Double Q-learning
- [ ] `chapter_29_reinforcement_learning_algorithms/011_dyna_q.py` — Dyna-Q
- [ ] `chapter_29_reinforcement_learning_algorithms/012_policy_gradient_reinforce.py` — REINFORCE
- [ ] `chapter_29_reinforcement_learning_algorithms/013_actor_critic_basics.py` — actor-critic basics
- [ ] `chapter_29_reinforcement_learning_algorithms/014_upper_confidence_bound_bandit.py` — UCB bandit
- [ ] `chapter_29_reinforcement_learning_algorithms/015_thompson_sampling.py` — Thompson sampling

### Chapter 30: Compression and Information Coding Algorithms

`chapter_30_compression_and_information_coding/` focuses on lossless compression, entropy coding, error detection, and error-correcting codes.

- [x] `chapter_30_compression_and_information_coding/001_run_length_encoding.py` — run-length encoding
- [x] `chapter_30_compression_and_information_coding/002_huffman_coding.py` — Huffman coding
- [x] `chapter_30_compression_and_information_coding/003_canonical_huffman.py` — canonical Huffman coding
- [x] `chapter_30_compression_and_information_coding/004_arithmetic_coding.py` — arithmetic coding
- [x] `chapter_30_compression_and_information_coding/005_lz77.py` — LZ77
- [x] `chapter_30_compression_and_information_coding/006_lz78.py` — LZ78
- [x] `chapter_30_compression_and_information_coding/007_lzw.py` — LZW
- [x] `chapter_30_compression_and_information_coding/008_bwt_compression_pipeline.py` — BWT compression pipeline
- [x] `chapter_30_compression_and_information_coding/009_move_to_front.py` — move-to-front transform
- [x] `chapter_30_compression_and_information_coding/010_delta_encoding.py` — delta encoding
- [x] `chapter_30_compression_and_information_coding/011_varint_encoding.py` — variable-length integer encoding
- [x] `chapter_30_compression_and_information_coding/012_crc32.py` — CRC32
- [x] `chapter_30_compression_and_information_coding/013_hamming_code.py` — Hamming code
- [x] `chapter_30_compression_and_information_coding/014_reed_solomon_basics.py` — Reed-Solomon basics

### Chapter 31: Cryptography Algorithms

`chapter_31_cryptography_algorithms/` focuses on educational implementations of cryptographic primitives and protocols. These files are for learning and must not be used as production security code.

- [x] `chapter_31_cryptography_algorithms/001_caesar_cipher.py` — Caesar cipher
- [x] `chapter_31_cryptography_algorithms/002_vigenere_cipher.py` — Vigenere cipher
- [x] `chapter_31_cryptography_algorithms/003_diffie_hellman.py` — Diffie-Hellman key exchange
- [x] `chapter_31_cryptography_algorithms/004_rsa_key_generation.py` — RSA key generation
- [x] `chapter_31_cryptography_algorithms/005_rsa_encrypt_decrypt.py` — RSA encryption and decryption
- [x] `chapter_31_cryptography_algorithms/006_elgamal.py` — ElGamal
- [x] `chapter_31_cryptography_algorithms/007_sha256_core.py` — SHA-256 core structure
- [x] `chapter_31_cryptography_algorithms/008_hmac.py` — HMAC
- [x] `chapter_31_cryptography_algorithms/009_merkle_tree.py` — Merkle tree
- [ ] `chapter_31_cryptography_algorithms/010_aes_sbox_and_rounds.py` — AES S-box and round structure
- [ ] `chapter_31_cryptography_algorithms/011_elliptic_curve_group.py` — elliptic-curve group operations
- [ ] `chapter_31_cryptography_algorithms/012_ecdsa_basics.py` — ECDSA basics

### Chapter 32: Compiler Algorithms

`chapter_32_compiler_algorithms/` focuses on parsing, program analysis, optimization, and register allocation algorithms.

- [ ] `chapter_32_compiler_algorithms/001_regex_to_nfa.py` — regex to NFA
- [ ] `chapter_32_compiler_algorithms/002_nfa_to_dfa.py` — NFA to DFA
- [ ] `chapter_32_compiler_algorithms/003_dfa_minimization.py` — DFA minimization
- [ ] `chapter_32_compiler_algorithms/004_first_follow_sets.py` — FIRST and FOLLOW sets
- [ ] `chapter_32_compiler_algorithms/005_ll1_parsing_table.py` — LL(1) parsing table
- [ ] `chapter_32_compiler_algorithms/006_lr0_items.py` — LR(0) items
- [ ] `chapter_32_compiler_algorithms/007_slr_parsing.py` — SLR parsing
- [ ] `chapter_32_compiler_algorithms/008_shunting_yard.py` — shunting-yard algorithm
- [ ] `chapter_32_compiler_algorithms/009_three_address_code.py` — three-address code
- [ ] `chapter_32_compiler_algorithms/010_basic_blocks_cfg.py` — basic blocks and CFG
- [ ] `chapter_32_compiler_algorithms/011_dominators.py` — dominator computation
- [ ] `chapter_32_compiler_algorithms/012_static_single_assignment.py` — SSA construction basics
- [ ] `chapter_32_compiler_algorithms/013_liveness_analysis.py` — liveness analysis
- [ ] `chapter_32_compiler_algorithms/014_graph_coloring_register_allocation.py` — graph-coloring register allocation

### Chapter 33: Database Algorithms

`chapter_33_database_algorithms/` focuses on storage indexes, query execution, query optimization, and transaction-control algorithms.

- [ ] `chapter_33_database_algorithms/001_b_tree.py` — B-tree
- [ ] `chapter_33_database_algorithms/002_b_plus_tree.py` — B+ tree
- [ ] `chapter_33_database_algorithms/003_lsm_tree_basics.py` — LSM tree basics
- [ ] `chapter_33_database_algorithms/004_hash_index.py` — hash index
- [ ] `chapter_33_database_algorithms/005_bitmap_index.py` — bitmap index
- [ ] `chapter_33_database_algorithms/006_nested_loop_join.py` — nested-loop join
- [ ] `chapter_33_database_algorithms/007_hash_join.py` — hash join
- [ ] `chapter_33_database_algorithms/008_sort_merge_join.py` — sort-merge join
- [ ] `chapter_33_database_algorithms/009_external_merge_sort.py` — external merge sort
- [ ] `chapter_33_database_algorithms/010_grace_hash_join.py` — Grace hash join
- [ ] `chapter_33_database_algorithms/011_volcano_iterator_model.py` — Volcano iterator model
- [ ] `chapter_33_database_algorithms/012_dynamic_programming_join_order.py` — DP join ordering
- [ ] `chapter_33_database_algorithms/013_two_phase_locking.py` — two-phase locking
- [ ] `chapter_33_database_algorithms/014_mvcc_basics.py` — MVCC basics

### Chapter 34: Distributed Systems Algorithms

`chapter_34_distributed_systems_algorithms/` focuses on algorithms used for coordination, consistency, replication, partitioning, and distributed state.

- [ ] `chapter_34_distributed_systems_algorithms/001_consistent_hashing.py` — consistent hashing
- [ ] `chapter_34_distributed_systems_algorithms/002_rendezvous_hashing.py` — rendezvous hashing
- [ ] `chapter_34_distributed_systems_algorithms/003_vector_clock.py` — vector clock
- [ ] `chapter_34_distributed_systems_algorithms/004_lamport_clock.py` — Lamport clock
- [ ] `chapter_34_distributed_systems_algorithms/005_gossip_protocol.py` — gossip protocol
- [ ] `chapter_34_distributed_systems_algorithms/006_leader_election_bully.py` — Bully leader election
- [ ] `chapter_34_distributed_systems_algorithms/007_leader_election_ring.py` — ring leader election
- [ ] `chapter_34_distributed_systems_algorithms/008_two_phase_commit.py` — two-phase commit
- [ ] `chapter_34_distributed_systems_algorithms/009_three_phase_commit.py` — three-phase commit
- [ ] `chapter_34_distributed_systems_algorithms/010_paxos_basics.py` — Paxos basics
- [ ] `chapter_34_distributed_systems_algorithms/011_raft_basics.py` — Raft basics
- [ ] `chapter_34_distributed_systems_algorithms/012_crdt_g_counter.py` — CRDT G-Counter
- [ ] `chapter_34_distributed_systems_algorithms/013_merkle_tree_sync.py` — Merkle-tree synchronization

### Chapter 35: Operating System Scheduling Algorithms

`chapter_35_operating_system_scheduling/` focuses on CPU, memory, disk, and page-replacement scheduling algorithms.

- [ ] `chapter_35_operating_system_scheduling/001_first_come_first_served.py` — FCFS scheduling
- [ ] `chapter_35_operating_system_scheduling/002_shortest_job_first.py` — SJF scheduling
- [ ] `chapter_35_operating_system_scheduling/003_shortest_remaining_time_first.py` — SRTF scheduling
- [ ] `chapter_35_operating_system_scheduling/004_round_robin.py` — round-robin scheduling
- [ ] `chapter_35_operating_system_scheduling/005_priority_scheduling.py` — priority scheduling
- [ ] `chapter_35_operating_system_scheduling/006_multilevel_feedback_queue.py` — MLFQ
- [ ] `chapter_35_operating_system_scheduling/007_rate_monotonic_scheduling.py` — rate-monotonic scheduling
- [ ] `chapter_35_operating_system_scheduling/008_earliest_deadline_first.py` — earliest-deadline-first scheduling
- [ ] `chapter_35_operating_system_scheduling/009_fifo_page_replacement.py` — FIFO page replacement
- [ ] `chapter_35_operating_system_scheduling/010_lru_page_replacement.py` — LRU page replacement
- [ ] `chapter_35_operating_system_scheduling/011_clock_page_replacement.py` — clock page replacement
- [ ] `chapter_35_operating_system_scheduling/012_scan_disk_scheduling.py` — SCAN disk scheduling
- [ ] `chapter_35_operating_system_scheduling/013_c_scan_disk_scheduling.py` — C-SCAN disk scheduling

### Chapter 36: Graph Machine Learning Sampling Algorithms

`chapter_36_graph_machine_learning_sampling/` focuses on graph sampling and random-walk algorithms commonly used before or inside graph ML pipelines.

- [ ] `chapter_36_graph_machine_learning_sampling/001_random_walk.py` — random walk
- [ ] `chapter_36_graph_machine_learning_sampling/002_personalized_pagerank.py` — personalized PageRank
- [ ] `chapter_36_graph_machine_learning_sampling/003_deepwalk_sampling.py` — DeepWalk-style sampling
- [ ] `chapter_36_graph_machine_learning_sampling/004_node2vec_sampling.py` — Node2Vec biased random walks
- [ ] `chapter_36_graph_machine_learning_sampling/005_negative_sampling.py` — negative sampling
- [ ] `chapter_36_graph_machine_learning_sampling/006_graphsage_neighbor_sampling.py` — GraphSAGE neighbor sampling
- [ ] `chapter_36_graph_machine_learning_sampling/007_ladies_sampling_basics.py` — LADIES sampling basics
- [ ] `chapter_36_graph_machine_learning_sampling/008_random_edge_sampling.py` — random edge sampling
- [ ] `chapter_36_graph_machine_learning_sampling/009_subgraph_sampling.py` — subgraph sampling

## Implementation Standard

Each Python implementation should follow a consistent structure:

- Core algorithm logic must be implemented by hand.
- Do not use one-shot library calls that solve the target algorithm directly.
- Standard libraries may be used for basic containers, typing, math helpers, and test scaffolding.
- `numpy` may be used for array storage and basic vectorized arithmetic, but not to replace the target algorithm.
- `torch` may be used for tensors, autograd experiments, and low-level neural-network building blocks, but not for one-shot replacements such as using `torch.optim.Adam` to implement Adam, `sklearn.svm.SVC` to implement SVM, or `torch.nn.MultiheadAttention` to implement multi-head attention.
- If the file is about implementing a heap, binary search, FFT, SVM, ResNet block, BLAST-style seed extension, or any other named algorithm, the named core must be visible in the source code.
- Every source file must start with a Chinese intent comment explaining what the file implements, why the algorithm matters, expected inputs, outputs, and complexity.
- Every public function must include a clear Chinese docstring explaining parameters, return values, edge cases, and the core idea.
- Long or non-obvious code paths must include Chinese comments at key decision points.
- Important invariants, proof ideas, and tricky boundary conditions must be documented near the relevant code.
- Implementations should follow SOLID and DRY principles where they apply: keep functions focused, avoid duplicated logic, and separate reusable helpers from examples.
- Changes should be made through patch-style edits instead of rewriting whole files unnecessarily.
- Each algorithm file should include several runnable examples in `main()`.
- Each completed implementation should be marked as `- [x]` in the task list.

```python
"""
文件意图：
    本文件实现二分查找，用于在有序数组中查找目标值的位置。

适用场景：
    输入数组必须已经按非递减顺序排列。

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

    关键点：
        每次比较中间位置，将搜索区间缩小一半。
    """
    left, right = 0, len(nums) - 1

    # 循环不变量：如果 target 存在，它一定在闭区间 [left, right] 中。
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

## Running Examples

Run a single algorithm file:

```bash
python3 chapter_01_foundations/001_binary_search.py
```

Run the repository-level test driver:

```bash
python3 main.py
```

When the repository grows, `main.py` can be used as a lightweight smoke-test runner that imports selected examples from each chapter.

## Testing Expectations

Every algorithm should include multiple cases, not just the happy path.

Suggested coverage:

- empty input;
- single-element input;
- duplicate values;
- already sorted and reverse sorted input;
- disconnected graphs where applicable;
- negative weights where applicable;
- boundary values for modular arithmetic and indexing;
- cases that demonstrate why the algorithm is correct.

## Complexity Notes

Each implementation should document:

- input assumptions;
- time complexity;
- space complexity;
- important invariants;
- why the algorithm works;
- when the algorithm should not be used.

For example, Dijkstra's algorithm should explicitly state that the standard version assumes non-negative edge weights, while Bellman-Ford can handle negative edges but not reachable negative cycles.

## Development Roadmap

Initial build order:

- [ ] Create the chapter directory structure.
- [ ] Add foundational algorithms with direct examples.
- [ ] Add graph algorithms and dynamic programming implementations.
- [ ] Add data structures commonly used in contest problems.
- [ ] Add advanced topics such as flow, matching, string algorithms, and computational geometry.
- [ ] Add advanced competitive-programming topics such as HLD, DSU on tree, CDQ, Mo's algorithm, FFT, and NTT.
- [ ] Add classical non-AI bioinformatics algorithms.
- [ ] Add ML/DL optimization algorithms.
- [ ] Add a repository-level `main.py` smoke-test runner.
- [ ] Add optional `pytest` tests once the implementation set becomes large.

## Commit Message Standard

Commit messages should be specific, reviewable, and no longer than 10 lines.

Recommended format:

```text
完善算法任务清单与实现规范

- 扩展 chapter 任务列表，覆盖课程算法、竞赛算法和生信算法
- 明确 Python 文件必须包含中文意图注释、函数注释和关键点注释
- 补充 SOLID、DRY、patch 修改模式和测试要求
```

## Project Principles

- Prefer readable implementations over overly compressed code.
- Keep each algorithm self-contained unless shared utilities clearly reduce duplication.
- Include examples that make edge cases visible.
- Use stable numbered filenames so the repository remains easy to navigate.
- Keep explanations concise but technically precise.

## License

This repository is licensed under the [MIT License](LICENSE).
