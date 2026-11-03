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
| `questions/module_1_core_cs/1.3.2_network_layer_routing.json` | Network Layer, IP Addressing & Routing | 25 | 7 | 13 | 5 |
| `questions/module_1_core_cs/1.3.3_transport_layer.json` | Transport Layer Protocols | 25 | 8 | 12 | 5 |
| `questions/module_1_core_cs/1.3.4_application_security.json` | Application Layer Protocols & Network Security | 25 | 7 | 13 | 5 |
| `questions/module_1_core_cs/1.4.1_oop_architecture.json` | Core Architecture & Class Mechanics | 30 | 9 | 15 | 6 |
| `questions/module_1_core_cs/1.4.2_object_lifecycle.json` | Object Lifecycle & Memory Management | 30 | 9 | 15 | 6 |

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

Link-layer questions define ACK numbering, sequence modulus, window bounds, buffering, loss patterns, and timer rules. Timing questions distinguish serialization from propagation and state which overhead counts as useful data. Textbook CRC exercises define their polynomial and bit-order conventions; they do not assume a real Ethernet CRC parameter set. The rounded quotas are 8 Easy/12 Medium/5 Hard for Subpart 1.3.1 and 7 Easy/13 Medium/5 Hard for Subpart 1.3.2. Their combined 50 questions have exactly 15 Easy, 25 Medium, and 10 Hard, preserving 30%/50%/20% overall.

The bit/octet transparency rules were checked against [RFC 1662, Sections 4.2 and 5.2](https://www.rfc-editor.org/rfc/rfc1662.html), and one's-complement checksum arithmetic against [RFC 1071, Section 1](https://www.rfc-editor.org/rfc/rfc1071.html). Any simplified framing model is stated explicitly in its question.

Network-layer questions state subnet reservations, route-selection rules, DV update order, and fragmentation units. IPv4 packet sizing and refragmentation were checked against [RFC 791](https://www.rfc-editor.org/rfc/rfc791.html), and source-only IPv6 fragmentation against [RFC 8200, Section 4.5](https://www.rfc-editor.org/rfc/rfc8200.html). ARP examples follow [RFC 826](https://www.rfc-editor.org/rfc/rfc826.html); TTL/DF-related ICMP behavior follows [RFC 1812](https://www.rfc-editor.org/rfc/rfc1812.html). NAPT examples explicitly define their mappings, including related-ICMP embedded-header translation described in [RFC 3022, Section 4.3](https://www.rfc-editor.org/rfc/rfc3022.html).

Transport questions distinguish byte-stream framing, cumulative byte ACKs, SYN/FIN sequence consumption, and accepted resets using [RFC 9293](https://www.rfc-editor.org/rfc/rfc9293.html). UDP length/checksum examples follow [RFC 768](https://www.rfc-editor.org/rfc/rfc768.html), and window scaling follows [RFC 7323](https://www.rfc-editor.org/rfc/rfc7323.html). Congestion examples explicitly state their idealized RTT or classic Reno rules, including FlightSize-based thresholds from [RFC 5681](https://www.rfc-editor.org/rfc/rfc5681.html); they do not assume every modern TCP implementation uses that model.

Application examples distinguish SMTP relay from submission, active from passive FTP, and TLS-over-TCP from HTTP/3. Protocol checks use [HTTP semantics (RFC 9110)](https://www.rfc-editor.org/rfc/rfc9110.html), [DNS (RFC 1035)](https://www.rfc-editor.org/rfc/rfc1035.html), [DNS over TCP (RFC 7766)](https://www.rfc-editor.org/rfc/rfc7766.html), [DHCPv4 (RFC 2131)](https://www.rfc-editor.org/rfc/rfc2131.html), [SMTP (RFC 5321)](https://www.rfc-editor.org/rfc/rfc5321.html), and [FTP (RFC 959)](https://www.rfc-editor.org/rfc/rfc959.html). TLS 1.3 examples specify the key-exchange/replay assumptions from [RFC 8446](https://www.rfc-editor.org/rfc/rfc8446.html), with service-identity checks from [RFC 9525](https://www.rfc-editor.org/rfc/rfc9525.html). Firewall questions define their own matching and state policy. Subparts 1.3.3 and 1.3.4 use 8/12/5 and 7/13/5 difficulty quotas, totaling exactly 15 Easy, 25 Medium, and 10 Hard.

OOP snippets specify C++17 or Java 17. Their class/access rules were checked against the [C++ classes specification](https://eel.is/c++draft/class) and [Java Language Specification, Chapter 8](https://docs.oracle.com/javase/specs/jls/se17/html/jls-8.html). Self-contained examples can be checked with `python scripts/verify_oop_examples.py`, using a C++17 compiler and a JDK supporting `--release 17`. Use `--cxx` and `--java-home` to select toolchains, or pass individual JSON paths. The verifier compares successful output and expected compilation rejection; conceptual questions are reviewed separately. Snippets classified as undefined behavior are compiled but never executed as though they had a predictable output.

Lifecycle examples distinguish construction from assignment, owning from non-owning pointer copies, and complete objects from partially constructed subobjects. Java GC questions use explicit strong-root graphs and ask about eligibility, not nondeterministic collection timing; initialization rules follow [JLS Chapter 12](https://docs.oracle.com/javase/specs/jls/se17/html/jls-12.html). C++17 elision questions use guaranteed prvalue cases rather than optional named-return-value optimization.
