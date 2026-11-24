# AI-RAG · Week 13 Lab Guide (Notebooks)
## Tool Calling, API Agents & Structured Data (Phase 3 Opener)

W13 is delivered as **two runnable notebooks**, one per day. They contain the same code
as the package modules, lifted verbatim into narrated cells so you can run a cell, watch
the agent pick a tool, and explain it. Both run **fully offline** — a deterministic
`StubRouter` + fixtures + a local SQLite side-DB — so there's **no OpenAI/Tavily key and
no cost** anywhere.

| Notebook | Day | Covers |
|---|---|---|
| **`AI-RAG_W13_Notebook_1.ipynb`** — Foundations & Tool Design | Day 1 | the tool interface, the agent loop, the four design principles, the tool-design clinic |
| **`AI-RAG_W13_Notebook_2.ipynb`** — The Three Tools, Build & Measure | Day 2 | search_web, query_sql (SQL safety rails), calculate, tool-selection accuracy |

Each notebook is **self-contained**: setup writes the offline data files and builds the
SQLite side-DB. Notebook 2 re-establishes the tools + agent from Notebook 1 so it runs on
its own.

---

## Before you start

```bash
jupyter lab            # or open the .ipynb in VS Code / Cursor
```

Only `pydantic` is needed (the setup cell installs it if missing). In each notebook:
**Kernel → Restart & Run All.** Every cell should go green. (They ship already-executed so
you can read the outputs first.)

To run the **live** path later: `pip install openai tavily-python`, set `OPENAI_API_KEY`
(and `TAVILY_API_KEY`), and pass `use_llm=True` to `build_agent` / `offline=False` to
`SearchWebTool`.

---

## Notebook 1 — Foundations & Tool Design (Day 1)

Phase 3's shift: **decide → call → observe → answer**. Work the sections in order:

1. **The tool interface** (`base.py`) — a tool is four things: a **name**, a typed
   **schema** (Pydantic), a model-facing **description**, and declared **idempotency**.
   One definition renders to **both** OpenAI and Anthropic schemas.
2. **A concrete tool** (`calculate.py`) — see it render to both providers from one
   definition, and run through the validating `call()`.
3. **The other two tools** (`query_sql`, `search_web`) — inlined so the loop can run;
   the deep dive is Notebook 2.
4. **The agent loop** (`router.py` + `three_tool_agent.py`) — run a query offline and
   watch the `StubRouter` pick a tool, run it, and answer. The loop is tiny and
   framework-free (LangGraph arrives in W16).
5. **The four principles** — name · schema · description · idempotency. The framing to
   hold: when the agent picks the wrong tool, the fix is **almost never a bigger model** —
   tool design is the **dominant lever** for reliability.
6. **The tool-design clinic** (`tool_clinic.py`) — the **mandatory Activity**. `list` the
   six broken tools, `run C1`, `grade C1 naming` (the grader reveals the principle), and
   `lint good` (the three reference tools pass every check). Diagnose all six.

**Checkpoint ✅** — all cells green; you can classify each broken tool's violated
principle before checking, and explain why the fix is the tool, not the model.

---

## Notebook 2 — The Three Tools, Build & Measure (Day 2)

1. **Prerequisites** — run setup + the re-established tools/agent (self-contained).
2. **Tool 1 — search_web** — reaches outside the corpus, but has cost/latency, so its
   description tells the model to prefer internal tools. Run it offline (fixtures).
3. **Tool 2 — query_sql (the SQL safety rails)** — the important one. Run it live: a
   `SELECT` is **allowed**, a `DELETE` is **DENIED and logged**, and the `audit_log` shows
   both. Read-only default + audit logging + denied writes. *(Mind PII & retention in what
   the audit log stores — W28 covers compliance.)*
4. **Tool 3 — calculate** — the clean four-principles example; evaluates arithmetic with
   no `eval`.
5. **Measure — tool-selection accuracy** (`selection_eval.py`) — the new **KPI #5**. Run
   the harness over the 15-question labelled set; read the overall + per-tool accuracy.
   Aim ≥ 80% — and if you're below that with the real model, the fix is almost always your
   tool **descriptions**, not the loop.

**Checkpoint ✅** — the SQL tool allows the SELECT and denies+logs the write; selection
accuracy is reported per tool.

---

## Taking it to your own capstone

The notebooks demonstrate the mechanics; the capstone is **your** agent:

- **Add your own tool** — subclass `Tool`, set the four fields well (run the clinic's
  `lint` on it), and register it in `default_tools`.
- **Wire the real router** — set `OPENAI_API_KEY` and use `build_agent(use_llm=True)`;
  the `LLMRouter` uses OpenAI function calling (`gpt-5-mini`).
- **Measure honestly** — run `selection_eval` against the real model; if a tool is
  mis-selected, fix its **description** first. That's KPI #5.
- **Keep SQL safe** — never expose raw write-SQL; writes are a **W18** topic behind
  injection defenses + a human-approval step.

## Done when…

- [ ] Both notebooks: **Restart & Run All** → all cells green, no errors.
- [ ] You can diagnose all six clinic tools and run `lint` on a tool of your own.
- [ ] The SQL tool allows a SELECT and denies+logs a write, with the audit trail visible.
- [ ] Tool-selection accuracy is measured (aim ≥ 80%) — KPI #5 is live.

## Notebook vs the package

These notebooks are where you **see and explain** the agent. The same code is
a pytest-tested package with a `smoke_test.sh` and the tool-selection harness — the
notebook to understand it, the package to run and gate it. Next: **W14** — the raw agent
loop and failure-oriented design.
