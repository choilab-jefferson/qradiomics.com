# Nexus Agent Universal Protocol (AGENTS.md)

> **READ THIS FIRST.** If you are an AI agent in this repo without prior Nexus knowledge, read this entire file before acting. Do not improvise.

## 0. Basic Rules
- **Communication**: User conversation in **Korean**. Repo, Wiki, docs, git messages: **English only**.
- **Style**: Technical caveman. Fact-based, concise, no filler.
- **Maintenance**: Keep this file **under 200 lines**. Auto-optimize if exceeded.

## 1. Core Principles
- **Wiki-First (LTM)**: Wiki is the definitive spec. Code is derivative. Read `nexus wiki query` before acting. Follow [wiki/protocols/LLM-Wiki-Protocol.md](./wiki/protocols/LLM-Wiki-Protocol.md) before writing wiki.
- **Stateless (MTM+)**: Task state lives in Redis SSOT only. Local `plan.md` is **prohibited**.
- **Issue-Driven**: Every significant change requires a GitLab Issue ID + MR.

## 2. Agent Hierarchy

| Agent | Role | Entry |
|-------|------|-------|
| **Nexus** | User-facing orchestrator. Strategy, human interface. | `nexus agent <prompt>` |
| **Mini-Nexus** | Background orchestrator. Complex pipelines, nested delegation. | `nexus mini <prompt>` |
| **Mini-Worker** | General-purpose single-shot executor. | `delegate(agent_name="mini-worker")` |
| **Mini-Driver** | Implementation specialist. | `delegate(agent_name="mini-driver")` |
| **Mini-Navigator** | Logic/security reviewer. | `delegate(agent_name="mini-navigator")` |
| **Mini-Refiner** | Final verdict: Confirm/Modify/Rollback. | `delegate(agent_name="mini-refiner")` |
| **Mini-Verifier** | Output validator. Returns PASS/FAIL vs. success criteria. Triggers re-plan on FAIL. | `delegate(agent_name="mini-verifier")` |
| **Graphify-Runner** | Knowledge graph generation. | `delegate(agent_name="graphify-runner")` |

## 3. Communication & Identity

Two channels carry agent messages — they are **not interchangeable**. See [wiki/protocols/Communication-Layers.md](./wiki/protocols/Communication-Layers.md) for the workflow SSOT.

- **Intra-project (now-traffic)**: Agent-Bus (Redis Streams) — DM via `target=<instanceId>`, broadcast via `target=ALL`. Session-scoped, transient, never crosses project prefix (except opt-in global hub).
- **Inter-project (cross-boundary)**: GitLab issue board via `glab` — durable, owned by the target project, closed by its maintainer. Always reference as `<group>/<project>#<iid>`. File on the target's board, not your own.
- **Knowledge layer (LTM+)**: IKB — retrieval, not communication. Don't conflate with the issue board.
- **Centralized ID**: Agents MUST NOT self-generate IDs. Register with `nexus-core` on startup.
- **DM Reply Rule**: Messages from `nexus-term` or direct inbox MUST be answered with `target=sender`. No broadcast replies to DMs.
- **Identity Clarification**: Prepend identity prompts when calling sub-agents via shell (e.g., "You are mini-driver, NOT Gemini").
- **Auto-Launch Stack**: Any Nexus MCP boot silently starts: nexus-core, project opencode-lite, community hub (port 4090). Opt out: `NEXUS_AUTOSTART_LITE=0` / `NEXUS_AUTOSTART_COMMUNITY=0`.
- **Headless Entry**: `nexus agent <prompt>` (orchestrator) or `nexus mini <prompt>`. Provider order: `claude > gemini > opencode > delegate`. Override: `NEXUS_AGENT_PROVIDER`.

## 4. Memory & Knowledge Hierarchy

| Layer | Type | Platform | Purpose |
|-------|------|----------|---------|
| **STM** | Active | Context Window | Short-term reasoning, tool outputs |
| **MTM** | Real-time | Agent-Bus (Redis Streams) | Signals, peer coordination |
| **MTM+** | Task | Redis SSOT | Canonical task state (status, pid) |
| **LTM** | Knowledge | Git-first Wiki | Source of Truth — architecture, specs |
| **LTM+** | Search | IKB | Cross-project semantic search (`ikb` CLI) |

### 4.1 Process Isolation
- Each pipeline step (Driver → Navigator → Refiner) runs as a **separate CLI process**.
- Sub-agents share no memory. Communication only via artifacts: `~/.local/share/nexus/artifacts/{project_id}/{timestamp}_{task_id}/`.
- Payload > 2000 chars: store in `wiki/_temp/`, share path via agent-bus.
- **Worktree by default (every agent)**: every non-trivial change runs inside a git worktree, not the primary checkout. Primary trees (meta-repo + each submodule) stay on `main` permanently; create `git worktree add ../.worktrees/<feature> -b feat/<name> origin/main` and work there. Delegated workers auto-spawn into `<repo>/.worktrees/worker-<task_id>/` via `worker_worktree.py` (see [Worker-Worktree](wiki/architecture/Worker-Worktree)). Break-glass: `NEXUS_WORKER_WORKTREE=0`, CLI `--no-worktree`, MCP `worktree=False`. Cleanup `git worktree remove` after merge.
- **One feature branch → many commits → one MR**. Never stack MRs (parent-merge auto-deletes the source branch and breaks dependent MRs). Never split one feature into sibling MRs.

### 4.2 Multi-Provider Dispatch
Workers are dispatched with `provider` + `model_id`. nexus-core translates to the correct CLI invocation. See `/hybrid-swarm` skill for routing strategy.

| provider | Backend | Constraint |
|----------|---------|------------|
| `claude` | `claude --agent <n> -p` | Claude Code session only |
| `opencode` | `opencode run --agent` | Any environment |
| `opencode-lite` | OpenCode Web API | Headless, no local tools |
| `gemini` | `gemini --agent <n> -p` | Any environment |
| `copilot` | `copilot --agent <n> -p` | GitHub Copilot CLI required |
| `hermes` | `hermes chat -q` | SOUL.md system prompt; no per-agent file |
| `ollama` | Ollama REST API | Local; zero API cost |

Recommended model routing:
- Bulk/atomic → `gemini` / `gemini-3.1-flash-lite-preview`
- Large context → `gemini` / `gemini-3.1-pro-preview`
- Pinpoint algorithm → `opencode` / `github-copilot/gpt-4.1`
- Claude-only tasks → `claude` / `claude-haiku-4-5-20251001`

**Default provider priority (quality-first)**: `claude` → `copilot` (if premium quota healthy) → `opencode`.
Full rules and quota gate: [wiki/protocols/Delegation-Provider-Priority.md](./wiki/protocols/Delegation-Provider-Priority.md).

## 5. Project Status & Roadmap (May 2026)

### 5.1 Current Status
- **Core Engine**: Stable (v0.32+). Middleware mode active.
- **Coverage**: ~30%. Critical gaps in agent-bus ordering and delegation error handling.
- **Portability**: Transitioning to platform-agnostic Git remotes. `wiki.git` is just git.

### 5.2 Roadmap (Stabilization Phase)
- **P1**: Increase test coverage to >50% for `nexus_core` and `agent_bus`.
- **P1**: Implement global cost/ceiling enforcement in `load_balancer`.
- **P2**: Automate "drift healing" for wiki-code divergence.
- **P3**: Adapt patterns to Medical AI pipelines (CBCTc, GANSURV).

Detailed source: [`wiki/reports/Status-Report-2026-05-08.md`](wiki/reports/Status-Report-2026-05-08.md).

## 6. Architecture Standards

- **NEXUS_ROOT**: Where tools are deployed (`~/.local/share/nexus`).
- **CWD = Identity**: Project ID, Redis prefix, port derived from CWD only.
- **REDIS_PREFIX**: `folder_name_hash(full_path)` — isolates projects sharing folder names.
- **ARTIFACTS**: Stored in `~/.local/share/nexus/artifacts/{project_id}/`. Override with `NEXUS_ARTIFACTS_DIR`. Project ID is `basename(cwd)_md5(cwd)[:6]`.

## 7. Execution Environment

- **Python**: miniconda3-latest — `/home/wxc151/.pyenv/versions/miniconda3-latest/bin/python`
- **Headless**: OSC 52 for clipboard. No xclip.

## 8. Mandatory Workflow (Universal Loop)

```
1. DISCOVER   nexus wiki query "<domain>"  → pull LTM spec
2. TASK       glab issue list / create     → anchor MTM+
3. DELEGATE   delegate(agent_name, provider, model_id, caller_id=my_id)
4. SIGNAL     agent_bus send → broadcast or DM
5. COLLECT    inbox(read) on TASK_COMPLETE → validate artifact
6. DISTILL    nexus wiki ingest / ikb create → push LTM / LTM+
```

### Pipeline Hand-off
- **Hub-and-Spoke** (recommended): `delegate(caller_id=my_id)` → TASK_COMPLETE in Nexus inbox → dispatch next stage. Nexus validates at each hop.
- **P2P** (low-latency): Worker sends `agent_bus send(target="mini-worker", message="HANDOFF: artifact=...")` directly. Use only when Nexus validation not needed.

## 9. Collaborative Scenarios

### Scenario A — Direct Edit
Nexus edits directly. No delegation. Trivial single-file changes only.

### Scenario B — Surgical Pipeline (Pair Programming)
Single file. Nexus → Mini-Worker → [Mini-Driver → Mini-Navigator → Mini-Refiner] → Nexus commit.
Karpathy roles: Driver=Simplicity, Navigator=Surgical, Refiner=Think-first (see §12).

### Scenario C — Swarm Branching
Multi-file. Feature branch → parallel Mini-Workers → MR delivery.

### Scenario D — Hybrid Swarm (Multi-Provider)
Large-scale or mixed-complexity. See `/hybrid-swarm` skill.
- Decompose into atomic subtasks → route each by complexity/cost
- Parallel dispatch (single message, multiple `delegate` calls)
- Artifacts in `~/.local/share/nexus/artifacts/{project_id}/{ts}_{task_id}/`
- Fan-in: `tasks(show_all=True)` → Nexus merges → single commit

## 10. Wiki Maintenance

| Command | Purpose | When |
|---------|---------|------|
| `nexus wiki ingest [--since <date>]` | Import raw sessions → `wiki/raw/sessions/` | Daily |
| `nexus wiki promote <file> [--category]` | Synthesize raw → permanent wiki entry | After durable decisions |
| `nexus wiki query "<term>"` | Semantic search across wiki | Before every task |
| `nexus wiki lint` | Fix dead links, purge noise | Before wiki commits |

Raw sessions: **3-day retention**. Purge immediately after synthesis.

## 11. Housekeeping

- Commit completed work units immediately. No dirty departures.
- Update parent meta-repo pointer when committing in submodules.
- `code/scripts/drift-heal.sh` batches Graphify drift findings → one GitLab Issue/day.
- `nexus doctor` runs Wiki State + Graphify Hooks health check.

## 12. Coding Discipline (Karpathy)

Full skill: `/karpathy-guidelines`. Summary:

| Step | Rule |
|------|------|
| **Think first** | State assumptions. Surface tradeoffs. Ask before implementing. |
| **Simplicity** | Minimum code that solves the problem. No speculative features. |
| **Surgical** | Touch only what the task requires. Match existing style. |
| **Goal-driven** | Define `verify:` per step. Loop until verified. |

When Nexus protocol and Karpathy conflict → Nexus protocol wins; surface the tradeoff.

## 13. Key Skills Reference

| Skill | Purpose |
|-------|---------|
| `/hybrid-swarm` | Multi-provider task splitting, pipeline patterns |
| `/agent-delegator` | Dispatch syntax, provider/model routing |
| `/agent-bus-protocol` | MTM signaling, inbox, hand-off |
| `/ikb-manager` | LTM+ — register repos, ingest docs, semantic search |
| `/wiki-navigator` | LTM — read/write GitLab wiki |
| `/glab-collaboration` | MTM+ — issue/MR management |
| `/karpathy-guidelines` | Coding discipline |

## 14. Guardrails

To prevent runaway pipelines and unbounded cost:

- **Step Limit**: Max 10 steps per pipeline (`NEXUS_MAX_STEPS=10` override). Conductor loops, recursive delegation, and verifier re-plan cycles all count toward this budget.
- **Cost Ceiling**: All `delegate()` calls SHOULD declare an expected token budget. The agent-delegator enforces a hard cutoff on overrun.
- **Loop Protection**: Mini-Verifier emits `HALT` when bounded retries are exhausted or semantic drift is detected between consecutive worker outputs. Orchestrators MUST treat `HALT` as terminal — no further re-plan.

---
*Nexus: Search in Wiki. Plan in GitLab. Signal in Bus. Delegate the Hands.*
