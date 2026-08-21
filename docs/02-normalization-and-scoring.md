# 02 — Normalisation and scoring

Weights appear in exactly two places: this document and `tools/compute_exposure.py`.
If they ever disagree, the code is wrong and this document is the specification.

All three indices run 0–100 and higher is worse.

## Human Risk Index (HRI)

Three components, computed over the **in-scope** population only.

    s = phish_clicked / phish_sent            susceptibility
    r = phish_reported / phish_sent           resilience
    k = 1 - (training_completed / assigned)   knowledge gap

    positive = 0.55·s + 0.25·k
    credit   = min(0.55·r , 0.80·positive)
    HRI      = 100 · (positive - credit) / 0.80

### Why resilience carries the same weight as susceptibility

This is the load-bearing decision in the model, and it is the one worth
defending out loud.

Most awareness reporting treats the phish-prone rate as the headline and the
reporting rate as a secondary nicety. That ordering is backwards from an
operational standpoint. A click produces an incident somebody has to discover.
A report produces an incident that has already been discovered, by the cheapest
sensor in the organisation, before the payload had time to matter. Two units
with an identical 25% click rate are not in the same position if one reports at
30% and the other at 3%: the first has a working human detection layer and the
second has none.

So resilience enters with a negative sign and the same coefficient as
susceptibility. The marginal value of teaching someone to report equals the
marginal value of teaching them not to click.

### Why the credit is capped

Uncapped, a high reporting rate could drive HRI to exactly zero, and the
geometric mean would then annihilate the compound score — a unit with a serious
technical problem would rank last because its people report well. That is a
scoring artefact, not a finding.

There is also a substantive reason. Reporting does not undo a click. Where a
credential was submitted, the report arrives after the credential is already
gone; it shortens the response window but does not close it. Capping the credit
at 80% of the positive terms says: reporting is worth a great deal, and it is
not worth everything.

### Why the knowledge gap is weighted lowest

Course completion measures attendance, not capability. It is included because
an untouched training backlog is a real operational signal — usually about
scheduling rather than attitude — but weighting it like behaviour would let a
unit improve its score by clicking through modules.

## Technical Risk Index (TRI)

Computed over the **worst quartile** of each unit's in-scope assets, ranked by
`qds_max`.

    severity = Σ(qds_max · criticality) / (100 · Σ criticality)   over the top quartile
    latency  = min(mean_age_of_critical_findings / 180 , 1)

    TRI = 100 · (0.70·severity + 0.30·latency)

### Why the worst quartile and not the mean

A mean over the whole estate rewards fleet size. Add two hundred well-patched
print servers and the average improves while the exposed domain controller is
exactly where it was. Attackers do not sample the estate at random; they look
for the worst thing reachable. The statistic should look where they look.

### Why latency is a separate term

Severity says how bad the open findings are. Latency says how long that state
has been tolerated, which is a property of the organisation rather than of the
vulnerabilities. A unit that consistently closes criticals in three weeks is a
different risk from one that takes six months, even at identical severity.
Saturation at 180 days reflects that beyond roughly six months, further delay
carries no additional information — the process has already failed.

## Compound Exposure Score (CES)

    CES = √(HRI · TRI)

The geometric mean, not the arithmetic one. Compound exposure requires both
vectors to be present: a vulnerable estate operated by people who never fall
for anything is a technical problem, and a susceptible population sitting on a
hardened estate is a training problem. Neither is the compound case, and the
arithmetic mean would rank both alongside it. The geometric mean pulls hard
toward the smaller vector, which is the intended behaviour.

## Coverage Confidence and the corrected score

    CC   = min(person_coverage , asset_coverage)
    CES* = min(100 , CES / (0.50 + 0.50·CC))

At full coverage the correction is neutral. At zero coverage it doubles the
score. It never lowers one.

This asymmetry is deliberate and it is a bias, so it is stated rather than
hidden. Missing measurement is treated as bad news because in practice it
correlates with the conditions that produce risk: shift populations without
individual accounts, sites onboarded late, acquisitions never integrated. A
unit that is genuinely fine but unmeasured will be overstated by this rule, and
the remedy is to measure it, which is precisely the behaviour the rule is meant
to provoke.

`CC` uses the minimum rather than the mean of the two coverages because a
compound score cannot be more trustworthy than its weaker input.

### It is not a statistical confidence

The name collides with a term of art and the collision is worth stating
plainly. Coverage Confidence is **not** a confidence interval, a p-value, or
any statement about sampling uncertainty. It is a plain proportion: how much of
the unit was actually measured. It answers "how much of this unit did we look
at", not "how sure are we about the number".

Real statistical confidence appears elsewhere in this repository — the
period-over-period analysis in `docs/06` reports 95% intervals in the ordinary
sense. The two are unrelated. If you are reading a table and cannot tell which
is which: intervals are written in brackets and apply to changes; CC is a
single number between 0 and 1 and applies to a period.

### Worked example

Take Operations - Poland from the sample output.

    person coverage  0.377   (of its headcount, this share is enrolled)
    asset coverage   0.548   (of its known assets, this share is scanned)

    CC = min(0.377, 0.548) = 0.377

    HRI = 32.75   TRI = 92.51
    CES = sqrt(32.75 x 92.51) = 55.04

    denominator = 0.50 + 0.50 x 0.377 = 0.689
    CES* = 55.04 / 0.689 = 79.97

So a raw compound score of 55 is reported as 80. The unit did not become more
exposed; the score says that roughly six people in ten are invisible to the
measurement, and a number built on the visible four cannot be taken at face
value.

Two sanity checks on the arithmetic:

- At CC = 1.00 the denominator is 1.00 and CES* equals CES exactly. Full
  measurement, no correction.
- At CC = 0.00 the denominator is 0.50 and CES* is twice CES, capped at 100.
  That factor of two is the maximum penalty the model will apply, and it is
  chosen rather than derived — there is no theory behind it. It is large
  enough to move a unit up the ranking and small enough not to put every
  unmeasured unit at the top regardless of everything else.

Compare with IT & Infrastructure at CC 0.994: CES 8.43, CES* 8.46. Where
measurement is complete, the correction does essentially nothing, which is the
intended behaviour.

## Normalisation across periods

Scores are normalised against **fixed absolute bounds**, never against the
current period's own distribution. Percentile or z-score normalisation makes
period-over-period comparison meaningless: if every unit improves by ten points,
relative normalisation reports no change at all. The whole purpose of the
report is to answer whether the position moved, so the yardstick has to stay
still.

The consequence is that a first report will often place everything in the
middle of the range. That is correct behaviour, not a calibration failure.

## What the numbers are for

CES* orders work. It does not measure risk in any unit that means anything
outside this model, it does not convert to money, and it does not support
comparison against another organisation. Two units three points apart are
indistinguishable. Treat the score as a queue, and the queue as a proposal.
