# advisory-method

> A data-driven method for prioritizing cybersecurity risk by combining
> **human-risk** and **technical-vulnerability** signals into a single,
> business-readable view — so an organization knows the *few* things that,
> if fixed, reduce its real exposure the most.

**Status:** work in progress · **Scope:** method + reusable templates · **Examples:** synthetic / anonymized only

---

## The problem this solves

Most security reporting arrives in silos. The awareness team presents a
phishing report. The vulnerability team presents a scan report. Each is
accurate, and neither answers the only question leadership actually has:

> *"Given everything, where do we act first — and why there?"*

Two separate dashboards force the customer to do the integration in their
head. They usually can't, so prioritization defaults to whatever is loudest
(the latest CVE, the last incident, the noisiest vendor). Budget follows
noise instead of exposure.

This method removes the silo. It produces **one decision**, expressed in the
language of risk and cost, backed by the customer's own data.

## The idea, in one paragraph

It adapts Roger Grimes' *Data-Driven Computer Security Defense* to a concrete,
repeatable workflow. Grimes' thesis: a small number of root causes — chiefly
**social engineering** and **unpatched software** — drive the large majority
of real breaches, so defense should be guided by measured exposure rather than
by fear of the headline of the day. Those two root causes map directly onto two
measurable signals an organization usually already collects: human risk and
technical vulnerability. This repo turns that mapping into a method.

## The two vectors → the two data sources

| Root cause (Grimes)            | Signal           | Reference data source* |
|--------------------------------|------------------|------------------------|
| Social engineering (human)     | Human risk       | Security-awareness platform (e.g. KnowBe4) |
| Unpatched / vulnerable software| Technical risk   | Vulnerability management (e.g. Qualys VMDR) |

\* The method is grounded in KnowBe4 + Qualys because that is the reference
implementation, but the logic is vendor-neutral: any source that yields a
per-group human-risk score and a per-asset technical-risk score will work.

## The method in 6 steps

1. **Map the two vectors.** Pull a per-group human-risk signal and a per-asset
   technical-risk signal from the respective platforms (both expose APIs).
2. **Normalize to a common scale.** Bring both signals onto a comparable
   `0–100` scale, weighted by asset / business criticality.
3. **Aggregate by business unit.** Resolve users and assets to the same
   organizational unit, so each unit carries two scores: human and technical.
4. **Build the matrix.** Plot human risk (X) against technical risk (Y), with
   bubble size = business criticality. The top-right quadrant is the real
   exposure — where the two risks compound.
5. **Translate to business language.** State the result in exposure and cost:
   *"these N units concentrate ~X% of real exposure; fixing the patch backlog
   on these assets + targeted phishing training on these groups reduces
   exposure more than any other action per euro spent."*
6. **Track the trend.** Re-run quarterly. The movement of the matrix over time
   is the proof of advisory value — evidence that recommendations *moved the
   risk*, not just produced activity.

## What "good" output looks like

- A single **risk matrix** (human × technical, sized by criticality) the
  customer can read in thirty seconds.
- One **prioritization statement** in business terms (exposure %, euro, the
  top N units to act on first).
- A **quarter-over-quarter delta** that shows whether the risk actually moved.

Not a list of 4,000 critical vulnerabilities. Not a phishing click-rate in
isolation. A decision.

## Repository structure

```
advisory-method/
├── README.md
├── docs/
│   ├── 01-rationale.md            # why data-driven (Grimes, adapted to IT/EU)
│   ├── 02-data-model.md           # the two vectors → sources → fields
│   ├── 03-scoring.md              # normalization to 0–100, criticality weighting
│   ├── 04-matrix.md               # the human × technical matrix and its quadrants
│   ├── 05-business-translation.md # matrix → exposure / euro / report outline
│   └── 06-tracking.md             # quarterly cadence, proving the delta
├── templates/
│   ├── risk-matrix-template.xlsx
│   └── advisory-report-outline.md
├── examples/
│   └── worked-example-anonymized.md
└── scripts/
    ├── extract_knowbe4.py
    ├── extract_qualys.py
    └── build_matrix.py
```

## Scope, ethics, and data handling

- **Examples are synthetic or fully anonymized.** No customer data, asset
  names, or identifiable user information appears anywhere in this repository.
- The method is **decision-support**, not an automated control. A human
  advisor interprets the matrix and owns the recommendation.
- Designed for the **Italian / EU regulatory context** (NIS2, DORA, GDPR):
  prioritization output is meant to feed gap assessments and remediation
  roadmaps, not to replace them.

## Why this exists

Built as part of a deliberate move from security operations toward a
**security advisory** practice: the discipline of translating technical risk
into business decisions. The differentiator is access to *both* sides of the
data — human and technical — and the method to fuse them.

---

*Method inspired by Roger Grimes' data-driven defense work; this is an
independent, reusable formulation, not affiliated with or endorsed by any
vendor.*
