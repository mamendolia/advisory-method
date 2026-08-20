# advisory-method

A data-driven method for prioritising security awareness work by combining a
**human risk vector** with a **technical risk vector** into a single ranking of
business units — plus a working implementation that produces a directional
report from either synthetic or real data.

The problem it addresses is narrow and common. Most awareness programmes are
deployed uniformly across a workforce, report attendance rather than behaviour,
and cannot answer whether anything changed. This method spends the budget where
the measurement says the exposure is, and states plainly what the measurement
cannot support.

## Run it

No dependencies beyond the Python standard library.

```bash
python3 tools/generate_synthetic_data.py --users 2000 --outdir data/synthetic
python3 tools/compute_exposure.py
python3 tools/build_report.py
```

The seed is fixed, so every clone produces byte-identical output. That
reproducibility is how you can tell the data is synthetic — a disclaimer in a
README proves nothing, a fixed seed proves it.

Result: [`examples/sample-report.md`](examples/sample-report.md).

## The method in six steps

1. **Attribute** every person and every asset to a business unit, and record
   what could not be attributed instead of hiding it.
2. **Measure the human vector** — susceptibility, resilience, knowledge gap —
   over the enrolled population only.
3. **Measure the technical vector** — criticality-weighted severity over the
   worst asset quartile, plus remediation latency.
4. **Combine** the two into a compound exposure score using a geometric mean,
   so that only units exposed on both vectors rank at the top.
5. **Correct for data confidence**, inflating the score where coverage is thin,
   so that unmeasured populations cannot pass as safe ones.
6. **Recommend**, with a declared verification criterion attached to every
   recommendation.

## Two design decisions worth arguing about

**Reporting rate carries the same weight as click rate, with the opposite
sign.** A click creates an incident someone has to discover; a report creates
an incident that has already been discovered. Two units clicking at the same
rate are not in the same position if one reports at 30% and the other at 3%.
Most reporting treats the phish-prone rate as the headline and reporting as a
nicety, and that ordering is backwards. See
[`docs/02`](docs/02-normalization-and-scoring.md).

**Missing data raises the score, never lowers it.** A unit that is not measured
is not a unit with a clean record. The correction is a deliberate bias — it is
meant to make removing an awkward population from scope unattractive — and it
is disclosed rather than buried. See [`docs/05`](docs/05-limits.md).

## Repository layout

```
docs/
  01-data-model.md                 Sources, fields, the mapping layer, personal data handling
  02-normalization-and-scoring.md  Formulas, weights, and why each one is what it is
  03-segmentation-and-indicators.md The indicator hierarchy and how to segment a prioritised unit
  04-nis2-article-20.md            What this evidences under NIS2, and what it does not
  05-limits.md                     Known failure modes, including the unsolved ones
tools/
  generate_synthetic_data.py       Fixed-seed dataset with deliberately heterogeneous units
  compute_exposure.py              HRI, TRI, CES, coverage confidence
  build_report.py                  Scores to a directional report
templates/
  human-risk-reduction-report.md   The report structure, empty
examples/
  sample-report.md                 Generated output, regenerable in three commands
```

## Scope and honesty notes

- **All data in this repository is invented.** No client engagement, dataset or
  finding is reflected here in any form, anonymised or otherwise.
- **The weights are argued, not fitted.** There is no training set and no
  empirical calibration. Presenting this as a validated model would
  misrepresent it.
- **The score orders work.** It is not a measurement of risk in any external
  unit, it does not convert to money, and it does not support benchmarking
  between organisations.
- **Blast radius is not modelled**, which means the lowest-ranked unit in the
  sample output is also the one whose compromise would matter most. That is a
  known limit, discussed in `docs/05`, not an oversight.

## Intellectual debts

The two-vector framing owes its shape to Roger Grimes's data-driven defence
argument — that most security effort is spent disproportionately to how
attacks actually succeed. The knowledge–behaviour distinction that keeps
training completion weighted low draws on Perry Carpenter's work on why
knowing and doing come apart under pressure, and on the Carpenter/Roer security
culture dimensions. The treatment of susceptibility as a property of the lure
rather than of the person draws on Luca Allodi's empirical work on cognition in
social engineering.

None of these authors is responsible for what has been done with their ideas
here.

## Licence

MIT. See [`LICENSE`](LICENSE).

*Italian summary: [`README.it.md`](README.it.md)*
