#!/usr/bin/env python3
"""
Turn the computed scores into a Human Risk Reduction Report.

The report is written for a decision maker, not for an analyst. Every section
answers a question that someone might actually ask in a steering committee,
and the section on what the data cannot support is mandatory rather than
optional.

Usage:
    python3 tools/build_report.py --scores data/scores.json --out examples/sample-report.md
"""

import argparse
import json
import os
from datetime import date

PERIOD = "H1 2026"


def bar(value, width=28):
    filled = int(round(width * value / 100))
    return "#" * filled + "." * (width - filled)


def priority_band(score):
    if score >= 70:
        return "critical"
    if score >= 50:
        return "high"
    if score >= 30:
        return "moderate"
    return "low"


def build(scores):
    units = scores["units"]
    ranked = sorted(units, key=lambda u: u["CES_corrected"], reverse=True)
    top = ranked[0]
    bottom = ranked[-1]
    total_people = sum(u["headcount"] for u in units)
    measured_people = sum(u["human"]["measured_people"] for u in units)
    measured_assets = sum(u["technical"]["measured_assets"] for u in units)
    total_assets = sum(
        round(u["technical"]["measured_assets"] / u["asset_coverage"]) for u in units
    )
    movers = [u for u in units if u["rank_raw"] != u["rank_corrected"]]

    lines = []
    add = lines.append

    add("# Human Risk Reduction Report")
    add(f"### Reporting period: {PERIOD} — two-vector method v1.0")
    add("")
    add("> **SYNTHETIC DATA.** Every figure below was produced by "
        "`tools/generate_synthetic_data.py` from a fixed seed. The organisation "
        "described here does not exist. Nothing in this document derives from "
        "any client engagement, and none of it may be used as an industry "
        "benchmark.")
    add("")
    add(f"*Generated {date.today().isoformat()} — regenerate with three commands, see README.*")
    add("")
    add("---")
    add("")

    # 1
    add("## 1. Executive summary")
    add("")
    spread = top["CES_corrected"] / bottom["CES_corrected"] if bottom["CES_corrected"] > 1 else None
    spread_text = (
        f"a factor of {spread:.0f}" if spread
        else "more than an order of magnitude"
    )
    add(f"Exposure across the organisation is **not uniform**. {top['unit_name']} "
        f"scores {top['CES_corrected']:.1f} against {bottom['CES_corrected']:.1f} "
        f"for {bottom['unit_name']} — {spread_text} on the corrected compound "
        f"score. Spending the awareness budget evenly across the population "
        f"would direct most of it at people who are not the problem.")
    add("")
    add(f"**{top['unit_name']} carries the highest compound exposure "
        f"(CES* {top['CES_corrected']:.1f}, {priority_band(top['CES_corrected'])}).** "
        f"It combines a measured phish-prone rate of "
        f"{top['human']['phish_prone_rate']:.1f}% with a reporting rate of only "
        f"{top['human']['report_rate']:.1f}% and a mean age of "
        f"{top['technical']['mean_age_critical_days']:.0f} days on its worst "
        f"technical findings. Neither vector alone would have put it first.")
    add("")
    add(f"**Measurement covers {100 * measured_people / total_people:.1f}% of people "
        f"and {100 * measured_assets / total_assets:.1f}% of known assets.** "
        f"Coverage is worst precisely where the raw scores are highest, which "
        f"means the true position of those units is very probably worse than "
        f"the raw numbers say.")
    add("")
    if movers:
        names = ", ".join(u["unit_name"] for u in movers)
        add(f"**Correcting for data confidence changes the ranking.** {names} "
            f"move once thin coverage is accounted for. Any unit whose position "
            f"depends on the correction should be read as a measurement finding "
            f"first and a risk finding second.")
    else:
        add("**The confidence correction does not change the ranking this period.** "
            "Coverage differences exist but are not large enough to reorder units.")
    add("")

    # 2
    add("## 2. Exposure ranking")
    add("")
    add("`CES*` is the compound exposure score after correction for data "
        "confidence. It is an instrument for ordering work, not a measurement of "
        "anything in the world. Two units three points apart are not "
        "meaningfully different.")
    add("")
    add("| # | Business unit | Crit | HRI | TRI | CES | CES* | Confidence | Band |")
    add("|---|---------------|------|-----|-----|-----|------|------------|------|")
    for u in ranked:
        add(f"| {u['rank_corrected']} | {u['unit_name']} | {u['business_criticality']} | "
            f"{u['HRI']:.1f} | {u['TRI']:.1f} | {u['CES']:.1f} | "
            f"**{u['CES_corrected']:.1f}** | {u['coverage_confidence']:.2f} | "
            f"{priority_band(u['CES_corrected'])} |")
    add("")
    add("```")
    for u in ranked:
        add(f"{u['unit_name']:<24} {bar(u['CES_corrected'])} {u['CES_corrected']:>5.1f}")
    add("```")
    add("")

    # 3
    add("## 3. The human vector in detail")
    add("")
    add("| Business unit | Phish-prone | Reporting | Training gap | Click→credential | People measured |")
    add("|---------------|-------------|-----------|--------------|------------------|-----------------|")
    for u in ranked:
        h = u["human"]
        add(f"| {u['unit_name']} | {h['phish_prone_rate']:.1f}% | "
            f"{h['report_rate']:.1f}% | {h['training_gap_rate']:.1f}% | "
            f"{h['credential_conversion_rate']:.1f}% | {h['measured_people']} |")
    add("")
    add("Two readings deserve separating.")
    add("")
    add("**Reporting rate is the operational metric, not the phish-prone rate.** "
        "A click produces an incident that somebody has to find. A report "
        "produces an incident that has already been found. Units below roughly "
        "10% reporting have no human detection capability worth the name, "
        "whatever their click rate looks like.")
    add("")
    add("**Click-to-credential conversion is a property of the lure.** It says "
        "how convincing the simulated message was, not how weak the population "
        "is. Comparing conversion across campaigns that used different templates "
        "is comparing two different experiments.")
    add("")

    # 4
    add("## 4. The technical vector in detail")
    add("")
    add("| Business unit | Weighted severity | Mean age of critical findings | KEV findings | Assets measured |")
    add("|---------------|-------------------|-------------------------------|--------------|-----------------|")
    for u in ranked:
        t = u["technical"]
        add(f"| {u['unit_name']} | {t['weighted_severity']:.1f} | "
            f"{t['mean_age_critical_days']:.0f} d | {t['kev_findings']} | "
            f"{t['measured_assets']} |")
    add("")
    add("Severity is read off the worst quartile of each estate, weighted by "
        "asset criticality. A mean over the whole estate would let a unit "
        "improve its score by owning more uninteresting machines.")
    add("")

    # 5
    add("## 5. Priority segments")
    add("")
    focus = ranked[:3]
    for u in focus:
        h, t = u["human"], u["technical"]
        add(f"**{u['unit_name']}** — {u['headcount']} people, business "
            f"criticality {u['business_criticality']}, CES* {u['CES_corrected']:.1f}")
        add("")
        if h["report_rate"] < 10:
            add(f"- Reporting sits at {h['report_rate']:.1f}%. The dominant gap is "
                f"detection, not knowledge. Training content will not move this "
                f"number; a one-click reporting path and a visible response to "
                f"reports will.")
        if h["training_gap_rate"] > 30:
            add(f"- {h['training_gap_rate']:.1f}% of assigned training is "
                f"outstanding. Check whether this is refusal or scheduling: "
                f"shift workers without desk time do not fail training, they "
                f"never get offered it.")
        if t["mean_age_critical_days"] > 90:
            add(f"- Critical findings are averaging "
                f"{t['mean_age_critical_days']:.0f} days. At that latency the "
                f"technical vector is the constraint, and human-side "
                f"improvement will not reduce compound exposure much.")
        if u["coverage_confidence"] < 0.6:
            add(f"- Confidence is {u['coverage_confidence']:.2f}. Before "
                f"investing in remediation here, close the measurement gap — "
                f"otherwise the next report cannot show whether anything worked.")
        add("")

    # 6
    add("## 6. What this report does not tell you")
    add("")
    add("*This section is mandatory. A report that only states findings invites "
        "the reader to trust the findings more than the data supports.*")
    add("")
    add("- **Blast radius is not modelled.** The ranking orders units by their "
        "own exposure, not by what an attacker gains from reaching them. The "
        "lowest-scoring unit in this report is IT & Infrastructure, which is "
        "also the unit whose compromise would matter most. The model does not "
        "know that, and no reader should let the table decide that question.")
    add("- **Unit boundaries are an org chart, not a network topology.** The "
        "compound score assumes the human and technical vectors interact "
        "because they sit in the same box on a slide. Real lateral movement "
        "does not respect reporting lines.")
    add("- **Simulated phishing measures response to simulated phishing.** It is "
        "a proxy for susceptibility to real social engineering, and the "
        "correlation is assumed rather than demonstrated here.")
    add("- **Absent data is treated as bad news.** The confidence correction "
        "never lowers a score. This is a deliberate bias, not a neutral choice, "
        "and it will overstate units that are genuinely fine but unmeasured.")
    add("- **No causal claim is made.** Nothing here establishes that training "
        "caused a change in behaviour. Quarter-over-quarter movement is "
        "consistent with an intervention working and equally consistent with "
        "campaign difficulty having shifted.")
    add("")

    # 7
    add("## 7. Recommendations")
    add("")
    add("*Every recommendation declares how it will be judged. A recommendation "
        "without a verification criterion is an opinion.*")
    add("")
    add(f"**1. Instrument reporting before adding training content.** Priority: "
        f"{', '.join(u['unit_name'] for u in ranked[:3])}. "
        f"Effort: low, mostly configuration and internal communication. "
        f"*Verified by:* reporting rate above 15% in the target units at the "
        f"next campaign, measured on comparable templates.")
    add("")
    add(f"**2. Close the measurement gap in low-confidence units.** Priority: "
        f"units below 0.60 confidence. Effort: medium, depends on identity "
        f"provisioning for non-desk populations. *Verified by:* coverage "
        f"confidence above 0.80, at which point the corrected and raw scores "
        f"converge and the ranking becomes trustworthy.")
    add("")
    add(f"**3. Treat remediation latency as an awareness constraint.** Where "
        f"critical findings age past 90 days, human-side work cannot reduce "
        f"compound exposure on its own. *Verified by:* mean age of top-quartile "
        f"critical findings falling below 90 days in "
        f"{ranked[0]['unit_name']}.")
    add("")
    add("**4. Standardise campaign difficulty before reading any trend.** "
        "Template language, pretext family and send timing must be held "
        "constant, or period-over-period movement is uninterpretable. "
        "*Verified by:* a documented template ladder applied identically across "
        "units in the next two cycles.")
    add("")
    add("---")
    add("")
    add("## Appendix A — Method")
    add("")
    add("Scoring formulas, weights and their rationale: "
        "`docs/02-normalization-and-scoring.md`. Data model and field mapping: "
        "`docs/01-data-model.md`. Regulatory mapping: "
        "`docs/04-nis2-article-20.md`.")
    add("")
    add("## Appendix B — Coverage")
    add("")
    add("| Business unit | People measured | Person coverage | Asset coverage | Confidence |")
    add("|---------------|-----------------|-----------------|----------------|------------|")
    for u in ranked:
        add(f"| {u['unit_name']} | {u['human']['measured_people']} / {u['headcount']} | "
            f"{100 * u['person_coverage']:.1f}% | {100 * u['asset_coverage']:.1f}% | "
            f"{u['coverage_confidence']:.2f} |")
    add("")
    add("## Appendix C — Indicator glossary")
    add("")
    add("| Indicator | Definition |")
    add("|-----------|------------|")
    add("| Phish-prone rate | Clicks divided by delivered simulated messages |")
    add("| Reporting rate | Reports divided by delivered simulated messages |")
    add("| Training gap | Assigned training not completed, as a share of assigned |")
    add("| Click→credential | Credential submissions divided by clicks |")
    add("| Weighted severity | Criticality-weighted detection score of the worst asset quartile |")
    add("| HRI | Human Risk Index, 0–100, higher is worse |")
    add("| TRI | Technical Risk Index, 0–100, higher is worse |")
    add("| CES | Compound Exposure Score, geometric mean of HRI and TRI |")
    add("| CES* | CES after correction for coverage confidence |")
    add("")

    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scores", default="data/scores.json")
    parser.add_argument("--out", default="examples/sample-report.md")
    args = parser.parse_args()

    with open(args.scores, encoding="utf-8") as handle:
        scores = json.load(handle)

    report = build(scores)
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as handle:
        handle.write(report)
    print(f"Report written to {args.out} ({len(report.splitlines())} lines)")


if __name__ == "__main__":
    main()
