# 03 — Scoring

Goal of this stage: turn the raw inputs from `02-data-model.md` into three
values per business unit —

- **H** — human risk, `0–100`
- **T** — technical risk, `0–100`
- **C** — business criticality, `1–5`

— that are *comparable to each other* and *stable across quarters*. The design
choices below are deliberate; the "why" matters more than the formulas, because
the choices are what make the output defensible to a skeptical customer.

---

## H — Human-risk score (0–100)

KnowBe4 already emits a 0–100 risk score, so H starts mostly done. Two refinements:

**Central tendency, membership-weighted.** When a BU spans several KnowBe4
groups, combine them by member count, not a flat average — a 5-person group and
a 500-person group should not weigh the same.

```
H_central = Σ(group_risk_score × member_count) / Σ(member_count)
```

**Keep the tail visible.** An average hides the dangerous minority — a handful
of high-risk users in a unit with payment or wire authority is a breach path the
mean washes out. So alongside H_central, carry a tail metric:

```
H_tail = share of users in the BU with risk_score ≥ 80   (a "%")
```

**Reported H** is `H_central`, but the tail travels with it and overrides the
narrative when it is high. *A BU at H_central 45 with 20% of users above 80 is
not a "medium" — it has a hot cluster, and the recommendation says so.* This is
the Grimes instinct applied to people: act on measured concentration of risk,
not on the comfortable average.

---

## T — Technical-risk score (0–100)

The raw input is per-asset TruRisk (`~0–1000`). Two decisions: how to roll
assets up to the BU, and how to land on 0–100.

### Roll-up: emphasize the worst critical assets, do not average

A plain mean dilutes. One crown-jewel server at TruRisk 950 surrounded by 200
low-risk endpoints must **not** average down to "fine." Aggregate with
criticality weighting and a tail emphasis:

```
T_raw(BU) = criticality-weighted aggregate of asset TruRisk,
            biased toward the high end
          ≈ weighted mean of the top-quartile assets by TruRisk,
            weights = ACS
```

In practice: take the BU's assets, weight each TruRisk by its `ACS (1–5)`,
and compute the weighted mean over the **top quartile** (or top-N) rather than
all assets. Crown jewels drive the score; a long tail of benign hosts cannot
hide them. (If Qualys tag-level TruRisk is available and assets are tagged by
BU, use it directly as `T_raw` and skip the manual roll-up.)

### Normalization: absolute, not relative

Two ways to reach 0–100:

- **Absolute** — fixed anchor (e.g. `T_raw / 10`, or fixed thresholds documented
  once). Same input always gives the same score.
- **Relative** — min–max across this quarter's BUs. Spreads BUs nicely across
  the matrix, but the scale *moves every quarter*.

**Use absolute as the primary.** Step 6 of the method is *prove the delta over
time* — that only works if a BU scoring 60 last quarter and 50 this quarter
genuinely improved, which relative normalization breaks. A relative view can be
shown as a secondary, single-quarter readability aid, clearly labeled.

```
T = clamp(T_raw / 10, 0, 100)        # first-cut absolute mapping; document your anchors
```

---

## C — Business criticality (1–5)

C is a **business judgment, set with the customer**, not a metric pulled from a
tool. It can be *informed* by the max asset ACS in the BU, but the final value
reflects revenue, regulatory exposure (is this BU in NIS2 / DORA scope?), and
data sensitivity. Keeping a human in the loop here is intentional: it preserves
the "decision-support, not automation" stance and gives the customer ownership
of the prioritization.

C becomes the **bubble size** on the matrix.

---

## Putting it together

Each BU is now a point: `(H, T)` with size `C`.

**The matrix is the headline.** Humans read quadrants in seconds; a single
fused number invites false precision and hides the *reason*. So the deliverable
leads with the plot (see `04-matrix.md`), and a score is used only to **sort the
action list**:

```
# Ranking key only — never the headline number.
# Product rewards "both high" (the compounding breach path Grimes describes):
# a BU high on one axis and low on the other ranks below one high on both.

E = (C / 5) × (H × T) / 100        # 0–100, used to order the priority list
```

`E` answers "which BU first?"; the matrix answers "why there?". They are shown
together, never one without the other.

---

## Worked micro-example (synthetic)

Three BUs, fully invented numbers:

| BU            | H_central | H_tail | T   | C | E (rank key) |
|---------------|-----------|--------|-----|---|--------------|
| Retail-North  | 72        | 24%    | 68  | 4 | 39.2         |
| Finance-HQ    | 58        | 31%    | 81  | 5 | 47.0         |
| Logistics-Ops | 44        | 9%     | 35  | 2 | 6.2          |

Reading it: **Finance-HQ ranks first** — not because either axis is the single
highest, but because both are high *and* it is the most business-critical, and
nearly a third of its users sit in the high-risk tail. The recommendation writes
itself: close the patch backlog on Finance-HQ's critical assets **and** run
targeted phishing/training on its high-risk cluster — that single coordinated
action removes more real exposure than anything else available. Logistics-Ops,
despite showing up on both scan and phishing reports, is correctly deprioritized.

That sentence — concrete, ranked, in business terms — is the entire point of the
method. `05-business-translation.md` turns it into the customer-facing report.

---

## Design decisions log

| Decision                              | Why |
|---------------------------------------|-----|
| Weighted mean + tail for H            | the average hides dangerous user clusters |
| Top-quartile, ACS-weighted roll-up    | crown jewels must not be diluted by benign hosts |
| Absolute normalization                | quarter-over-quarter trend must stay valid (step 6) |
| C set by human judgment               | criticality is a business call, not a tool output |
| Matrix as headline, `E` only to sort  | avoid false precision; keep the *reason* visible |
