# 06 — Measuring change over time

The single-period method answers *where is the exposure*. It does not answer
*did anything change*, which is the question a client asks second and cares
about more. This document covers the second question.

The short version: comparing two aggregate click rates is wrong four separate
ways, and each one has to be dealt with explicitly.

## Failure 1 — the population is not the same people

An aggregate rate compares two different populations. If the people who left
were disproportionately clickers, the rate improves without anyone having
changed their behaviour. At the turnover rates typical of operations and sales
functions, this alone can produce several points of apparent improvement per
year.

**Fix: a closed cohort.** Compute everything on the people measured in both
periods. Report the open-population rate alongside it, and where the two
disagree, that gap is turnover being read as learning.

People who moved between units are excluded rather than assigned. Neither unit
owns that person's change, and forcing an attribution introduces a bias whose
direction is unknowable.

## Failure 2 — campaign difficulty is a hidden variable

The second campaign may simply be easier to spot. When that happens every unit
improves together, and a programme that did nothing looks effective.

There is no reliable way to score template difficulty in the abstract. Attempts
to build a difficulty index from template attributes — sender plausibility,
urgency cues, brand imitation — are guesses dressed as measurement.

**Fix: a control arm.** Hold a set of units out of the intervention and use
their movement as the counterfactual. The estimate becomes a
difference-in-differences:

    effect = (treated_after − treated_before) − (control_after − control_before)

This is the load-bearing idea of the whole document. Without a control arm, no
attribution claim is defensible; with one, the campaign drift cancels because
it applies to both arms.

### On withholding training

The obvious objection is ethical: you cannot deny security training to a group
of employees to make your statistics cleaner.

Correct, and it is not necessary. Use **staggered rollout** instead. Every unit
receives the intervention; they receive it in a sequence dictated by the
exposure ranking. The units scheduled for a later wave are the control arm for
the earlier ones, they are not deprived of anything, and the ordering was going
to be needed anyway. The prioritisation output of the single-period method
doubles as the randomisation-free assignment mechanism for the longitudinal
one.

## Failure 3 — sampling noise looks like a trend

On a unit of sixty people, three clicks is five percentage points. Most
period-over-period movement in awareness reporting is noise reported as
achievement.

**Fix: test it, and use the right unit of observation.**

Four messages sent to one person are not four independent observations. People
who click once are markedly more likely to click again; treating messages as
independent inflates the sample size and produces significance where none
exists.

So every observation here is **one person's own change between periods**:

    delta_i = (clicks_i / sent_i)_after − (clicks_i / sent_i)_before

The pairing is inside the observation. A unit's own movement is then a
one-sample test against zero, and the comparison against the control arm is a
Welch two-sample test on unequal variances.

### Why not a binary outcome

An earlier version of the tool used "clicked at least once" with McNemar's
test, which is the textbook choice for paired binary data. It was dropped
because the outcome saturates: over four messages at a 30% propensity, roughly
three quarters of a unit clicks at least once. The metric loses discrimination
exactly where exposure is worst, and in testing it failed to detect an effect
that was present in the data by construction.

The binary version is still what gets described in prose, because "one in five
people clicked" is what a reader understands. It is not what the statistics
run on.

## Failure 4 — regression to the mean

The worst unit in any period will tend to improve in the next one whether or
not anyone intervened, because part of what made it worst was chance. Since
interventions are targeted at the worst units, this bias points directly at
the units whose improvement will be claimed as a result.

**Fix: no fix, only disclosure.** Units that were extremes in the first period
are flagged in the output. The control arm absorbs part of the effect, but only
part, because control units were by construction not extremes.

## The most robust signal available

**Repeat-click persistence**: of the cohort members who clicked in the first
period, the share who clicked again in the second.

It is unaffected by turnover, since it is defined on the cohort. It is largely
unaffected by campaign difficulty, since the same people faced both campaigns.
And it measures the thing that actually matters operationally — whether the
people who are susceptible are still susceptible — rather than an average that
a large compliant majority can carry.

## What the tool outputs

`tools/compare_periods.py` produces, per unit: cohort size, before and after
rates, own change with a p-value, difference-in-differences against the control
arm with a 95% interval, repeat-click persistence, and a plain-language reading
that is deliberately conservative. Three readings are possible for a treated
unit:

- **attributable improvement** — the interval excludes zero
- **moved, but not beyond the control arm** — real movement, campaign drift
- **no detectable change** — including cases where an effect exists but the
  unit is too small to detect it

The third reading is the one that gets programmes into trouble, because
"no detectable change" is routinely reported as "no change". A unit of a
hundred people cannot detect a three-point effect. That is a statement about
the measurement, not about the intervention.

## Minimum viable design for a client

1. Freeze template difficulty policy before the baseline period.
2. Rank units with the single-period method.
3. Schedule the intervention in waves; wave 2 and later are the control arm
   for wave 1.
4. Measure both periods with identical campaign parameters.
5. Run the comparison on the closed cohort.
6. Report attributable effects, drift, and undetectable cases separately.

Steps 1 and 3 have to be decided **before** the baseline. Retrofitting a
control arm after the fact is not possible, and this is the single most common
reason awareness programmes cannot demonstrate anything after three years of
operation.

## Limits

- Two periods is a comparison, not a trend. Three is the minimum for a
  direction.
- The control arm is not randomised. If the reason a unit was scheduled late
  correlates with its propensity to improve, the estimate is biased.
- Pooled control units are assumed to drift together. Inspect them
  individually before trusting the pooled counterfactual.
- Statistical significance is not operational significance, and neither is a
  return on investment.
- This module covers the human vector only. Remediation latency moves for
  reasons — staffing, maintenance windows, an acquisition — that this design
  does not isolate.
