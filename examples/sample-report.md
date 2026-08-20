# Human Risk Reduction Report
### Reporting period: H1 2026 — two-vector method v1.0

> **SYNTHETIC DATA.** Every figure below was produced by `tools/generate_synthetic_data.py` from a fixed seed. The organisation described here does not exist. Nothing in this document derives from any client engagement, and none of it may be used as an industry benchmark.

*Generated 2026-08-20 — regenerate with three commands, see README.*

---

## 1. Executive summary

Exposure across the organisation is **not uniform**. Operations - Poland scores 82.2 against 6.5 for IT & Infrastructure — a factor of 13 on the corrected compound score. Spending the awareness budget evenly across the population would direct most of it at people who are not the problem.

**Operations - Poland carries the highest compound exposure (CES* 82.2, critical).** It combines a measured phish-prone rate of 32.9% with a reporting rate of only 3.3% and a mean age of 144 days on its worst technical findings. Neither vector alone would have put it first.

**Measurement covers 72.2% of people and 79.8% of known assets.** Coverage is worst precisely where the raw scores are highest, which means the true position of those units is very probably worse than the raw numbers say.

**The confidence correction does not change the ranking this period.** Coverage differences exist but are not large enough to reorder units.

## 2. Exposure ranking

`CES*` is the compound exposure score after correction for data confidence. It is an instrument for ordering work, not a measurement of anything in the world. Two units three points apart are not meaningfully different.

| # | Business unit | Crit | HRI | TRI | CES | CES* | Confidence | Band |
|---|---------------|------|-----|-----|-----|------|------------|------|
| 1 | Operations - Poland | 3 | 37.7 | 86.2 | 57.0 | **82.2** | 0.39 | critical |
| 2 | Operations - Site A | 4 | 31.8 | 78.5 | 50.0 | **63.7** | 0.57 | high |
| 3 | Operations - Site B | 3 | 27.1 | 73.0 | 44.5 | **52.6** | 0.69 | high |
| 4 | Sales & Marketing | 3 | 20.6 | 57.0 | 34.2 | **35.5** | 0.93 | moderate |
| 5 | Corporate - UK | 4 | 8.9 | 57.6 | 22.7 | **26.1** | 0.74 | low |
| 6 | Finance & Admin | 5 | 7.5 | 50.9 | 19.5 | **19.8** | 0.97 | low |
| 7 | R&D | 4 | 2.8 | 63.8 | 13.3 | **14.2** | 0.87 | low |
| 8 | IT & Infrastructure | 5 | 1.0 | 41.0 | 6.5 | **6.5** | 1.00 | low |

```
Operations - Poland      #######################.....  82.2
Operations - Site A      ##################..........  63.7
Operations - Site B      ###############.............  52.6
Sales & Marketing        ##########..................  35.5
Corporate - UK           #######.....................  26.1
Finance & Admin          ######......................  19.8
R&D                      ####........................  14.2
IT & Infrastructure      ##..........................   6.5
```

## 3. The human vector in detail

| Business unit | Phish-prone | Reporting | Training gap | Click→credential | People measured |
|---------------|-------------|-----------|--------------|------------------|-----------------|
| Operations - Poland | 32.9% | 3.3% | 55.4% | 43.7% | 116 |
| Operations - Site A | 29.9% | 4.3% | 45.4% | 47.5% | 251 |
| Operations - Site B | 28.6% | 6.6% | 38.4% | 45.9% | 249 |
| Sales & Marketing | 24.6% | 8.6% | 30.6% | 43.2% | 267 |
| Corporate - UK | 18.3% | 13.9% | 18.9% | 43.2% | 118 |
| Finance & Admin | 19.4% | 15.4% | 15.2% | 45.4% | 139 |
| R&D | 11.0% | 17.2% | 20.4% | 46.7% | 203 |
| IT & Infrastructure | 5.6% | 44.8% | 4.3% | 40.9% | 100 |

Two readings deserve separating.

**Reporting rate is the operational metric, not the phish-prone rate.** A click produces an incident that somebody has to find. A report produces an incident that has already been found. Units below roughly 10% reporting have no human detection capability worth the name, whatever their click rate looks like.

**Click-to-credential conversion is a property of the lure.** It says how convincing the simulated message was, not how weak the population is. Comparing conversion across campaigns that used different templates is comparing two different experiments.

## 4. The technical vector in detail

| Business unit | Weighted severity | Mean age of critical findings | KEV findings | Assets measured |
|---------------|-------------------|-------------------------------|--------------|-----------------|
| Operations - Poland | 88.9 | 144 d | 36 | 261 |
| Operations - Site A | 85.9 | 111 d | 35 | 520 |
| Operations - Site B | 83.5 | 87 d | 33 | 461 |
| Sales & Marketing | 73.5 | 34 d | 4 | 417 |
| Corporate - UK | 73.0 | 39 d | 4 | 211 |
| Finance & Admin | 67.7 | 21 d | 0 | 217 |
| R&D | 78.0 | 55 d | 7 | 307 |
| IT & Infrastructure | 54.5 | 18 d | 0 | 160 |

Severity is read off the worst quartile of each estate, weighted by asset criticality. A mean over the whole estate would let a unit improve its score by owning more uninteresting machines.

## 5. Priority segments

**Operations - Poland** — 300 people, business criticality 3, CES* 82.2

- Reporting sits at 3.3%. The dominant gap is detection, not knowledge. Training content will not move this number; a one-click reporting path and a visible response to reports will.
- 55.4% of assigned training is outstanding. Check whether this is refusal or scheduling: shift workers without desk time do not fail training, they never get offered it.
- Critical findings are averaging 144 days. At that latency the technical vector is the constraint, and human-side improvement will not reduce compound exposure much.
- Confidence is 0.39. Before investing in remediation here, close the measurement gap — otherwise the next report cannot show whether anything worked.

**Operations - Site A** — 440 people, business criticality 4, CES* 63.7

- Reporting sits at 4.3%. The dominant gap is detection, not knowledge. Training content will not move this number; a one-click reporting path and a visible response to reports will.
- 45.4% of assigned training is outstanding. Check whether this is refusal or scheduling: shift workers without desk time do not fail training, they never get offered it.
- Critical findings are averaging 111 days. At that latency the technical vector is the constraint, and human-side improvement will not reduce compound exposure much.
- Confidence is 0.57. Before investing in remediation here, close the measurement gap — otherwise the next report cannot show whether anything worked.

**Operations - Site B** — 360 people, business criticality 3, CES* 52.6

- Reporting sits at 6.6%. The dominant gap is detection, not knowledge. Training content will not move this number; a one-click reporting path and a visible response to reports will.
- 38.4% of assigned training is outstanding. Check whether this is refusal or scheduling: shift workers without desk time do not fail training, they never get offered it.

## 6. What this report does not tell you

*This section is mandatory. A report that only states findings invites the reader to trust the findings more than the data supports.*

- **Blast radius is not modelled.** The ranking orders units by their own exposure, not by what an attacker gains from reaching them. The lowest-scoring unit in this report is IT & Infrastructure, which is also the unit whose compromise would matter most. The model does not know that, and no reader should let the table decide that question.
- **Unit boundaries are an org chart, not a network topology.** The compound score assumes the human and technical vectors interact because they sit in the same box on a slide. Real lateral movement does not respect reporting lines.
- **Simulated phishing measures response to simulated phishing.** It is a proxy for susceptibility to real social engineering, and the correlation is assumed rather than demonstrated here.
- **Absent data is treated as bad news.** The confidence correction never lowers a score. This is a deliberate bias, not a neutral choice, and it will overstate units that are genuinely fine but unmeasured.
- **No causal claim is made.** Nothing here establishes that training caused a change in behaviour. Quarter-over-quarter movement is consistent with an intervention working and equally consistent with campaign difficulty having shifted.

## 7. Recommendations

*Every recommendation declares how it will be judged. A recommendation without a verification criterion is an opinion.*

**1. Instrument reporting before adding training content.** Priority: Operations - Poland, Operations - Site A, Operations - Site B. Effort: low, mostly configuration and internal communication. *Verified by:* reporting rate above 15% in the target units at the next campaign, measured on comparable templates.

**2. Close the measurement gap in low-confidence units.** Priority: units below 0.60 confidence. Effort: medium, depends on identity provisioning for non-desk populations. *Verified by:* coverage confidence above 0.80, at which point the corrected and raw scores converge and the ranking becomes trustworthy.

**3. Treat remediation latency as an awareness constraint.** Where critical findings age past 90 days, human-side work cannot reduce compound exposure on its own. *Verified by:* mean age of top-quartile critical findings falling below 90 days in Operations - Poland.

**4. Standardise campaign difficulty before reading any trend.** Template language, pretext family and send timing must be held constant, or period-over-period movement is uninterpretable. *Verified by:* a documented template ladder applied identically across units in the next two cycles.

---

## Appendix A — Method

Scoring formulas, weights and their rationale: `docs/02-normalization-and-scoring.md`. Data model and field mapping: `docs/01-data-model.md`. Regulatory mapping: `docs/04-nis2-article-20.md`.

## Appendix B — Coverage

| Business unit | People measured | Person coverage | Asset coverage | Confidence |
|---------------|-----------------|-----------------|----------------|------------|
| Operations - Poland | 116 / 300 | 38.7% | 54.4% | 0.39 |
| Operations - Site A | 251 / 440 | 57.0% | 73.9% | 0.57 |
| Operations - Site B | 249 / 360 | 69.2% | 80.0% | 0.69 |
| Sales & Marketing | 267 / 280 | 95.4% | 93.1% | 0.93 |
| Corporate - UK | 118 / 160 | 73.8% | 82.4% | 0.74 |
| Finance & Admin | 139 / 140 | 99.3% | 96.9% | 0.97 |
| R&D | 203 / 220 | 92.3% | 87.2% | 0.87 |
| IT & Infrastructure | 100 / 100 | 100.0% | 100.0% | 1.00 |

## Appendix C — Indicator glossary

| Indicator | Definition |
|-----------|------------|
| Phish-prone rate | Clicks divided by delivered simulated messages |
| Reporting rate | Reports divided by delivered simulated messages |
| Training gap | Assigned training not completed, as a share of assigned |
| Click→credential | Credential submissions divided by clicks |
| Weighted severity | Criticality-weighted detection score of the worst asset quartile |
| HRI | Human Risk Index, 0–100, higher is worse |
| TRI | Technical Risk Index, 0–100, higher is worse |
| CES | Compound Exposure Score, geometric mean of HRI and TRI |
| CES* | CES after correction for coverage confidence |

