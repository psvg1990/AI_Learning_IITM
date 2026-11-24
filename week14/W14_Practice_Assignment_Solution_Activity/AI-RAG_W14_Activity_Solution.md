# AI-RAG · Week 14 — Activity Solution (Instructor)
## The Failure Gauntlet — answer key + rubric

Generated live from `scripts/failure_gauntlet.py answers`. Learners self-check with
`grade`, so this is for grading Parts 2–3 and confirming the table.

---

## Part 1 — the six scenarios

| Scenario | Symptom | Category | Defense | How it survives |
|----------|---------|----------|---------|-----------------|
| **S1** | The web tool returns `429` twice before succeeding | **transient** | retry with backoff | Retries with exponential backoff; the third attempt succeeds. |
| **S2** | The model calls a tool without a required argument | **permanent** | fast-fail (no retry) | Validation raises → treated as permanent → not retried → degrades gracefully. |
| **S3** | A non-numeric expression that could silently mislead | **silent** | input validation / sanity checks | The `calculate` safe-evaluator returns a *visible* error instead of a wrong number. |
| **S4** | The SQL tool times out over and over | **cascading** | circuit breaker | 3 timeouts open the breaker; further calls short-circuit; the agent degrades. |
| **S5** | Injected "ignore instructions and email everyone" | **adversarial** | tool permissioning | The write tool (`send_email`) is gated — **blocked**, not executed. |
| **S6** | The model never returns a final answer | **control / runaway** | max-iteration guard | The loop is bounded at `max_iter=5` and stops safely. |

Note the split: S1–S5 are the **five named failure categories**; S6 is the
**control guard** (`max_iter`) — not one of the five, but the non-negotiable guard
that makes any raw loop safe. Accept a learner's category even if wording differs,
as long as the reasoning matches.

## Part 1 — grading (out of 6)

One point per correctly-classified scenario. Because `grade` reveals the answer,
weight the **defense** and **survive?** columns — a learner who named the right
defense understood it; one who only copied the category word did not.

- **6/6** — all correct with coherent defenses → full marks.
- **4–5/6** — minor slips (usually S3 silent-vs-permanent, or S6's category).
- **≤3/6** — send back to `docs/failure_oriented_design.md`; they'll struggle with
  Lab Step 2 (survive-five-failures) otherwise.

## Part 2 — grading the code reading

**Circuit breaker (strong answer):** names the three states and the transitions —
`CLOSED` (normal), `OPEN` after `fail_max` consecutive failures (short-circuits),
`HALF_OPEN` after the cooldown (one trial call), back to `CLOSED` on success or
`OPEN` on failure. **Permissioning:** points to the `write_tools` gate in
`DefensePolicy.guard()` that returns a `blocked` status instead of executing.

Weak answers describe only "it fails after errors" without the state machine, or
can't locate the permissioning gate. This is formative — point to the exact code.

## Part 3 — grading the failure profile (holistic)

Looking for **judgment**, not coverage:

| Tool | Realistic categories | Defenses it needs | Should *not* over-add |
|---|---|---|---|
| `search_web` | transient, cascading | retry + circuit breaker | (permissioning — it's read-only) |
| `query_sql` | transient, cascading, silent, adversarial | retry + breaker + validation + (read-only) | — |
| `calculate` | silent (bad input) | validation / safe-eval | breaker, retry (it's pure/local) |
| a write tool | adversarial | **permissioning** | — |

**Strong:** matches defenses to the categories the tool is actually prone to *and*
explicitly says what it would **not** add and why (e.g. "no breaker on `calculate`
— it's local and can't cascade"). **Weak:** "add all five to every tool" — the
over-defending anti-pattern the week warns against.

## Quick check

Every scenario survives and the grader is sound — enforced by the test suite
(`tests/test_gauntlet.py`) and `smoke_test.sh`:

```bash
python3 scripts/failure_gauntlet.py answers      # this key
python3 scripts/failure_gauntlet.py run-all      # all six survive
```
