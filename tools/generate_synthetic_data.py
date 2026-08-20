#!/usr/bin/env python3
"""
Generate a synthetic dataset for the two-vector advisory method.

Everything this script produces is invented. No client data is involved at any
point. The seed is fixed, so anyone who clones the repository and runs the
three tools in order obtains byte-identical files. That reproducibility is the
evidence that the data is synthetic -- a claim in a README is not.

Unit profiles are deliberately heterogeneous. A dataset where every business
unit behaves the same way cannot stress-test a scoring model: it produces a
flat ranking and hides exactly the failure modes the method is supposed to
surface.

Usage:
    python3 tools/generate_synthetic_data.py --users 2000 --outdir data/synthetic
"""

import argparse
import csv
import os
import random

SEED = 20260820

# ---------------------------------------------------------------------------
# Unit profiles
#
# Each tuple drives the probability distributions below:
#   share            fraction of the population assigned to the unit
#   criticality      business criticality of the unit, 1..5
#   ppp              baseline phish-prone probability
#   report           baseline probability that a recipient reports the phish
#   overdue          baseline probability that assigned training is overdue
#   qds              baseline Qualys-like detection score of its assets
#   mttr             mean time to remediate critical findings, in days
#   person_coverage  fraction of the headcount actually enrolled in the
#                    awareness platform
#   asset_coverage   fraction of known assets actually scanned
# ---------------------------------------------------------------------------
UNITS = [
    # unit_id,       name,                   share, crit, ppp,  report, overdue, qds, mttr, p_cov, a_cov
    ("SALES",        "Sales & Marketing",     0.14,   3, 0.24,  0.11,   0.31,    52,   41,  0.94,  0.91),
    ("FIN",          "Finance & Admin",       0.07,   5, 0.18,  0.22,   0.14,    47,   28,  0.99,  0.97),
    ("IT",           "IT & Infrastructure",   0.05,   5, 0.06,  0.48,   0.05,    38,   16,  1.00,  0.99),
    ("RND",          "R&D",                   0.11,   4, 0.13,  0.19,   0.22,    61,   57,  0.92,  0.86),
    ("OPS_IT_A",     "Operations - Site A",   0.22,   4, 0.29,  0.06,   0.44,    68,  121,  0.61,  0.74),
    ("OPS_IT_B",     "Operations - Site B",   0.18,   3, 0.26,  0.08,   0.38,    64,   96,  0.68,  0.79),
    ("OPS_PL",       "Operations - Poland",   0.15,   3, 0.33,  0.04,   0.52,    71,  164,  0.38,  0.55),
    ("CORP_UK",      "Corporate - UK",        0.08,   4, 0.16,  0.14,   0.19,    55,   49,  0.72,  0.83),
]

ASSETS_PER_HEAD = 1.6


def jitter(rng, base, spread):
    """Beta-ish jitter around a base rate, clamped to a sane interval."""
    value = rng.gauss(base, base * spread)
    return max(0.005, min(0.95, value))


def generate_people(rng, total_users):
    rows = []
    person_id = 0
    for unit_id, _, share, _, ppp, report, overdue, _, _, p_cov, _ in UNITS:
        headcount = max(1, round(total_users * share))
        for _ in range(headcount):
            person_id += 1
            in_scope = rng.random() < p_cov

            if not in_scope:
                # Not enrolled: no measurement exists for this person at all.
                rows.append({
                    "person_id": f"P{person_id:05d}",
                    "unit_id": unit_id,
                    "in_scope": 0,
                    "phish_sent": 0,
                    "phish_clicked": 0,
                    "phish_reported": 0,
                    "credential_submitted": 0,
                    "training_assigned": 0,
                    "training_completed": 0,
                })
                continue

            sent = rng.choice([3, 4, 4, 5])
            p_click = jitter(rng, ppp, 0.35)
            p_report = jitter(rng, report, 0.45)

            clicked = sum(1 for _ in range(sent) if rng.random() < p_click)
            # Reporting and clicking are not mutually exclusive across a
            # campaign series, but a person who clicked is markedly less
            # likely to also report that same message.
            reported = 0
            for i in range(sent):
                penalty = 0.35 if i < clicked else 1.0
                if rng.random() < p_report * penalty:
                    reported += 1

            # Credential submission is conditional on a click. The conversion
            # rate is a property of the lure, not of the population.
            submitted = sum(1 for _ in range(clicked) if rng.random() < 0.46)

            assigned = rng.choice([2, 3, 3, 4])
            p_overdue = jitter(rng, overdue, 0.30)
            completed = sum(1 for _ in range(assigned) if rng.random() > p_overdue)

            rows.append({
                "person_id": f"P{person_id:05d}",
                "unit_id": unit_id,
                "in_scope": 1,
                "phish_sent": sent,
                "phish_clicked": clicked,
                "phish_reported": reported,
                "credential_submitted": submitted,
                "training_assigned": assigned,
                "training_completed": completed,
            })
    return rows


def generate_assets(rng, total_users):
    rows = []
    asset_id = 0
    for unit_id, _, share, crit, _, _, _, qds, mttr, _, a_cov in UNITS:
        headcount = max(1, round(total_users * share))
        count = max(1, round(headcount * ASSETS_PER_HEAD))
        for _ in range(count):
            asset_id += 1
            in_scope = rng.random() < a_cov

            if not in_scope:
                rows.append({
                    "asset_id": f"A{asset_id:05d}",
                    "unit_id": unit_id,
                    "in_scope": 0,
                    "asset_criticality": 0,
                    "qds_max": 0,
                    "oldest_critical_age_days": 0,
                    "kev_count": 0,
                })
                continue

            # Asset criticality varies inside a unit; the unit profile only
            # shifts the centre of the distribution.
            asset_crit = max(1, min(5, round(rng.gauss(crit, 0.9))))
            qds_max = max(0, min(100, round(rng.gauss(qds, 16))))
            age = max(0, round(rng.expovariate(1 / mttr)))
            kev = 0
            if qds_max > 80 and rng.random() < 0.28:
                kev = rng.choice([1, 1, 2])

            rows.append({
                "asset_id": f"A{asset_id:05d}",
                "unit_id": unit_id,
                "in_scope": 1,
                "asset_criticality": asset_crit,
                "qds_max": qds_max,
                "oldest_critical_age_days": age,
                "kev_count": kev,
            })
    return rows


def generate_units(total_users):
    rows = []
    for unit_id, name, share, crit, *_ in UNITS:
        rows.append({
            "unit_id": unit_id,
            "unit_name": name,
            "headcount": max(1, round(total_users * share)),
            "business_criticality": crit,
        })
    return rows


def write_csv(path, rows):
    if not rows:
        raise ValueError(f"refusing to write an empty file: {path}")
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"  {path}  ({len(rows)} rows)")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--users", type=int, default=2000)
    parser.add_argument("--outdir", default="data/synthetic")
    args = parser.parse_args()

    rng = random.Random(SEED)
    os.makedirs(args.outdir, exist_ok=True)

    print(f"Generating synthetic dataset (seed {SEED}, {args.users} users)")
    write_csv(os.path.join(args.outdir, "units.csv"), generate_units(args.users))
    write_csv(os.path.join(args.outdir, "people.csv"), generate_people(rng, args.users))
    write_csv(os.path.join(args.outdir, "assets.csv"), generate_assets(rng, args.users))
    print("Done. This data is invented and must never be used as an industry benchmark.")


if __name__ == "__main__":
    main()
