# Human Risk Reduction Report
### Reporting period: H1 2026 — two-vector method v1.0

> **SYNTHETIC DATA.** Every figure below was produced by `tools/generate_synthetic_data.py` from a fixed seed. The organisation described here does not exist. Nothing in this document derives from any client engagement, and none of it may be used as an industry benchmark.

*Regenerate with three commands — see README. Output is byte-identical on any machine.*

---

## 1. Executive summary

Exposure across the organisation is **not uniform**. Operations - Poland scores 80.0 against 8.5 for IT & Infrastructure — a factor of 9 on the corrected compound score. Spending the awareness budget evenly across the population would direct most of it at people who are not the problem.

**Operations - Poland carries the highest compound exposure (CES* 80.0, critical).** It combines a measured phish-prone rate of 28.0% with a reporting rate of only 3.8% and a mean age of 178 days on its worst technical findings. Neither vector alone would have put it first.

**Measurement covers 71.8% of people and 79.8% of known assets.** Coverage is worst precisely where the raw scores are highest, which means the true position of those units is very probably worse than the raw numbers say.

**The confidence correction does not change the ranking this period.** Coverage differences exist but are not large enough to reorder units.

## 2. Exposure ranking

`CES*` is the compound exposure score after correction for data confidence. It is an instrument for ordering work, not a measurement of anything in the world. Two units three points apart are not meaningfully different.

| # | Business unit | Crit | HRI | TRI | CES | CES* | Confidence | Band |
|---|---------------|------|-----|-----|-----|------|------------|------|
| 1 | Operations - Poland | 3 | 32.8 | 92.5 | 55.0 | **80.0** | 0.38 | critical |
| 2 | Operations - Site A | 4 | 31.1 | 79.4 | 49.7 | **61.6** | 0.61 | high |
| 3 | Operations - Site B | 3 | 27.4 | 74.7 | 45.3 | **54.0** | 0.68 | high |
| 4 | Sales & Marketing | 3 | 21.3 | 56.4 | 34.7 | **36.5** | 0.90 | moderate |
| 5 | Corporate - UK | 4 | 7.7 | 60.5 | 21.6 | **25.6** | 0.69 | low |
| 6 | R&D | 4 | 3.8 | 68.2 | 16.0 | **17.6** | 0.82 | low |
| 7 | Finance & Admin | 5 | 3.0 | 51.8 | 12.4 | **12.6** | 0.95 | low |
| 8 | IT & Infrastructure | 5 | 1.6 | 44.1 | 8.4 | **8.5** | 0.99 | low |

```
Operations - Poland      ######################......  80.0
Operations - Site A      #################...........  61.6
Operations - Site B      ###############.............  54.0
Sales & Marketing        ##########..................  36.5
Corporate - UK           #######.....................  25.6
R&D                      #####.......................  17.6
Finance & Admin          ####........................  12.6
IT & Infrastructure      ##..........................   8.5
```

## 3. The human vector in detail

| Business unit | Phish-prone | Reporting | Training gap | Click→credential | People measured |
|---------------|-------------|-----------|--------------|------------------|-----------------|
| Operations - Poland | 28.0% | 3.8% | 51.5% | 35.7% | 113 |
| Operations - Site A | 30.1% | 5.2% | 44.6% | 48.3% | 270 |
| Operations - Site B | 27.5% | 6.2% | 40.7% | 47.7% | 244 |
| Sales & Marketing | 24.9% | 8.1% | 31.3% | 46.3% | 258 |
| Corporate - UK | 15.9% | 14.1% | 20.7% | 55.6% | 110 |
| R&D | 14.6% | 19.2% | 22.1% | 45.6% | 202 |
| Finance & Admin | 17.2% | 21.0% | 9.5% | 44.2% | 139 |
| IT & Infrastructure | 9.5% | 41.1% | 4.7% | 46.1% | 100 |

Two readings deserve separating.

**Reporting rate is the operational metric, not the phish-prone rate.** A click produces an incident that somebody has to find. A report produces an incident that has already been found. Units below roughly 10% reporting have no human detection capability worth the name, whatever their click rate looks like.

**Click-to-credential conversion is a property of the lure.** It says how convincing the simulated message was, not how weak the population is. Comparing conversion across campaigns that used different templates is comparing two different experiments.

## 4. The technical vector in detail

| Business unit | Weighted severity | Mean age of critical findings | KEV findings | Assets measured |
|---------------|-------------------|-------------------------------|--------------|-----------------|
| Operations - Poland | 89.9 | 178 d | 21 | 263 |
| Operations - Site A | 86.1 | 115 d | 32 | 545 |
| Operations - Site B | 85.2 | 91 d | 23 | 465 |
| Sales & Marketing | 70.8 | 41 d | 7 | 404 |
| Corporate - UK | 75.2 | 47 d | 4 | 215 |
| R&D | 82.8 | 62 d | 13 | 289 |
| Finance & Admin | 66.7 | 31 d | 2 | 214 |
| IT & Infrastructure | 58.9 | 18 d | 0 | 159 |

Severity is read off the worst quartile of each estate, weighted by asset criticality. A mean over the whole estate would let a unit improve its score by owning more uninteresting machines.

## 5. Priority segments

**Operations - Poland** — 300 people, business criticality 3, CES* 80.0

- Reporting sits at 3.8%. The dominant gap is detection, not knowledge. Training content will not move this number; a one-click reporting path and a visible response to reports will.
- 51.5% of assigned training is outstanding. Check whether this is refusal or scheduling: shift workers without desk time do not fail training, they never get offered it.
- Critical findings are averaging 178 days. At that latency the technical vector is the constraint, and human-side improvement will not reduce compound exposure much.
- Confidence is 0.38. Before investing in remediation here, close the measurement gap — otherwise the next report cannot show whether anything worked.

**Operations - Site A** — 440 people, business criticality 4, CES* 61.6

- Reporting sits at 5.2%. The dominant gap is detection, not knowledge. Training content will not move this number; a one-click reporting path and a visible response to reports will.
- 44.6% of assigned training is outstanding. Check whether this is refusal or scheduling: shift workers without desk time do not fail training, they never get offered it.
- Critical findings are averaging 115 days. At that latency the technical vector is the constraint, and human-side improvement will not reduce compound exposure much.

**Operations - Site B** — 360 people, business criticality 3, CES* 54.0

- Reporting sits at 6.2%. The dominant gap is detection, not knowledge. Training content will not move this number; a one-click reporting path and a visible response to reports will.
- 40.7% of assigned training is outstanding. Check whether this is refusal or scheduling: shift workers without desk time do not fail training, they never get offered it.
- Critical findings are averaging 91 days. At that latency the technical vector is the constraint, and human-side improvement will not reduce compound exposure much.

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

Confidence is the smaller of the two coverage figures on each row. It is a proportion of the unit that was measured, not a statistical confidence: a unit at 0.40 had roughly six people in ten invisible to the measurement. The corrected score divides the raw score by (0.50 + 0.50 x confidence), so full coverage leaves the score untouched and zero coverage doubles it. Method: `docs/02-normalization-and-scoring.md`.

| Business unit | People measured | Person coverage | Asset coverage | Confidence |
|---------------|-----------------|-----------------|----------------|------------|
| Operations - Poland | 113 / 300 | 37.7% | 54.8% | 0.38 |
| Operations - Site A | 270 / 440 | 61.4% | 77.4% | 0.61 |
| Operations - Site B | 244 / 360 | 67.8% | 80.7% | 0.68 |
| Sales & Marketing | 258 / 280 | 92.1% | 90.2% | 0.90 |
| Corporate - UK | 110 / 160 | 68.8% | 84.0% | 0.69 |
| R&D | 202 / 220 | 91.8% | 82.1% | 0.82 |
| Finance & Admin | 139 / 140 | 99.3% | 95.5% | 0.95 |
| IT & Infrastructure | 100 / 100 | 100.0% | 99.4% | 0.99 |

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

