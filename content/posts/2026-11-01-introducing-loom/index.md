---
title: "Introducing loom: A Zero-Dependency Sandboxed Leaf-Agent CLI for Reproducible Multi-Agent Workflows"
date: "2026-11-01T12:00:00.000-05:00"
lastmod: "2026-11-01T19:30:00.000-05:00"
math: true
categories:
  - "news"
  - "research"
  - "open-source"
  - "ai"
  - "research-tools"
tags:
  - "Loom"
  - "Nexus-Lite"
  - "QRadiomics"
  - "medimage"
  - "Multi-Agent"
  - "Go"
  - "CLI"
  - "Google Colab"
  - "Gemini"
  - "Anthropic"
  - "Ollama"
  - "HIPAA"
  - "PHI"
  - "IBSI-SUV"
  - "Radiomics"
  - "Reproducibility"
cover:
  image: "images/loom-overview.svg"
  alt: "loom zero-dependency sandboxed leaf-agent CLI architecture for nexus-lite and qradiomics"
  relative: true
aliases:
  - /loom/
  - /nexus-loom/
  - /2026/11/01/introducing-loom/
  - /projects/loom/
description: "Introducing loom (v0.2.3), a dependency-free Go stdlib single-agent CLI with workspace sandboxing, multi-turn context piping (loom.context.v1), hard turn/token/time budgets, --phi local-model confinement, and hidden-test IBSI radiomics verification with nexus-lite."
---

Today we are releasing **[loom](https://github.com/choilab-jefferson/nexus.loom)** (`v0.2.3`, MIT License), a small, zero-dependency (**Go 1.22+ standard library only**) single-agent CLI engineered to execute one bounded coding or scientific task per run as an unattended leaf worker.

Across our open-source computational oncology stack, each layer has a distinct responsibility:
- **[qradiomics](/qradiomics/)** (`v0.9.6`, [PyPI](https://pypi.org/project/qradiomics/)) provides the domain-specific Unix CLI (`qr`) and Python atomic library for DICOM/RTSTRUCT conversion, **IBSI-1** & **IBSI-SUV v3.1** PET normalization, deformable registration (`sitk`, `plastimatch`, `elastix`), longitudinal contour QC (`qr longitudinal`), 3D shape biomarkers (`AHSN`, `spic6`, solid-core remodeling), and survival/ML benchmarking (`qr bench`).
- **[medimage](/posts/2026-08-04-introducing-medimage/)** teaches those quantitative imaging workflows through a 13-chapter zero-setup Google Colab curriculum.
- **[nexus-lite](/nexus-lite/)** (`v0.2.2`, [PyPI: `pip install nexus-lite`](https://pypi.org/project/nexus-lite/)) provides the zero-server multi-agent orchestration kernel (`dtach` PTYs, SQLite WAL Bus v1, 3-tier memory `stm`/`mtm`/`ltm`, parallel swarms, role pipelines, and zero-preinstall remote compute).
- **`loom` (`nexus.loom` `v0.2.3`) is the deterministic leaf-worker binary**: one agent, one bounded task (or one composable turn via `loom.context.v1` stdin/stdout piping), a strict workspace sandbox, allowlisted command execution with timeout clamping (`--max-cmd-timeout`), hard turn/token/time budgets, and a resumable JSONL trace—with **zero external runtime dependencies**, **zero implicit host-state reads**, and **zero configuration files**.

- **Repository:** [github.com/choilab-jefferson/nexus.loom](https://github.com/choilab-jefferson/nexus.loom) · **Version:** `v0.2.3` · **License:** MIT
- **Prebuilt Releases:** [github.com/choilab-jefferson/nexus.loom/releases](https://github.com/choilab-jefferson/nexus.loom/releases) (`loom-linux-amd64`, `loom-darwin-arm64`, `loom-darwin-amd64` + SHA-256 `checksums.txt`)
- **Python Installer (via `nexus-lite` on PyPI):** `pip install nexus-lite && nexus-lite loom install`
- **Interactive Google Colab Notebooks Featuring `loom`:**
  - **Loom Multi-Agent, 93-Test IBSI Radiomics & Remote Compute (`loom_multi_agent_colab.ipynb`):** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/choilab-jefferson/nexus.lite/blob/main/notebooks/loom_multi_agent_colab.ipynb)
  - **Nexus-Lite Core Primitives + Cell 9 Loom Verification (`nexus_lite_colab_demo.ipynb`):** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/choilab-jefferson/nexus.lite/blob/main/notebooks/nexus_lite_colab_demo.ipynb)
  - **QRadiomics + MedImage Suite + Demo 7 Loom IBSI Suite (`qradiomics_medimage_colab_demo.ipynb`):** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/choilab-jefferson/nexus.lite/blob/main/notebooks/qradiomics_medimage_colab_demo.ipynb)

---

## Why `loom`? The Bounded Leaf-Worker Philosophy

Full interactive coding terminals (`agy`, `claude`, `opencode`) excel at open-ended interactive sessions, but unattended multi-agent pipelines in Google Colab, CI runners, and hospital HPC clusters also require a **hermetic, single-shot leaf worker** that obeys strict operational contracts:

1. **Zero Dependencies (Go Standard Library Only) & Zero Host-State Leakage**: `loom` compiles to a single static binary with no third-party Go modules (`go.mod` has zero `require` directives), no Node/Python runtime dependencies, no background daemon, and no interactive TTY prompts. In `v0.2.3`, `loom` reads **no implicit host Nexus state**—the caller owns all context via the prompt, `task_slice.context_files`, or explicit `--context-in` / `--context-out` (`loom.context.v1`) files.
2. **Strict Workspace Sandbox, Command Allowlisting & Timeout Clamping**: File tools (`read_file`, `search`, `edit_file`, `write_file`) resolve symlinks and refuse any path escaping `--workspace` or matching deny globs. `run_command` executes only explicitly allowlisted `argv` prefixes (`--allow-cmd`, computed as $\text{global} \cap \text{agent} \cap \text{task}$), clamps per-command execution time via `--max-cmd-timeout` (default `300s`), never invokes a shell (`sh -c`), and rejects interpreter evaluation flags (`python -c`, `node -e`).
3. **Composable Multi-Turn Context Piping (`loom.context.v1`)**: Each `loom` invocation answers one bounded turn, while `--context-out` and `--context-in` serialize and restore `loom.context.v1` JSON over files or Unix pipes (`-` for stdin/stdout)—allowing callers to chain turns across different providers (`anthropic` → `gemini` → `ollama`) or inspect and prune history between turns.
4. **Hard Budgets & Machine-Readable Exit Codes**: Every invocation is bounded by turn (`--max-turns`), token (`--max-total-tokens`, `--max-output-tokens`), tool-call (`--max-tool-calls`), and wall-clock (`--deadline`) budgets. When a run finishes or hits a boundary, `loom` emits a structured exit code and JSON summary that **[nexus-lite](/nexus-lite/)** maps directly to retry, escalation, or provider fallback logic.
5. **Clinical `--phi` Local-Only Confinement & Secret Scrubbing**: Passing `--phi` enforces strict local-only model execution (refusing non-local cloud API endpoints). API keys (`*_API_KEY`, `*TOKEN*`) are automatically scrubbed from child-process environments and redacted from all error streams and traces.
6. **Parallel Execution Safety (`flock`) & Atomic Checkpointing**: Multiple `loom` workers can run concurrently across subtasks. Each `--workspace` and `--trace` is guarded by a kernel-managed advisory `flock` (preventing collisions with zero stale lock files), and every turn is atomically checkpointed to `<trace>.ckpt` for instant `loom resume <trace>`.

---

## Installation & 60-Second Quickstart

### Install via `nexus-lite` (PyPI), Prebuilt Release, or Go Source

```bash
# Option 1: Install via nexus-lite (PyPI) — downloads & SHA-256-verifies ~/.local/bin/loom
pip install nexus-lite
nexus-lite loom install

# Option 2: Download checksum-verified prebuilt binary directly (e.g., Linux amd64 for Colab)
curl -fsSL -o loom https://github.com/choilab-jefferson/nexus.loom/releases/download/v0.2.3/loom-linux-amd64
curl -fsSL -o checksums.txt https://github.com/choilab-jefferson/nexus.loom/releases/download/v0.2.3/checksums.txt
grep loom-linux-amd64 checksums.txt | sed 's/loom-linux-amd64/loom/' | sha256sum -c -
chmod +x loom && ./loom version

# Option 3: Build from Go 1.22+ source (zero external dependencies)
git clone https://github.com/choilab-jefferson/nexus.loom.git
cd nexus.loom && make build   # produces ./bin/loom
```

### 60-Second CLI Usage & Multi-Turn Context Piping (`v0.2.3`)

```bash
# 1. Offline smoke test (no model, no network, no API key)
loom -p "hello" --provider mock --json

# 2. Local model via Ollama (`ollama serve` running locally or on a Colab GPU)
loom -p "Add unit tests for foo()" --workspace ./work --provider ollama

# 3. Hosted model with an allowlisted test command, command timeout clamp, and turn budget
export ANTHROPIC_API_KEY=sk-...
loom -p "Fix the failing edge case in discretise.py" \
  --workspace ./work \
  --provider anthropic \
  --allow-cmd "pytest -q" \
  --max-cmd-timeout 60s \
  --max-turns 8 \
  --trace run.jsonl \
  --json

# 4. Multi-turn conversation piping across providers (loom.context.v1 via stdin/stdout `-`)
loom -p "Draft discretise.py with IBSI fixed_bin_width" --provider anthropic --context-out - \
  | loom -p "Now add edge-case tests for exact bin boundaries" --provider gemini --context-in - --context-out ctx.json
```

The default `--provider auto` selects the first configured key among `ANTHROPIC_API_KEY`, `GEMINI_API_KEY` / `GOOGLE_API_KEY`, or `OPENAI_API_KEY`, falling back to a reachable local Ollama server (`OLLAMA_HOST`, default `127.0.0.1:11434`).

---

## Providers, CLI Flags & Structured Exit Codes

### Supported Model Providers

| Provider (`--provider`) | Default Model (`--model` / `LOOM_MODEL`) | Credential / Endpoint |
| :--- | :--- | :--- |
| `auto` *(default)* | Provider default | First available key (`ANTHROPIC` → `GEMINI` → `OPENAI`) else local `ollama` |
| `gemini` | `gemini-3.8-flash` | `GEMINI_API_KEY` or `GOOGLE_API_KEY` |
| `anthropic` | `claude-sonnet-5-5` | `ANTHROPIC_API_KEY` |
| `openai` | `gpt-4o-mini` | `OPENAI_API_KEY` |
| `ollama` | `qwen3:4b` (`qwen3.5:4b-mlx` on macOS) | `OLLAMA_HOST` (default `http://127.0.0.1:11434`) |
| `google-agent-platform` | Platform default | `NEXUS_GCP_PROJECT` + `NEXUS_GOOGLE_AGENT_API_KEY` |
| `typesafe` | Provider default | `TYPESAFE_API_KEY` |
| `mock` | Scripted offline responder | None (offline deterministic smoke testing) |

Query live model IDs available to your credentials at any time with:

```bash
loom models --provider gemini --json
```

### Core CLI Flags & Subcommands (`v0.2.3`)

| Flag / Command | Purpose |
| :--- | :--- |
| `-p "<prompt>"` / `loom run --task-file task.json` | Execute a one-shot prompt or structured JSON task specification |
| `--workspace <dir>` | Confine all file reads, edits, writes, and searches to `<dir>` (symlinks resolved) |
| `--context-in <file\|->`, `--context-out <file\|->` | Read/write multi-turn `loom.context.v1` conversation history JSON (supports `-` for Unix pipes across providers) |
| `--allow-cmd "<prefix>"` | Allowlist a command prefix for `run_command` (repeatable; empty by default) |
| `--max-cmd-timeout <S\|duration>` | Clamp `run_command` timeout per call (default `300s`; supports durations like `10m` or `LOOM_MAX_CMD_TIMEOUT`) |
| `--pass-env NAME[,PREFIX*]` | Pass extra environment variables to `run_command` children (ML vars like `PYTHONPATH`, `CUDA_*`, `HF_HOME` pass by default; secrets require exact name) |
| `--no-agents-md` (`LOOM_NO_AGENTS_MD=1`) | Disable automatic loading of `<workspace>/AGENTS.md` into the system prompt |
| `--max-turns`, `--max-total-tokens`, `--max-output-tokens`, `--max-tool-calls`, `--deadline` | Hard execution budgets per invocation |
| `--phi` | Enforce local-only model endpoints for PHI/HIPAA workloads |
| `--trace <file.jsonl>`, `--json` | Write per-turn JSONL execution trace and emit machine-readable final result |
| `loom resume <trace.jsonl>` | Resume an interrupted (`130`) run from its atomic `<trace>.ckpt` checkpoint |
| `loom capabilities --json` | Emit the machine-readable contract (available tools, providers, exit codes, version) |

### Deterministic Exit Code Contract

| Exit Code | Policy Constant | Meaning & Orchestrator Action |
| :---: | :--- | :--- |
| `0` | `policy.ExitOK` | Task completed within turn and token budgets (`ok`) |
| `1` | `policy.ExitTaskFail` | Retryable task failure or `max_turns` exhausted (`task_failure`) |
| `2` | `policy.ExitHarnessErr` | Fatal harness/config error, missing key, lock collision, or `PolicyViolationError` (`harness_or_policy_error`) |
| `3` | `policy.ExitEscalate` | Structured `escalation_required` JSON payload emitted on stdout (`escalation_required`) |
| `4` | `policy.ExitBudget` | Token, wall-clock deadline, or tool-call budget exhausted (`budget`) |
| `130` | `policy.ExitInterrupted` | `SIGINT` / `SIGTERM`; resumable via `loom resume <trace>` (`interrupted`) |

---

## Orchestrating `loom` from `nexus-lite v0.2.2` in Google Colab & Remote Compute

While `loom` is intentionally a single-agent CLI, **[nexus-lite](/nexus-lite/)** (`v0.2.2`, on [PyPI](https://pypi.org/project/nexus-lite/)) turns `loom` into a multi-agent team (`Orchestrator → Workers → Reviewer`) via `nexus_lite.loom` and `nexus_lite.demos.loom_multi_agent`, and can even ship `loom` workflows to remote hosts with zero pre-installation via `nexus_lite.compute`.

### 1. Explicit SHA-256 Installer & Python Subprocess Adapter (`nexus_lite.loom`)

```python
from nexus_lite import loom
from nexus_lite.loom import probe, LoomAdapter

# Explicitly install checksum-verified loom binary (~/.local/bin/loom) if missing
if not probe().available:
    loom.install_loom()

# Discover binary availability, version (>= 0.1.0), and JSON capabilities
status = probe()
print(f"Loom available: {status.available}, version: {status.version}")

# Run a bounded prompt with strict environment allowlisting
adapter = LoomAdapter()
result = adapter.run_prompt(
    "Implement fixed_bin_width(values, width, minimum) in discretise.py",
    provider="auto",
)
print(result.status, result.ok, result.returncode)
```

### 2. Multi-Agent Team vs. Single-Agent Baseline with 93 Hidden IBSI Radiomics Acceptance Tests

In [`notebooks/loom_multi_agent_colab.ipynb`](https://github.com/choilab-jefferson/nexus.lite/blob/main/notebooks/loom_multi_agent_colab.ipynb) (and in Cell 9 of `nexus_lite_colab_demo.ipynb` and Demo 7 of `qradiomics_medimage_colab_demo.ipynb`), `nexus-lite` benchmarks a multi-agent `loom` workflow against a single-agent `loom` baseline under strict anti-leakage rules:
1. **Orchestrator (`loom`)**: Splits a multi-module specification into per-file worker assignments.
2. **Parallel Workers (`loom`)**: Each worker writes its assigned Python module inside an isolated sandbox (`--workspace`).
3. **External Hidden Test Suite**: The Python harness runs **hidden unit tests** stored outside the workspace sandbox (never shown to any agent in any prompt).
4. **Advisory Reviewer (`loom`) & Targeted Rework**: If hidden tests fail, the reviewer receives only the failing test names and failure kinds (never the test source code or expected assertion values) and routes rework instructions back to the responsible worker (up to 2 rework rounds), with automatic retry, secret redaction (`redact()`), and cross-provider fallback (`anthropic` ↔ `gemini`).

### 3. Three Pluggable IBSI Radiomics Verification Suites (93 Hidden Tests, 12 Modules)

To benchmark coding agents on real quantitative medical imaging math—where off-by-one bin boundaries, slice-stacking inversions, or data leakage invalidate clinical studies—`nexus_lite.demos.loom_radiomics_tasks` includes three pluggable IBSI radiomics benchmark suites (`--task NAME[,NAME...]|all`) totaling **93 hidden unit tests** across **12 pure-stdlib modules**:

| Task Name | Sandboxed Worker Modules | Hidden Tests | Hidden-Test Medical Physics & IBSI Edge Cases |
| :--- | :--- | :---: | :--- |
| **`radiomics-firstorder`** | `discretise.py`<br>`roi.py`<br>`moments.py`<br>`distribution.py` | **33** | • **IBSI Discretization**: `fixed_bin_width` ($\lfloor (x - \min)/w \rfloor + 1$, exact bin-edge goes to higher bin) & `fixed_bin_number` (maximum value clamped to $n_{\text{bins}}$)<br>• **3D ROI & Re-Segmentation**: Row-major mask extraction (rejecting `bool` as `int`), inclusive $[lo, hi]$ range filtering<br>• **First-Order Statistics**: Population variance ($1/n$), zero-variance skewness/kurtosis handling, $\log_2$ Shannon entropy, and P10–P90 robust MAD (`rMAD`) |
| **`radiomics-texture`** | `glcm.py`<br>`glcm_features.py`<br>`glrlm.py`<br>`glrlm_features.py` | **34** | • **Mask-Aware 2D GLCM**: Symmetric normalized co-occurrence across $0^\circ, 45^\circ, 90^\circ, 135^\circ$ (only in-mask pairs), joint max, energy, contrast, homogeneity, entropy, correlation, autocorrelation<br>• **Mask-Aware 2D GLRLM**: Maximal contiguous run lengths per angle, SRE, LRE, GLNU, RLNU, Run Percentage ($N_r / N_p$), LGRE, HGRE |
| **`radiomics-stats`** | `icc.py`<br>`fdr.py`<br>`standardise.py`<br>`cindex.py` | **26** | • **Reproducibility & Multiple Testing**: Two-way mixed consistency $\text{ICC}(3,1)$ and Benjamini–Hochberg monotone FDR $q$-values (preserving original feature order)<br>• **Leakage-Safe Modeling**: Train-only z-score (`fit_zscore` / `apply_zscore`) and Harrell's survival concordance index ($C$-index) with censoring and tie rules |

*(For full DICOM PET **IBSI-SUV v3.1** standardization—including `BW`, `LBM`, `LBMJAMES128`, `LBMJANMA`, `IBW`, `BSA`, `START`/`ADMIN` decay, and frame-duration $t_{\text{ave}}$ scan-start reconstruction—see **[qradiomics](/qradiomics/) `v0.9.6`**'s native `qradiomics.io.dicom.pet_suv` engine.)*

Run the `loom` radiomics multi-agent benchmarks and zero-preinstall remote compute bundle locally or in Google Colab:

```bash
# Offline deterministic smoke run across all 3 IBSI suites (93 hidden tests, zero API keys required)
python examples/loom_radiomics.py --providers mock

# Live multi-agent benchmark on IBSI statistics with Anthropic + Gemini fallback
python examples/loom_radiomics.py --task radiomics-stats --providers anthropic,gemini --json-out stats_run.json

# Run via module entrypoint on texture features
python -m nexus_lite.demos.loom_multi_agent --task radiomics-texture --providers anthropic,gemini

# Run zero-preinstall remote compute + Loom multi-agent verification over a Colab tunnel
python examples/remote_compute_and_loom.py
```

---

## Acknowledgements

We gratefully acknowledge **Google** for providing **Gemini 4 Argon** access and compute support, which powered the multi-agent orchestration, sandboxed leaf-worker verification, and IBSI radiomics benchmarking across **[loom](https://github.com/choilab-jefferson/nexus.loom)**, **[nexus-lite](/nexus-lite/)**, **[qradiomics](/qradiomics/)**, and **[medimage](/posts/2026-08-04-introducing-medimage/)**.

---

*Computational Healthcare & Oncology Informatics (CHOI) Lab, Department of Radiation Oncology, Sidney Kimmel Medical College at Thomas Jefferson University* · [Wookjin Choi, Ph.D.](/profile/) · MIT License
