# Intervyn MCQ Question Bank

The bank contains **1,500 questions** in **32 JSON files** across six modules. `question_bank_catalog.json` defines the current module names, paths, numbering, question counts, difficulty quotas, and original-source ranges.

## Folder organization

```text
questions/
├── module_1_core_cs/
│   ├── 1.1_operating_systems/
│   │   ├── 1.1.1_cpu_scheduling.json
│   │   ├── 1.1.2_concurrency_deadlocks.json
│   │   ├── 1.1.3_memory_management.json
│   │   └── 1.1.4_storage_disk.json
│   ├── 1.2_database_management_systems/
│   │   ├── 1.2.1_schema_normalization.json
│   │   ├── 1.2.2_transactions_concurrency.json
│   │   ├── 1.2.3_storage_indexing.json
│   │   └── 1.2.4_sql_queries.json
│   ├── 1.3_computer_networks/
│   │   ├── 1.3.1_network_architecture.json
│   │   ├── 1.3.2_network_layer_routing.json
│   │   ├── 1.3.3_transport_layer.json
│   │   └── 1.3.4_application_security.json
│   └── 1.4_object_oriented_programming/
│       ├── 1.4.1_oop_architecture.json
│       ├── 1.4.2_object_lifecycle.json
│       ├── 1.4.3_runtime_polymorphism.json
│       └── 1.4.4_tricky_outputs_exceptions.json
├── module_2_dsa/
│   ├── 2.1_algorithm_analysis.json
│   ├── 2.2_linear_data_structures.json
│   ├── 2.3_non_linear_data_structures_hashing.json
│   └── 2.4_searching_sorting_algorithm_design.json
├── module_3_pseudocode/
│   ├── 3.1_bitwise_operations.json
│   └── 3.2_code_tracing_execution.json
├── module_4_applied_systems/
│   ├── 4.1_cloud_computing.json
│   ├── 4.2_software_engineering_git.json
│   ├── 4.3_linux_shell.json
│   └── 4.4_web_technologies_apis.json
├── module_5_data_science/
│   ├── 5.1_statistics_probability.json
│   ├── 5.2_machine_learning.json
│   └── 5.3_python_data_analysis.json
└── module_6_aptitude/
    ├── 6.1_quantitative_aptitude.json
    ├── 6.2_logical_reasoning.json
    └── 6.3_verbal_ability.json
```

Module 1 retains its topic files and IDs inside these four parent folders:

| Part | Name | Questions |
| --- | --- | ---: |
| 1.1 | Operating Systems (OS) | 110 |
| 1.2 | Database Management Systems (DBMS) | 120 |
| 1.3 | Computer Networks (CN) | 100 |
| 1.4 | Object-Oriented Programming (OOP) | 120 |

## Current question files

For Modules 2–6, each requested merge is one JSON array. Resulting groups are numbered consecutively within their module. Every file uses sequential IDs from `<subpart>-001` through its final question; for example, merged Linear Data Structures contains `2.2-001` through `2.2-085`.

| ID | Topic | Questions | Easy | Medium | Hard | File |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| 1.1.1 | CPU Scheduling & Process Lifecycle | 30 | 9 | 15 | 6 | `questions/module_1_core_cs/1.1_operating_systems/1.1.1_cpu_scheduling.json` |
| 1.1.2 | Concurrency, Synchronization & Deadlocks | 30 | 9 | 15 | 6 | `questions/module_1_core_cs/1.1_operating_systems/1.1.2_concurrency_deadlocks.json` |
| 1.1.3 | Memory Management & Virtual Memory | 30 | 9 | 15 | 6 | `questions/module_1_core_cs/1.1_operating_systems/1.1.3_memory_management.json` |
| 1.1.4 | Storage Systems, File Systems & Disk Scheduling | 20 | 6 | 10 | 4 | `questions/module_1_core_cs/1.1_operating_systems/1.1.4_storage_disk.json` |
| 1.2.1 | Relational Schema Design & Normalization | 30 | 9 | 15 | 6 | `questions/module_1_core_cs/1.2_database_management_systems/1.2.1_schema_normalization.json` |
| 1.2.2 | Transactions, Concurrency & Recovery | 30 | 9 | 15 | 6 | `questions/module_1_core_cs/1.2_database_management_systems/1.2.2_transactions_concurrency.json` |
| 1.2.3 | Storage, Indexing & ER Modeling | 25 | 8 | 12 | 5 | `questions/module_1_core_cs/1.2_database_management_systems/1.2.3_storage_indexing.json` |
| 1.2.4 | SQL Queries & Output Prediction | 35 | 10 | 18 | 7 | `questions/module_1_core_cs/1.2_database_management_systems/1.2.4_sql_queries.json` |
| 1.3.1 | Network Architecture & Physical/Data Link Layers | 25 | 8 | 12 | 5 | `questions/module_1_core_cs/1.3_computer_networks/1.3.1_network_architecture.json` |
| 1.3.2 | Network Layer, IP Addressing & Routing | 25 | 7 | 13 | 5 | `questions/module_1_core_cs/1.3_computer_networks/1.3.2_network_layer_routing.json` |
| 1.3.3 | Transport Layer Protocols | 25 | 8 | 12 | 5 | `questions/module_1_core_cs/1.3_computer_networks/1.3.3_transport_layer.json` |
| 1.3.4 | Application Layer Protocols & Network Security | 25 | 7 | 13 | 5 | `questions/module_1_core_cs/1.3_computer_networks/1.3.4_application_security.json` |
| 1.4.1 | Core Architecture & Class Mechanics | 30 | 9 | 15 | 6 | `questions/module_1_core_cs/1.4_object_oriented_programming/1.4.1_oop_architecture.json` |
| 1.4.2 | Object Lifecycle & Memory Management | 30 | 9 | 15 | 6 | `questions/module_1_core_cs/1.4_object_oriented_programming/1.4.2_object_lifecycle.json` |
| 1.4.3 | Runtime Polymorphism & Dynamic Dispatch | 30 | 9 | 15 | 6 | `questions/module_1_core_cs/1.4_object_oriented_programming/1.4.3_runtime_polymorphism.json` |
| 1.4.4 | Language-Specific OOP Outputs & Exception Handling | 30 | 9 | 15 | 6 | `questions/module_1_core_cs/1.4_object_oriented_programming/1.4.4_tricky_outputs_exceptions.json` |
| 2.1 | Algorithm Analysis | 35 | 11 | 17 | 7 | `questions/module_2_dsa/2.1_algorithm_analysis.json` |
| 2.2 | Linear Data Structures | 85 | 25 | 43 | 17 | `questions/module_2_dsa/2.2_linear_data_structures.json` |
| 2.3 | Non-linear Data Structures & Hashing | 150 | 45 | 75 | 30 | `questions/module_2_dsa/2.3_non_linear_data_structures_hashing.json` |
| 2.4 | Searching, Sorting & Algorithm Design | 40 | 12 | 20 | 8 | `questions/module_2_dsa/2.4_searching_sorting_algorithm_design.json` |
| 3.1 | Bitwise Operations | 50 | 15 | 25 | 10 | `questions/module_3_pseudocode/3.1_bitwise_operations.json` |
| 3.2 | Code Tracing & Execution | 100 | 30 | 50 | 20 | `questions/module_3_pseudocode/3.2_code_tracing_execution.json` |
| 4.1 | Cloud Computing | 30 | 9 | 15 | 6 | `questions/module_4_applied_systems/4.1_cloud_computing.json` |
| 4.2 | Software Engineering & Git | 30 | 9 | 15 | 6 | `questions/module_4_applied_systems/4.2_software_engineering_git.json` |
| 4.3 | Linux & Shell | 25 | 8 | 12 | 5 | `questions/module_4_applied_systems/4.3_linux_shell.json` |
| 4.4 | Web Technologies & APIs | 25 | 7 | 13 | 5 | `questions/module_4_applied_systems/4.4_web_technologies_apis.json` |
| 5.1 | Statistics & Probability | 85 | 26 | 42 | 17 | `questions/module_5_data_science/5.1_statistics_probability.json` |
| 5.2 | Machine Learning | 70 | 21 | 35 | 14 | `questions/module_5_data_science/5.2_machine_learning.json` |
| 5.3 | Python Data Analysis | 25 | 7 | 13 | 5 | `questions/module_5_data_science/5.3_python_data_analysis.json` |
| 6.1 | Quantitative Aptitude | 140 | 42 | 70 | 28 | `questions/module_6_aptitude/6.1_quantitative_aptitude.json` |
| 6.2 | Logical Reasoning | 90 | 27 | 45 | 18 | `questions/module_6_aptitude/6.2_logical_reasoning.json` |
| 6.3 | Verbal Ability | 70 | 21 | 35 | 14 | `questions/module_6_aptitude/6.3_verbal_ability.json` |

| Module | Name | Questions |
| --- | --- | ---: |
| 1 | Core Computer Science Fundamentals | 450 |
| 2 | Data Structures & Algorithms | 310 |
| 3 | Pseudocode & Code Tracing | 150 |
| 4 | Applied Systems & Software Engineering | 110 |
| 5 | Data Science & Analytics | 180 |
| 6 | Aptitude & Reasoning | 300 |

Difficulty labels are preserved. Merged quotas are the sums of the original quotas; integer rounding is visible in the table. All six modules retain their overall 30% Easy / 50% Medium / 20% Hard distribution.

## Numbering migration

The numbers in the first column below refer to the **original generation prompts**, not the current folders. Source arrays were concatenated in the listed order. Module 1 topic IDs remain unchanged; only their parent folders changed. No question assessment content was edited.

| Original prompt subpart | Current group | Current question range |
| --- | --- | --- |
| 2.1 | 2.1 — Algorithm Analysis | `2.1-001`–`2.1-035` |
| 2.2 | 2.2 — Linear Data Structures | `2.2-001`–`2.2-045` |
| 2.3 | 2.2 — Linear Data Structures | `2.2-046`–`2.2-085` |
| 2.4 | 2.3 — Non-linear Data Structures & Hashing | `2.3-001`–`2.3-060` |
| 2.5 | 2.3 — Non-linear Data Structures & Hashing | `2.3-061`–`2.3-105` |
| 2.6 | 2.3 — Non-linear Data Structures & Hashing | `2.3-106`–`2.3-150` |
| 2.7 | 2.4 — Searching, Sorting & Algorithm Design | `2.4-001`–`2.4-040` |
| 3.1 | 3.1 — Bitwise Operations | `3.1-001`–`3.1-050` |
| 3.2 | 3.2 — Code Tracing & Execution | `3.2-001`–`3.2-050` |
| 3.3 | 3.2 — Code Tracing & Execution | `3.2-051`–`3.2-100` |
| 4.1 | 4.1 — Cloud Computing | `4.1-001`–`4.1-030` |
| 4.2 | 4.2 — Software Engineering & Git | `4.2-001`–`4.2-030` |
| 4.3 | 4.3 — Linux & Shell | `4.3-001`–`4.3-025` |
| 4.4 | 4.4 — Web Technologies & APIs | `4.4-001`–`4.4-025` |
| 5.1 | 5.1 — Statistics & Probability | `5.1-001`–`5.1-045` |
| 5.2 | 5.1 — Statistics & Probability | `5.1-046`–`5.1-085` |
| 5.3 | 5.2 — Machine Learning | `5.2-001`–`5.2-040` |
| 5.4 | 5.2 — Machine Learning | `5.2-041`–`5.2-070` |
| 5.5 | 5.3 — Python Data Analysis | `5.3-001`–`5.3-025` |
| 6.1 | 6.1 — Quantitative Aptitude | `6.1-001`–`6.1-080` |
| 6.2 | 6.1 — Quantitative Aptitude | `6.1-081`–`6.1-140` |
| 6.3 | 6.2 — Logical Reasoning | `6.2-001`–`6.2-090` |
| 6.4 | 6.3 — Verbal Ability | `6.3-001`–`6.3-070` |

The catalog retains original filenames and source ranges for traceability. The numerical verifiers resolve their original fixture references through `scripts/question_bank.py`; questions on disk contain only current IDs and metadata. The paragraph-order constraint keys also use current question IDs.

## Question format

Each file is a UTF-8 JSON array of objects with exactly these fields:

| Field | Format |
| --- | --- |
| `id` | Unique string: subpart ID plus a three-digit sequence, e.g. `1.1.1-001` |
| `module` | Module title, e.g. `Module 1: Core Computer Science Fundamentals` |
| `subpart_id` | Numeric dotted ID matching the filename prefix, e.g. `1.1.1` |
| `subpart_name` | Full subpart title |
| `difficulty` | `Easy`, `Medium`, or `Hard` |
| `question` | Self-contained question with relevant execution and resource assumptions |
| `code_snippet` | String containing code, an operation trace, or a process/resource table, or `null` when unnecessary |
| `options` | Object containing exactly four distinct strings keyed `A`, `B`, `C`, `D` |
| `correct_answer` | One option key: `A`, `B`, `C`, or `D` |
| `explanation` | Reasoning, including a timeline or calculation where applicable |

## Validation

Structural validation requires Python 3.9+ and only the standard library. Run:

```sh
python scripts/validate_questions.py
```

The validator checks strict JSON syntax, the ten required fields, canonical paths, current module/subpart names, consecutive question IDs, duplicate IDs/questions, four distinct option texts, answer keys, total quotas, and the quotas of each original source range. It also rejects missing catalog files, unregistered files, numbering gaps, and misplaced Module 1 topics. You can validate a module, parent group, or single file:

```sh
python scripts/validate_questions.py questions/module_1_core_cs/1.1_operating_systems
python scripts/validate_questions.py questions/module_2_dsa/2.3_non_linear_data_structures_hashing.json
```

To audit this reorganization against its recorded original Git commit:

```sh
python scripts/verify_question_migration.py
```

This migration-specific audit compares the question, code, difficulty, options, correct answer, and explanation for every original question with its current source range. It also checks that the current file set matches the catalog.

Domain checks use the current folders automatically:

| Check | Command | Requirements / coverage |
| --- | --- | --- |
| OOP | `python scripts/verify_oop_examples.py --cxx PATH_TO_GXX --java-home PATH_TO_JDK` | C++17 compiler and JDK supporting Java 17; discovers the four files inside `1.4_object_oriented_programming` |
| DSA | `python scripts/verify_dsa_examples.py --cxx PATH_TO_GXX` | Executes explicit Python/C++ output examples; syntax-checks Python analysis examples |
| Pseudocode | `python scripts/verify_pseudocode_examples.py --java-home PATH_TO_JDK` | Translates and executes all 150 typed pseudocode programs using Java 17 conventions |
| Git | `python scripts/verify_git_examples.py` | Checks 19 answer keys in disposable repositories without remotes or global configuration changes |
| Linux | `python scripts/verify_shell_examples.py --bash PATH_TO_BASH` | GNU Bash/utilities; 12 exact outputs and four permission-bit checks |
| Data science | `python scripts/verify_data_science_examples.py` | 137 numerical/model/output checks, including all 25 pandas/NumPy programs |
| Aptitude | `python scripts/verify_aptitude_examples.py` | 229 exact/model checks, including the 14 authored paragraph-order constraint sets |

Install the recorded data-science environment on Python 3.10+ with `python -m pip install -r scripts/requirements_data_science.txt`. Its output programs specify pandas 2.3.x and NumPy 2.2.x and were checked with pandas 2.3.0 / NumPy 2.2.6. The numerical verifiers accept repeatable `--subpart` arguments using **current group numbers**:

```sh
python scripts/verify_data_science_examples.py --subpart 5.2
python scripts/verify_aptitude_examples.py --subpart 6.1
```

These examples select Machine Learning and Quantitative Aptitude respectively, including every original source merged into each group. Structural and numerical checks complement editorial review; they do not establish all conceptual, grammar, passage, or difficulty judgments.

## Assessment conventions

- Core CS questions state scheduling tie-breaks, concurrency atomicity, resource models, memory/address units, recovery policies, indexing capacities, and protocol assumptions where they affect the answer. SQL output questions use self-contained SQLite CTEs with explicit result ordering. OOP examples specify C++17 or Java 17; undefined-behavior cases are classified rather than executed as predictable outputs. Fictional ABI exercises state their own layouts.
- DSA questions request tight bounds when needed, state recurrence domains/base cases, and distinguish live space from cumulative allocation. Traversal, rotation, collision, graph, and sorting traces supply their ordering conventions.
- Pseudocode uses typed `Integer`, `Function Integer` / `Function Void`, braces, and `Main`. Signed 32-bit arithmetic wraps; `>>` is arithmetic, `^` is XOR, `div` truncates toward zero, and expression operands evaluate left to right subject to precedence. `Print` appends space-separated integer tokens. Static locals and globals retain state across calls.
- Applied-systems scenarios define failure domains, capacity assumptions, Git tree/index/worktree states, ordinary Linux permission rules, and HTTP/CORS conditions. Shell traces use GNU utilities under `LC_ALL=C`; Windows/MSYS text-output checks do not establish Linux ACL behavior. HTTP questions distinguish safety, idempotency, and CORS response exposure.
- Data-science questions state variance denominators, quartile definitions, conditioning/reporting protocols, moment conventions, test assumptions, and table precision. Model questions specify objective normalization, intercept treatment, impurity definitions, and AUC tie credit. Preprocessing stays inside training folds. Python outputs use explicit lists/scalars and avoid chained-assignment/view-mutation assumptions.
- Aptitude questions use exact fractions or terminating decimals unless approximation is requested. Work/rate, compounding, circular orientation, family, and data-sufficiency conventions are explicit. Universal categorical statements alone do not assert existence; a definite "no" can be sufficient for a yes/no question. The 15 family questions are reviewed by tracing their relations. Verbal Ability retains 22 sentence-correction, 14 error-spotting, 14 paragraph-ordering, and 20 comprehension questions across eight original passages; paragraph constraints record editorial dependencies rather than automatically proving English semantics.

## Reference material

The references used during content review are retained below. They support content conventions; the catalog and numbering are repository-specific.

- [proofreading guidance](https://owl.purdue.edu/owl/general_writing/the_writing_process/proofreading/proofreading_for_errors.html)
- [pronoun case](https://owl.purdue.edu/owl/general_writing/grammar/pronouns/pronoun_case.html)
- [relative-clause guidance](https://owl.purdue.edu/owl/general_writing/grammar/relative_pronouns/index.html)
- [pandas indexing](https://pandas.pydata.org/pandas-docs/version/2.3/user_guide/indexing.html)
- [groupby](https://pandas.pydata.org/pandas-docs/version/2.3/user_guide/groupby.html)
- [merge](https://pandas.pydata.org/pandas-docs/version/2.3/reference/api/pandas.merge.html)
- [NumPy broadcasting](https://numpy.org/doc/2.2/user/basics.broadcasting.html)
- [scikit-learn metrics guide](https://scikit-learn.org/stable/modules/model_evaluation.html)
- [linear-model objectives](https://scikit-learn.org/stable/modules/linear_model.html)
- [ETH lasso lecture notes](https://stat.ethz.ch/Teaching/buhlmann/advanced-comput-statist/slides1.pdf)
- [Statsmodels VIF documentation](https://www.statsmodels.org/v0.13.5/generated/statsmodels.stats.outliers_influence.variance_inflation_factor.html)
- [random-forest documentation](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html)
- [XGBoost objective tutorial](https://xgboost.readthedocs.io/en/stable/tutorials/model.html)
- [skewness/kurtosis definitions](https://www.itl.nist.gov/div898/handbook/eda/section3/eda35b.htm)
- [one-sample mean tests](https://www.itl.nist.gov/div898/handbook/prc/section2/prc.htm)
- [two-sample t-tests](https://www.itl.nist.gov/div898/handbook/eda/section3/eda353.htm)
- [one-way ANOVA](https://www.itl.nist.gov/div898/handbook/eda/section3/eda354.htm)
- [HTTP semantics (RFC 9110)](https://www.rfc-editor.org/rfc/rfc9110.html)
- [PATCH (RFC 5789)](https://www.rfc-editor.org/rfc/rfc5789.html)
- [Fielding's REST constraints](https://roy.gbiv.com/pubs/dissertation/rest_arch_style.htm)
- [cookies (RFC 6265)](https://www.rfc-editor.org/rfc/rfc6265.html)
- [WHATWG Web Storage](https://html.spec.whatwg.org/multipage/webstorage.html)
- [WHATWG Fetch CORS protocol](https://fetch.spec.whatwg.org/#http-cors-protocol)
- [Filesystem Hierarchy Standard](https://refspecs.linuxfoundation.org/FHS_3.0/fhs-3.0.html)
- [Linux umask](https://man7.org/linux/man-pages/man2/umask.2.html)
- [Bash redirections](https://www.gnu.org/software/bash/manual/html_node/Redirections.html)
- [GNU sed](https://www.gnu.org/software/sed/manual/sed.html)
- [Scrum Guide 2020](https://scrumguides.org/scrum-guide.html)
- [merge](https://git-scm.com/docs/git-merge)
- [rebase](https://git-scm.com/docs/git-rebase)
- [stash](https://git-scm.com/docs/git-stash)
- [cherry-pick](https://git-scm.com/docs/git-cherry-pick)
- [NIST SP 800-145](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-145.pdf)
- [shared responsibility model](https://aws.amazon.com/compliance/shared-responsibility-model/)
- [Docker's container/VM explanation](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/)
- [start,end)` notation.

Concurrency questions state atomicity and memory-order assumptions when tracing shared variables. Semaphore traces explicitly distinguish signed counters from nonnegative available-permit counts. Resource vectors declare their component order, and Banker’s Algorithm questions use `Need = Max - Allocation`.

Memory-management questions define binary storage units, address bounds, TLB lookup and page-walk costs, and whether fault-service times include retries. Replacement traces specify initial frame contents, hit-update rules, and relevant tie-breaking or dirty-page costs.

Storage questions distinguish file data from indirect metadata and specify block-cache and inode-lifetime assumptions when relevant. Disk-scheduling traces define initial head direction, endpoint and wrap behavior, tie-breaking, arrivals, and when movement measurement stops.

Normalization questions treat the listed FDs and their logical consequences as the complete constraints. Normal forms assume atomic values unless a question explicitly examines 1NF. Dependency-preservation checks use full FD projections, including implied dependencies.

Transaction questions define schedule notation and any strict-versus-rigorous locking conventions that affect an answer. Recovery traces specify buffer policies, durable log contents, checkpoint guarantees, and redo/undo rules rather than assuming one database implementation.

Indexing questions state whether height counts edges, define node capacities and split rules, and distinguish internal separators from leaf records. ER mappings state optionality and uniqueness requirements. Integer difficulty quotas are rounded where exact percentages are impossible: Subpart 1.2.3 uses 8 Easy, 12 Medium, and 5 Hard; Subpart 1.2.4 uses 10 Easy, 18 Medium, and 7 Hard. Together, Subparts 1.2.1 through 1.2.4 have 36 Easy, 60 Medium, and 24 Hard questions out of 120, preserving the exact overall 30%/50%/20% distribution.

SQL questions use SQLite SQL with self-contained CTE input data. Options encode complete ordered results as JSON row arrays, where `null` represents SQL NULL. Queries with multiple output rows specify final ordering; window functions separately specify their own ordering and partitioning. All 35 SQL queries were executed against SQLite 3.45.3 to verify that exactly the keyed option matches the result.

Link-layer questions define ACK numbering, sequence modulus, window bounds, buffering, loss patterns, and timer rules. Timing questions distinguish serialization from propagation and state which overhead counts as useful data. Textbook CRC exercises define their polynomial and bit-order conventions; they do not assume a real Ethernet CRC parameter set. The rounded quotas are 8 Easy/12 Medium/5 Hard for Subpart 1.3.1 and 7 Easy/13 Medium/5 Hard for Subpart 1.3.2. Their combined 50 questions have exactly 15 Easy, 25 Medium, and 10 Hard, preserving 30%/50%/20% overall.

The bit/octet transparency rules were checked against [RFC 1662, Sections 4.2 and 5.2](https://www.rfc-editor.org/rfc/rfc1662.html)
- [RFC 1071, Section 1](https://www.rfc-editor.org/rfc/rfc1071.html)
- [RFC 791](https://www.rfc-editor.org/rfc/rfc791.html)
- [RFC 8200, Section 4.5](https://www.rfc-editor.org/rfc/rfc8200.html)
- [RFC 826](https://www.rfc-editor.org/rfc/rfc826.html)
- [RFC 1812](https://www.rfc-editor.org/rfc/rfc1812.html)
- [RFC 3022, Section 4.3](https://www.rfc-editor.org/rfc/rfc3022.html)
- [RFC 9293](https://www.rfc-editor.org/rfc/rfc9293.html)
- [RFC 768](https://www.rfc-editor.org/rfc/rfc768.html)
- [RFC 7323](https://www.rfc-editor.org/rfc/rfc7323.html)
- [RFC 5681](https://www.rfc-editor.org/rfc/rfc5681.html)
- [DNS (RFC 1035)](https://www.rfc-editor.org/rfc/rfc1035.html)
- [DNS over TCP (RFC 7766)](https://www.rfc-editor.org/rfc/rfc7766.html)
- [DHCPv4 (RFC 2131)](https://www.rfc-editor.org/rfc/rfc2131.html)
- [SMTP (RFC 5321)](https://www.rfc-editor.org/rfc/rfc5321.html)
- [FTP (RFC 959)](https://www.rfc-editor.org/rfc/rfc959.html)
- [RFC 8446](https://www.rfc-editor.org/rfc/rfc8446.html)
- [RFC 9525](https://www.rfc-editor.org/rfc/rfc9525.html)
- [C++ classes specification](https://eel.is/c++draft/class)
- [Java Language Specification, Chapter 8](https://docs.oracle.com/javase/specs/jls/se17/html/jls-8.html)
- [JLS Chapter 12](https://docs.oracle.com/javase/specs/jls/se17/html/jls-12.html)
- [JLS Chapter 14](https://docs.oracle.com/javase/specs/jls/se17/html/jls-14.html)
