# Intervyn MCQ Question Bank

Questions are grouped by module and subpart under `questions/`, following the agreed topic filenames. Populated subparts:

| File | Topic | Questions | Easy | Medium | Hard |
| --- | --- | ---: | ---: | ---: | ---: |
| `questions/module_1_core_cs/1.1.1_cpu_scheduling.json` | CPU Scheduling & Process Lifecycle | 30 | 9 | 15 | 6 |
| `questions/module_1_core_cs/1.1.2_concurrency_deadlocks.json` | Concurrency, Synchronization & Deadlocks | 30 | 9 | 15 | 6 |
| `questions/module_1_core_cs/1.1.3_memory_management.json` | Memory Management & Virtual Memory | 30 | 9 | 15 | 6 |
| `questions/module_1_core_cs/1.1.4_storage_disk.json` | Storage Systems, File Systems & Disk Scheduling | 20 | 6 | 10 | 4 |
| `questions/module_1_core_cs/1.2.1_schema_normalization.json` | Relational Schema Design & Normalization | 30 | 9 | 15 | 6 |
| `questions/module_1_core_cs/1.2.2_transactions_concurrency.json` | Transactions, Concurrency & Recovery | 30 | 9 | 15 | 6 |
| `questions/module_1_core_cs/1.2.3_storage_indexing.json` | Storage, Indexing & ER Modeling | 25 | 8 | 12 | 5 |
| `questions/module_1_core_cs/1.2.4_sql_queries.json` | SQL Queries & Output Prediction | 35 | 10 | 18 | 7 |
| `questions/module_1_core_cs/1.3.1_network_architecture.json` | Network Architecture & Physical/Data Link Layers | 25 | 8 | 12 | 5 |

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

Use Python 3.9 or later; no third-party packages are needed. Run before committing:

```sh
python scripts/validate_questions.py
```

To check one file or directory:

```sh
python scripts/validate_questions.py questions/module_1_core_cs/1.1.1_cpu_scheduling.json
```

The validator checks strict JSON syntax (including duplicate keys and invalid constants), required fields and types, metadata, unique IDs and question text, four distinct option texts, answer keys, and configured subpart quotas. It exits with a nonzero status on failure. Exact quota checks cover all populated subparts listed above; add quota metadata in `SUBPARTS` as further subparts are populated.

Content review must still establish that options are mutually exclusive, exactly one is correct, and explanations are accurate. Structural validation cannot prove those properties. Scheduling questions state tie-breaking, arrival ordering, I/O behavior, and switch-cost conventions whenever those affect the result. Timeline intervals use `[start,end)` notation.

Concurrency questions state atomicity and memory-order assumptions when tracing shared variables. Semaphore traces explicitly distinguish signed counters from nonnegative available-permit counts. Resource vectors declare their component order, and Banker’s Algorithm questions use `Need = Max - Allocation`.

Memory-management questions define binary storage units, address bounds, TLB lookup and page-walk costs, and whether fault-service times include retries. Replacement traces specify initial frame contents, hit-update rules, and relevant tie-breaking or dirty-page costs.

Storage questions distinguish file data from indirect metadata and specify block-cache and inode-lifetime assumptions when relevant. Disk-scheduling traces define initial head direction, endpoint and wrap behavior, tie-breaking, arrivals, and when movement measurement stops.

Normalization questions treat the listed FDs and their logical consequences as the complete constraints. Normal forms assume atomic values unless a question explicitly examines 1NF. Dependency-preservation checks use full FD projections, including implied dependencies.

Transaction questions define schedule notation and any strict-versus-rigorous locking conventions that affect an answer. Recovery traces specify buffer policies, durable log contents, checkpoint guarantees, and redo/undo rules rather than assuming one database implementation.

Indexing questions state whether height counts edges, define node capacities and split rules, and distinguish internal separators from leaf records. ER mappings state optionality and uniqueness requirements. Integer difficulty quotas are rounded where exact percentages are impossible: Subpart 1.2.3 uses 8 Easy, 12 Medium, and 5 Hard; Subpart 1.2.4 uses 10 Easy, 18 Medium, and 7 Hard. Together, Subparts 1.2.1 through 1.2.4 have 36 Easy, 60 Medium, and 24 Hard questions out of 120, preserving the exact overall 30%/50%/20% distribution.

SQL questions use SQLite SQL with self-contained CTE input data. Options encode complete ordered results as JSON row arrays, where `null` represents SQL NULL. Queries with multiple output rows specify final ordering; window functions separately specify their own ordering and partitioning. All 35 SQL queries were executed against SQLite 3.45.3 to verify that exactly the keyed option matches the result.

Link-layer questions define ACK numbering, sequence modulus, window bounds, buffering, loss patterns, and timer rules. Timing questions distinguish serialization from propagation and state which overhead counts as useful data. Textbook CRC exercises define their polynomial and bit-order conventions; they do not assume a real Ethernet CRC parameter set. Subpart 1.3.1 uses the rounded 25-question quota of 8 Easy, 12 Medium, and 5 Hard.

The bit/octet transparency rules were checked against [RFC 1662, Sections 4.2 and 5.2](https://www.rfc-editor.org/rfc/rfc1662.html), and one's-complement checksum arithmetic against [RFC 1071, Section 1](https://www.rfc-editor.org/rfc/rfc1071.html). Any simplified framing model is stated explicitly in its question.
