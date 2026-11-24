# AI-RAG · Week 14 Lab Guide (Notebooks)
## Raw Agent Loop + Failure-Oriented Design + Testing

W14 is the **peak-density week**, delivered as **two runnable notebooks**, one per day.
They contain the same code as the package modules, lifted verbatim into narrated cells so
you can run a cell, watch the agent survive a failure, and explain it. Everything runs
**fully offline** on a scripted mock LLM + a local SQLite side-DB — **no OpenAI/Tavily key
and no cost** anywhere.

| Notebook | Day | Covers |
|---|---|---|
| **`AI-RAG_W14_Notebook_1.ipynb`** — Raw Agent + Taxonomy | Day 1 | the mock LLM, the tools, the ~80-line ReAct agent, the max-iter guard, the 5-category taxonomy |
| **`AI-RAG_W14_Notebook_2.ipynb`** — Defenses, Testing & the Gauntlet | Day 2 | the five defenses, the hardened agent, the failure gauntlet, mocking the LLM (three levels of test) |

Each notebook is **self-contained**: setup builds the side-DB and writes the fixtures; NB2
re-establishes the mock LLM, tools, and raw agent from NB1.

---

## Before you start

```bash
jupyter lab            # or open the .ipynb in VS Code / Cursor
```

Only `pydantic` is needed (the setup cell installs it if missing). In each notebook:
**Kernel → Restart & Run All.** Every cell should go green. (They ship already-executed so
you can read the outputs first.)

To run the **live** path later: `pip install openai`, set `OPENAI_API_KEY`, and pass
`use_llm=True` to `build_agent` (the real `OpenAILLM` uses `gpt-5-mini`).

---

## Notebook 1 — Raw Agent + Taxonomy (Day 1)

Build it raw, then name the failures. Work the sections in order:

1. **The mock LLM** (`mock_llm.py`) — the agent talks to `llm.complete(messages, tools)`.
   `MockLLM` is deterministic (scripted or keyword-routing); the whole package runs on it,
   which is *why* it works with no key. (Mocking is the testing lesson — NB2.)
2. **The tools** — carried from W13 plus the new **write** tool `send_email` (which is why
   permissioning exists, NB2).
3. **The failure types** — the exception classes the loop catches (`TransientError` →
   retry, `PermanentError` → fast-fail): the taxonomy *in code*.
4. **The raw ReAct agent** (`raw_react.py`) — the ~80-line loop: reason → act → observe →
   repeat. Run it **bare** (no defenses) and read the trace.
5. **The `max_iter` guard** — give it a model that never finishes and watch the guard stop
   it safely (the gauntlet's control scenario, S6).
6. **The 5-category taxonomy** — transient · permanent · silent · cascading · adversarial,
   each with its defense. These return in W18/W22/W25.

**Checkpoint ✅** — all cells green; you can run the bare loop, explain why `max_iter` is
non-negotiable, and name each of the five failure categories.

---

## Notebook 2 — Defenses, Testing & the Gauntlet (Day 2)

Defend it, prove it survives, then test it:

1. **The five defenses** (`defenses.py`) — retry + backoff, fast-fail, validation, a
   hand-rolled **circuit breaker** (CLOSED/OPEN/HALF_OPEN), and **permissioning**. Each is
   demonstrated: a retry that succeeds after two 429s, the breaker opening after repeated
   failures, and permissioning **blocking** a write tool. `DefensePolicy.guard` returns
   `ok` / `degraded` / `blocked` and never raises.
2. **The hardened agent** — wrap the raw loop with the policy and run it; contrast with
   NB1's bare run (a write is now blocked, failures degrade gracefully).
3. **The failure gauntlet** (`failure_gauntlet.py`) — **the mandatory Activity**. `list`
   the scenarios, `run S4` (a repeated timeout → the breaker opens), `grade S4 cascading`,
   `run-all`. The framing: **six scenarios = five injected failures (one per category) +
   the runaway-loop guard.** `failure_survival_rate` counts the five failures (5/5); S6 is
   the guard firing, not a failure.
4. **Testing — mock the LLM, three levels** — **tests vs evals** (tests are deterministic,
   mock the LLM; evals are probabilistic, RAGAS). Three representative tests from the suite,
   lifted and run: **unit** (a tool), **integration** (the loop with a scripted mock LLM),
   **end-to-end** (the gauntlet).

**Checkpoint ✅** — each defense demo behaves; the gauntlet shows all six scenarios pass and
grades correctly; the three-level tests pass.

---

## Taking it to your own capstone

The notebooks demonstrate the mechanics; the lab is **your** agent (Lab Part B):

- **Step 1 — Wire the five defenses** through the `DefensePolicy` in *your* `raw_react.py`
  (plus the `max_iter` guard and SQL sanitisation). Every tool call goes through the policy.
- **Step 2 — Survive five injected failures.** Inject one per category into your agent and
  verify it survives (returns *something* reasonable, never crashes). Save each trace —
  **the five traces are portfolio-grade artifacts.**
- **Step 3 — Build a real test suite** — five tests, all **mocking the LLM** (unit,
  integration, max-iter fires, retry-then-fail).
- **Step 4 — KPI snapshot** (`failure_survival_rate`) **+ ADR update** (§8).

## Done when…

- [ ] Both notebooks: **Restart & Run All** → all cells green, no errors.
- [ ] You can classify all six gauntlet scenarios and name each defense.
- [ ] Your agent survives five injected failures with saved traces.
- [ ] Your test suite passes, mocking the LLM at all three levels.

## Notebook vs the suite

These notebooks are where you **see and explain** the agent surviving failures.
The same code is a **pytest suite** with a `smoke_test.sh` that gates every commit — the
notebook to understand it, the suite to run and enforce it. Next: **W15 — Agent Memory**
(calmer and conceptual: when memory helps, and when *not* to use it).
