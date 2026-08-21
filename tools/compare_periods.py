#!/usr/bin/env python3
"""
Compare two measurement periods and say what actually changed.

The question a client asks is "did it work". Answering it from two aggregate
click rates is wrong for four separate reasons, and this tool addresses each
one explicitly:

  Turnover        The population is not the same people. A rate can improve
                  because clickers left. Everything here is computed on a
                  CLOSED COHORT -- only people measured in both periods.

  Campaign drift  The second campaign may be easier or harder. Every unit then
                  moves together, for a reason that has nothing to do with any
                  intervention. Removed by DIFFERENCE-IN-DIFFERENCES against
                  units that received nothing.

  Sampling noise  On a unit of sixty people, three clicks is five points.
                  Tested with MCNEMAR, which is the correct test for paired
                  binary outcomes on the same individuals.

  Regression      The worst unit improves next period whether or not anyone
                  intervened, because it was an extreme. Flagged, not fixed.

Person-level binary outcomes are used rather than message-level rates: four
messages to one person are not four independent observations, and treating
them as such inflates significance.

Usage:
    python3 tools/compare_periods.py --p1 data/synthetic --p2 data/synthetic-p2 \
        --out examples/sample-change-analysis.md
"""

import argparse
import csv
import math
import os
from collections import defaultdict

ALPHA = 0.05
Z = 1.96  # two-sided 95%


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def normal_cdf(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def paired_t(deltas):
    """Test whether a unit's own mean change differs from zero.

    Each observation is one person's change between the two periods, so the
    pairing is inside the observation and a one-sample test is correct.

    An earlier version used McNemar on "clicked at least once". That was
    dropped: over four messages at a 30% propensity, three quarters of a unit
    clicks at least once, so the binary outcome saturates precisely where
    exposure is highest and stops discriminating. The reasoning is in
    docs/06-measuring-change.md.
    """
    mean, var, n = mean_var(deltas)
    if n < 2 or var == 0:
        return mean, 1.0
    se = math.sqrt(var / n)
    if se == 0:
        return mean, 1.0
    return mean, 2 * (1 - normal_cdf(abs(mean / se)))


def mean_var(values):
    n = len(values)
    if n < 2:
        return (values[0] if values else 0.0), 0.0, n
    mean = sum(values) / n
    var = sum((v - mean) ** 2 for v in values) / (n - 1)
    return mean, var, n


def welch_did(treated_deltas, control_deltas):
    """Difference-in-differences on per-person change, Welch two-sample test.

    Each observation is one person's own change between periods, so the pairing
    is already inside the observation. Comparing the treated mean change with
    the control mean change is then an ordinary two-sample problem with unequal
    variances -- which is what Welch handles.

    Returns (point_estimate, (lo, hi), p_value).
    """
    mt, vt, nt = mean_var(treated_deltas)
    mc, vc, nc = mean_var(control_deltas)
    if nt < 2 or nc < 2:
        return 0.0, (0.0, 0.0), 1.0
    se = math.sqrt(vt / nt + vc / nc)
    point = mt - mc
    if se == 0:
        return point, (point, point), 1.0
    t = point / se
    # Normal approximation: both arms are in the hundreds here, where the
    # t distribution and the normal are indistinguishable for this purpose.
    p = 2 * (1 - normal_cdf(abs(t)))
    return point, (point - Z * se, point + Z * se), p


def person_outcomes(rows):
    """Map person_id -> outcomes for measured people.

    Two representations are kept. The binary one ("did this person click at
    all") is what gets displayed, because it is what a reader understands. The
    per-person rate is what the statistics run on: the binary version saturates
    -- at four messages and a 30% propensity, three quarters of a unit clicks
    at least once, and the metric stops discriminating exactly where the
    problem is worst.
    """
    out = {}
    for r in rows:
        if r["in_scope"] != "1":
            continue
        sent = max(int(r["phish_sent"]), 1)
        out[r["person_id"]] = {
            "unit": r["unit_id"],
            "clicked": int(r["phish_clicked"]) > 0,
            "reported": int(r["phish_reported"]) > 0,
            "rate_clicked": int(r["phish_clicked"]) / sent,
            "rate_reported": int(r["phish_reported"]) / sent,
        }
    return out


def analyse(p1_people, p2_people, units):
    o1, o2 = person_outcomes(p1_people), person_outcomes(p2_people)
    cohort_ids = sorted(set(o1) & set(o2))

    arms = {u["unit_id"]: u["arm"] for u in units}
    names = {u["unit_id"]: u["unit_name"] for u in units}
    notes = {u["unit_id"]: u.get("intervention", "") for u in units}

    by_unit = defaultdict(list)
    for pid in cohort_ids:
        if o1[pid]["unit"] != o2[pid]["unit"]:
            continue  # internal transfer: neither unit owns this person's change
        by_unit[o1[pid]["unit"]].append(pid)

    def rates(pids, key):
        """Mean of the individual rates -- the quantity the tests operate on."""
        n = len(pids)
        if n == 0:
            return 0.0, 0.0
        field = "rate_" + key
        return (sum(o1[p][field] for p in pids) / n,
                sum(o2[p][field] for p in pids) / n)

    def deltas(pids, key):
        """One observation per person: that person's own change between periods."""
        field = "rate_" + key
        return [o2[p][field] - o1[p][field] for p in pids]

    # Pooled control arm, used as the counterfactual.
    control_ids = [p for u, pids in by_unit.items() if arms.get(u) == "control" for p in pids]
    ctrl = {}
    for key in ("clicked", "reported"):
        p1c, p2c = rates(control_ids, key)
        ctrl[key] = {"p1": p1c, "p2": p2c, "n": len(control_ids),
                     "delta": p2c - p1c, "deltas": deltas(control_ids, key)}

    # Regression-to-the-mean flag, computed per metric: a unit that was an
    # extreme on susceptibility is not necessarily an extreme on resilience,
    # and the warning only applies where the unit actually was one.
    extreme = {}
    for key, worst_is_high in (("clicked", True), ("reported", False)):
        p1_by_unit = {u: rates(pids, key)[0] for u, pids in by_unit.items()}
        ranked = sorted(p1_by_unit.items(), key=lambda kv: kv[1], reverse=worst_is_high)
        extreme[key] = {u for u, _ in ranked[:max(1, len(ranked) // 4)]}

    results = []
    for uid, pids in sorted(by_unit.items(), key=lambda kv: names[kv[0]]):
        row = {
            "unit_id": uid,
            "unit_name": names[uid],
            "arm": arms.get(uid, "control"),
            "intervention": notes.get(uid, ""),
            "cohort_n": len(pids),
            "extreme_in_p1": {k: uid in v for k, v in extreme.items()},
            "metrics": {},
        }
        for key in ("clicked", "reported"):
            p1r, p2r = rates(pids, key)
            unit_deltas = deltas(pids, key)
            delta, pval = paired_t(unit_deltas)

            if arms.get(uid) == "control":
                did_point = did_lo = did_hi = did_p = None
            else:
                # Control observations from this unit are excluded by
                # construction: a treated unit is never part of its own
                # counterfactual.
                did_point, (did_lo, did_hi), did_p = welch_did(
                    unit_deltas, ctrl[key]["deltas"]
                )

            row["metrics"][key] = {
                "p1": p1r, "p2": p2r, "delta": delta,
                "paired_p": pval,
                "did": did_point, "did_lo": did_lo, "did_hi": did_hi,
                "did_p": did_p,
                "did_significant": (did_lo is not None and (did_lo > 0 or did_hi < 0)),
            }

        # Repeat-click persistence: of those who clicked in P1, who clicked again.
        clicked_p1 = [p for p in pids if o1[p]["clicked"]]
        again = sum(1 for p in clicked_p1 if o2[p]["clicked"])
        row["repeat_clickers"] = {
            "base": len(clicked_p1),
            "again": again,
            "rate": again / len(clicked_p1) if clicked_p1 else 0.0,
        }
        results.append(row)

    # Open-population rates, for contrast with the cohort.
    def open_rate(rows_, key_field):
        measured = [r for r in rows_ if r["in_scope"] == "1"]
        by = defaultdict(lambda: [0, 0])
        for r in measured:
            e = by[r["unit_id"]]
            e[0] += 1
            e[1] += 1 if int(r[key_field]) > 0 else 0
        return {u: v[1] / v[0] for u, v in by.items() if v[0]}

    open_p1 = open_rate(p1_people, "phish_clicked")
    open_p2 = open_rate(p2_people, "phish_clicked")

    turnover = {
        "p1_measured": len(o1),
        "p2_measured": len(o2),
        "cohort": len(cohort_ids),
        "left": len(set(o1) - set(o2)),
        "joined": len(set(o2) - set(o1)),
    }
    return results, ctrl, turnover, open_p1, open_p2


def verdict(m, arm, extreme, lower_is_better):
    """Plain-language reading of one metric. Deliberately conservative.

    Direction is a property of the metric, not of the arithmetic: a fall in
    clicking is good, a fall in reporting is not.
    """
    if arm == "control":
        if m["paired_p"] < ALPHA:
            return "moved (no intervention — this is the counterfactual)"
        return "no detectable change"
    if not m["did_significant"]:
        if m["paired_p"] < ALPHA:
            return "moved, but not beyond the control arm — attribute to campaign drift"
        return "no detectable change"
    better = (m["did"] < 0) if lower_is_better else (m["did"] > 0)
    direction = "improvement" if better else "deterioration"
    caveat = " (was an extreme in P1 — expect some regression to the mean)" if extreme else ""
    return f"attributable {direction}{caveat}"


def build(results, ctrl, turnover, open_p1, open_p2, labels):
    lines = []
    add = lines.append
    pct = lambda x: f"{100 * x:.1f}%"
    pp = lambda x: f"{100 * x:+.1f} pp"

    add("# Change Analysis — period over period")
    add(f"### {labels[0]} → {labels[1]} — two-vector method v1.1")
    add("")
    add("> **SYNTHETIC DATA.** Both periods were produced by "
        "`tools/generate_synthetic_data.py` from a fixed seed. The organisation "
        "does not exist and no client data is involved.")
    add("")
    add("---")
    add("")

    add("## 1. What this analysis does differently")
    add("")
    add("Every figure below is computed on a **closed cohort** — the people "
        "measured in both periods — and every claim of attribution is tested "
        "against a **control arm** of units that received no intervention.")
    add("")
    add(f"- Measured in {labels[0]}: {turnover['p1_measured']} people")
    add(f"- Measured in {labels[1]}: {turnover['p2_measured']} people")
    add(f"- **Closed cohort: {turnover['cohort']} people** "
        f"({turnover['left']} left, {turnover['joined']} joined)")
    add("")
    add(f"Roughly {100 * turnover['left'] / max(turnover['p1_measured'], 1):.0f}% of "
        f"the measured population turned over between periods. Any aggregate "
        f"rate comparison silently attributes that churn to behaviour change.")
    add("")

    add("## 2. The counterfactual")
    add("")
    add("Units that received nothing still moved. That movement is the "
        "campaign drift every other number has to be judged against.")
    add("")
    add("Rates are the mean of individual per-person rates — clicks divided by "
        "messages delivered to that person, averaged over the cohort. This is "
        "the quantity every test below operates on. A binary "
        "\"clicked at least once\" outcome saturates over a multi-message "
        "campaign and was rejected for that reason; the reasoning is in "
        "`docs/06-measuring-change.md`.")
    add("")
    add("| Metric | Control arm, " + labels[0] + " | Control arm, " + labels[1] + " | Drift |")
    add("|--------|------------|------------|-------|")
    add(f"| Mean click rate per person | {pct(ctrl['clicked']['p1'])} | "
        f"{pct(ctrl['clicked']['p2'])} | {pp(ctrl['clicked']['delta'])} |")
    add(f"| Mean report rate per person | {pct(ctrl['reported']['p1'])} | "
        f"{pct(ctrl['reported']['p2'])} | {pp(ctrl['reported']['delta'])} |")
    add("")
    add(f"Control arm cohort: {ctrl['clicked']['n']} people. A treated unit that "
        f"improved by less than the drift did not improve at all.")
    add("")

    add("## 3. Susceptibility — mean click rate per person")
    add("")
    add("| Business unit | Arm | Cohort | " + labels[0] + " | " + labels[1] +
        " | Change | vs control | Change p | Reading |")
    add("|---------------|-----|--------|------|------|--------|------------|-----------|---------|")
    for r in results:
        m = r["metrics"]["clicked"]
        did = f"{100 * m['did']:+.1f} pp" if m["did"] is not None else "—"
        if m["did"] is not None:
            did += f" [{100 * m['did_lo']:+.1f}, {100 * m['did_hi']:+.1f}]"
        add(f"| {r['unit_name']} | {r['arm']} | {r['cohort_n']} | {pct(m['p1'])} | "
            f"{pct(m['p2'])} | {pp(m['delta'])} | {did} | {m['paired_p']:.3f} | "
            f"{verdict(m, r['arm'], r['extreme_in_p1']['clicked'], True)} |")
    add("")
    add("The bracketed figures are 95% confidence intervals on the "
        "difference-in-differences estimate. Where the interval spans zero, the "
        "unit's movement is not distinguishable from what happened to units "
        "that received nothing.")
    add("")

    add("## 4. Resilience — mean report rate per person")
    add("")
    add("| Business unit | Arm | " + labels[0] + " | " + labels[1] +
        " | Change | vs control | Change p | Reading |")
    add("|---------------|-----|------|------|--------|------------|-----------|---------|")
    for r in results:
        m = r["metrics"]["reported"]
        did = f"{100 * m['did']:+.1f} pp" if m["did"] is not None else "—"
        if m["did"] is not None:
            did += f" [{100 * m['did_lo']:+.1f}, {100 * m['did_hi']:+.1f}]"
        add(f"| {r['unit_name']} | {r['arm']} | {pct(m['p1'])} | {pct(m['p2'])} | "
            f"{pp(m['delta'])} | {did} | {m['paired_p']:.3f} | "
            f"{verdict(m, r['arm'], r['extreme_in_p1']['reported'], False)} |")
    add("")

    add("## 5. Repeat clickers")
    add("")
    add("Of the cohort members who clicked in the first period, how many "
        "clicked again. This is the most robust behavioural signal available: "
        "it is unaffected by turnover, and largely unaffected by campaign "
        "difficulty, because the same people faced both campaigns.")
    add("")
    add("| Business unit | Clicked in " + labels[0] + " | Clicked again | Persistence |")
    add("|---------------|------------|---------------|-------------|")
    for r in results:
        rc = r["repeat_clickers"]
        add(f"| {r['unit_name']} | {rc['base']} | {rc['again']} | {pct(rc['rate'])} |")
    add("")

    add("## 6. Cohort versus open population")
    add("")
    add("The same units, measured both ways. Where the two disagree, the "
        "difference is turnover being read as behaviour change.")
    add("")
    add("| Business unit | Cohort change | Open-population change | Discrepancy |")
    add("|---------------|---------------|------------------------|-------------|")
    for r in results:
        uid = r["unit_id"]
        cohort_delta = r["metrics"]["clicked"]["delta"]
        open_delta = open_p2.get(uid, 0) - open_p1.get(uid, 0)
        gap = open_delta - cohort_delta
        flag = " ⚠" if abs(gap) > 0.02 else ""
        add(f"| {r['unit_name']} | {pp(cohort_delta)} | {pp(open_delta)} | "
            f"{pp(gap)}{flag} |")
    add("")

    add("## 7. What this analysis still cannot tell you")
    add("")
    add("- **The control arm was not randomised.** Units received or did not "
        "receive an intervention for operational reasons. If those reasons "
        "correlate with the propensity to improve, the estimate is biased and "
        "no amount of arithmetic fixes it.")
    add("- **Control units are not homogeneous.** Pooling them into one "
        "counterfactual assumes they drift together. Inspect their individual "
        "movements before trusting the pooled figure.")
    add("- **Two periods is the minimum, not a trend.** Two points define a "
        "line whether or not one exists. Three periods are the first at which "
        "a direction can be claimed.")
    add("- **Simulation response, not real-attack response.** Everything here "
        "measures behaviour under a simulated stimulus.")
    add("- **The technical vector is not compared.** This tool covers the human "
        "vector only. Remediation latency moves for reasons — staffing, "
        "maintenance windows, an acquisition — that this design does not "
        "attempt to isolate.")
    add("- **Statistical significance is not operational significance.** A "
        "detectable two-point improvement may be worth nothing. The question "
        "of whether it was worth the money is not a statistical one.")
    add("")

    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--p1", default="data/synthetic")
    parser.add_argument("--p2", default="data/synthetic-p2")
    parser.add_argument("--labels", default="H1 2026,H2 2026")
    parser.add_argument("--out", default="examples/sample-change-analysis.md")
    args = parser.parse_args()

    p1_people = read_csv(os.path.join(args.p1, "people.csv"))
    p2_people = read_csv(os.path.join(args.p2, "people.csv"))
    units = read_csv(os.path.join(args.p1, "units.csv"))

    results, ctrl, turnover, open_p1, open_p2 = analyse(p1_people, p2_people, units)
    labels = [s.strip() for s in args.labels.split(",")]
    report = build(results, ctrl, turnover, open_p1, open_p2, labels)

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(report)

    print(f"Change analysis written to {args.out}")
    print(f"{'UNIT':<24}{'ARM':<9}{'CLICK Δ':>10}{'DiD':>10}{'SIGNIFICANT':>13}")
    for r in results:
        m = r["metrics"]["clicked"]
        did = f"{100 * m['did']:+.1f}" if m["did"] is not None else "—"
        print(f"{r['unit_name']:<24}{r['arm']:<9}{100 * m['delta']:>+9.1f}{did:>10}"
              f"{('yes' if m['did_significant'] else 'no'):>13}")


if __name__ == "__main__":
    main()
