# AI-RAG · Week 14 — Activity: The Failure Gauntlet

> **Mandatory hands-on · ~30–40 min · fully offline (no API key).**
> Six failures are injected into the agent, one at a time. Your job: watch it
> **survive** each, then **classify** the failure into the taxonomy and **name the
> defense** that saved it. This turns the 5-category taxonomy into a permanent
> diagnostic tool — which is the whole point of the week.

The taxonomy: **transient · permanent · silent · cascading · adversarial** (plus
the **control/runaway** guard). Reference: `docs/failure_oriented_design.md`.

---

## Part 1 — Run the six scenarios

For each: run it, read the trace, decide the category, then check yourself.

```bash
python3 scripts/failure_gauntlet.py list           # overview of all six
python3 scripts/failure_gauntlet.py run S1          # S1's trace + whether it survived
python3 scripts/failure_gauntlet.py grade S1 transient   # check → reveals the defense
```

**Fill in this table as you go** (this is your submission):

| Scenario | Symptom (one line) | Category | Defense that saved it | Did it survive? |
|----------|--------------------|----------|-----------------------|-----------------|
| S1 | | | | |
| S2 | | | | |
| S3 | | | | |
| S4 | | | | |
| S5 | | | | |
| S6 | | | | |

Confirm they all survive at once:

```bash
python3 scripts/failure_gauntlet.py run-all        # every scenario should show survived=True
```

## Part 2 — Read one defense in the code

Open `src/agents/defenses.py` and find the **circuit breaker**. In your own words
(2–3 sentences), describe its three states and what moves it between them
(`CLOSED → OPEN → HALF_OPEN → CLOSED`). Then find where `DefensePolicy.guard()`
**blocks a write tool** — that's the adversarial defense (permissioning).

## Part 3 — Apply it to your capstone

Pick **one** tool your capstone agent calls (e.g. `query_sql`, `search_web`, or your
own). Answer, in a few sentences:

- Which failure **categories** is this tool realistically prone to?
- Which **defenses** does it therefore need — and which does it *not* need?
  (Remember: don't over-defend. A read-only `calculate` doesn't need a breaker; a
  write tool must have permissioning.)

Then confirm the defense is actually wired for that tool in your `raw_react.py` /
`DefensePolicy`.

---

## What to submit

1. The completed **six-row gauntlet table** (Part 1).
2. Your **circuit-breaker description** + where permissioning blocks a write (Part 2).
3. Your **one-tool failure profile** — categories it's prone to and the matching
   defenses (Part 3).

## Done when…

- [ ] All six scenarios graded correct with `failure_gauntlet.py grade`.
- [ ] `run-all` shows every scenario `survived=True`.
- [ ] You can describe the breaker's three states from memory.
- [ ] You mapped one capstone tool to its failure categories and defenses.

*Why this matters:* Lab Step 2 asks you to inject five failures into **your own**
agent and survive them. This gauntlet is the pattern — once you can classify a
failure and name its defense, the lab (and W18, W22, W25) is just applying it.
