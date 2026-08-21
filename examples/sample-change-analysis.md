# Change Analysis — period over period
### H1 2026 → H2 2026 — two-vector method v1.1

> **SYNTHETIC DATA.** Both periods were produced by `tools/generate_synthetic_data.py` from a fixed seed. The organisation does not exist and no client data is involved.

---

## 1. What this analysis does differently

Every figure below is computed on a **closed cohort** — the people measured in both periods — and every claim of attribution is tested against a **control arm** of units that received no intervention.

- Measured in H1 2026: 1436 people
- Measured in H2 2026: 1436 people
- **Closed cohort: 1304 people** (132 left, 132 joined)

Roughly 9% of the measured population turned over between periods. Any aggregate rate comparison silently attributes that churn to behaviour change.

## 2. The counterfactual

Units that received nothing still moved. That movement is the campaign drift every other number has to be judged against.

Rates are the mean of individual per-person rates — clicks divided by messages delivered to that person, averaged over the cohort. This is the quantity every test below operates on. A binary "clicked at least once" outcome saturates over a multi-message campaign and was rejected for that reason; the reasoning is in `docs/06-measuring-change.md`.

| Metric | Control arm, H1 2026 | Control arm, H2 2026 | Drift |
|--------|------------|------------|-------|
| Mean click rate per person | 20.7% | 15.9% | -4.8 pp |
| Mean report rate per person | 16.1% | 16.5% | +0.4 pp |

Control arm cohort: 722 people. A treated unit that improved by less than the drift did not improve at all.

## 3. Susceptibility — mean click rate per person

| Business unit | Arm | Cohort | H1 2026 | H2 2026 | Change | vs control | Change p | Reading |
|---------------|-----|--------|------|------|--------|------------|-----------|---------|
| Corporate - UK | treated | 99 | 16.4% | 13.6% | -2.8 pp | +1.9 pp [-3.4, +7.3] | 0.261 | no detectable change |
| Finance & Admin | control | 133 | 17.5% | 14.0% | -3.5 pp | — | 0.152 | no detectable change |
| IT & Infrastructure | control | 86 | 9.4% | 5.5% | -3.9 pp | — | 0.042 | moved (no intervention — this is the counterfactual) |
| Operations - Poland | control | 104 | 29.7% | 26.8% | -2.9 pp | — | 0.327 | no detectable change |
| Operations - Site A | treated | 246 | 29.9% | 20.3% | -9.7 pp | -4.9 pp [-9.2, -0.6] | 0.000 | attributable improvement (was an extreme in P1 — expect some regression to the mean) |
| Operations - Site B | control | 221 | 27.5% | 19.8% | -7.7 pp | — | 0.000 | moved (no intervention — this is the counterfactual) |
| R&D | control | 178 | 14.7% | 11.1% | -3.6 pp | — | 0.038 | moved (no intervention — this is the counterfactual) |
| Sales & Marketing | treated | 237 | 25.7% | 21.0% | -4.7 pp | +0.1 pp [-4.1, +4.3] | 0.013 | moved, but not beyond the control arm — attribute to campaign drift |

The bracketed figures are 95% confidence intervals on the difference-in-differences estimate. Where the interval spans zero, the unit's movement is not distinguishable from what happened to units that received nothing.

## 4. Resilience — mean report rate per person

| Business unit | Arm | H1 2026 | H2 2026 | Change | vs control | Change p | Reading |
|---------------|-----|------|------|--------|------------|-----------|---------|
| Corporate - UK | treated | 14.0% | 21.0% | +7.0 pp | +6.6 pp [+1.1, +12.0] | 0.008 | attributable improvement |
| Finance & Admin | control | 21.7% | 21.5% | -0.2 pp | — | 0.942 | no detectable change |
| IT & Infrastructure | control | 42.3% | 47.7% | +5.4 pp | — | 0.103 | no detectable change |
| Operations - Poland | control | 4.0% | 3.9% | -0.0 pp | — | 0.981 | no detectable change |
| Operations - Site A | treated | 5.1% | 10.4% | +5.3 pp | +4.9 pp [+1.9, +7.8] | 0.000 | attributable improvement (was an extreme in P1 — expect some regression to the mean) |
| Operations - Site B | control | 6.1% | 6.9% | +0.7 pp | — | 0.574 | no detectable change |
| R&D | control | 18.7% | 17.1% | -1.6 pp | — | 0.408 | no detectable change |
| Sales & Marketing | treated | 8.3% | 9.2% | +0.9 pp | +0.5 pp [-2.7, +3.6] | 0.501 | no detectable change |

## 5. Repeat clickers

Of the cohort members who clicked in the first period, how many clicked again. This is the most robust behavioural signal available: it is unaffected by turnover, and largely unaffected by campaign difficulty, because the same people faced both campaigns.

| Business unit | Clicked in H1 2026 | Clicked again | Persistence |
|---------------|------------|---------------|-------------|
| Corporate - UK | 51 | 24 | 47.1% |
| Finance & Admin | 69 | 29 | 42.0% |
| IT & Infrastructure | 30 | 7 | 23.3% |
| Operations - Poland | 76 | 49 | 64.5% |
| Operations - Site A | 178 | 102 | 57.3% |
| Operations - Site B | 151 | 93 | 61.6% |
| R&D | 79 | 33 | 41.8% |
| Sales & Marketing | 160 | 105 | 65.6% |

## 6. Cohort versus open population

The same units, measured both ways. Where the two disagree, the difference is turnover being read as behaviour change.

| Business unit | Cohort change | Open-population change | Discrepancy |
|---------------|---------------|------------------------|-------------|
| Corporate - UK | -2.8 pp | -8.6 pp | -5.7 pp ⚠ |
| Finance & Admin | -3.5 pp | -13.7 pp | -10.2 pp ⚠ |
| IT & Infrastructure | -3.9 pp | -12.0 pp | -8.1 pp ⚠ |
| Operations - Poland | -2.9 pp | -4.7 pp | -1.8 pp |
| Operations - Site A | -9.7 pp | -18.3 pp | -8.7 pp ⚠ |
| Operations - Site B | -7.7 pp | -8.3 pp | -0.5 pp |
| R&D | -3.6 pp | -5.4 pp | -1.9 pp |
| Sales & Marketing | -4.7 pp | -5.3 pp | -0.6 pp |

## 7. What this analysis still cannot tell you

- **The control arm was not randomised.** Units received or did not receive an intervention for operational reasons. If those reasons correlate with the propensity to improve, the estimate is biased and no amount of arithmetic fixes it.
- **Control units are not homogeneous.** Pooling them into one counterfactual assumes they drift together. Inspect their individual movements before trusting the pooled figure.
- **Two periods is the minimum, not a trend.** Two points define a line whether or not one exists. Three periods are the first at which a direction can be claimed.
- **Simulation response, not real-attack response.** Everything here measures behaviour under a simulated stimulus.
- **The technical vector is not compared.** This tool covers the human vector only. Remediation latency moves for reasons — staffing, maintenance windows, an acquisition — that this design does not attempt to isolate.
- **Statistical significance is not operational significance.** A detectable two-point improvement may be worth nothing. The question of whether it was worth the money is not a statistical one.

