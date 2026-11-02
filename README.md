# Intervyn MCQ Question Bank

Questions are grouped by module and subpart under `questions/`, following the agreed topic filenames. Populated subparts:

| File | Topic | Questions | Easy | Medium | Hard |
| --- | --- | ---: | ---: | ---: | ---: |
| `questions/module_1_core_cs/1.1.1_cpu_scheduling.json` | CPU Scheduling & Process Lifecycle | 30 | 9 | 15 | 6 |
| `questions/module_1_core_cs/1.1.2_concurrency_deadlocks.json` | Concurrency, Synchronization & Deadlocks | 30 | 9 | 15 | 6 |

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

The validator checks strict JSON syntax (including duplicate keys and invalid constants), required fields and types, metadata, unique IDs and question text, four distinct option texts, answer keys, and configured subpart quotas. It exits with a nonzero status on failure. Exact quota checks currently cover Subparts 1.1.1 and 1.1.2; add quota metadata in `SUBPARTS` as further subparts are populated.

Content review must still establish that options are mutually exclusive, exactly one is correct, and explanations are accurate. Structural validation cannot prove those properties. Scheduling questions state tie-breaking, arrival ordering, I/O behavior, and switch-cost conventions whenever those affect the result. Timeline intervals use `[start,end)` notation.

Concurrency questions state atomicity and memory-order assumptions when tracing shared variables. Semaphore traces explicitly distinguish signed counters from nonnegative available-permit counts. Resource vectors declare their component order, and Banker’s Algorithm questions use `Need = Max - Allocation`.
