# Human Risk Reduction Report — <organisation>
### Reporting period: <period> — two-vector method v1.0

> Classification: <internal / confidential>. Distribution list: <names>.
> Data sources and extraction dates: <awareness platform, date>; <vulnerability
> platform, date>.

---

## 1. Executive summary

*Three findings, no more. Each one a claim a decision maker could act on or
disagree with. Numbers only where they change the decision.*

- Finding 1 — the highest compound exposure and what makes it compound.
- Finding 2 — the state of measurement coverage, stated before anyone asks.
- Finding 3 — what changed since the last period, or an explicit statement
  that the periods are not comparable and why.

## 2. Exposure ranking

*Question answered: where does the work go first.*

| # | Business unit | Crit | HRI | TRI | CES | CES* | Confidence | Band |
|---|---------------|------|-----|-----|-----|------|------------|------|

State here that the score orders work and does not measure risk in any external
unit, and that units within a few points of each other are indistinguishable.

## 3. Human vector

*Question answered: how do these populations behave, not what do they know.*

| Business unit | Phish-prone | Reporting | Training gap | Click→credential | People measured |
|---------------|-------------|-----------|--------------|------------------|-----------------|

Separate the reading of susceptibility from the reading of resilience. Note
whether click-to-credential conversion reflects the lure rather than the
population.

## 4. Technical vector

*Question answered: what state is the estate in, where these people work.*

| Business unit | Weighted severity | Mean age of critical findings | KEV findings | Assets measured |
|---------------|-------------------|-------------------------------|--------------|-----------------|

## 5. Priority segments

*Question answered: on whom do we intervene, and why those.*

For each prioritised unit: population size, what the dominant gap is
(measurement, detection, concentration, workflow), and what that implies. Do
not recommend here; recommendations belong in §7 with their verification
criteria.

## 6. What this report does not tell you

***Mandatory section. Do not delete it, and do not shorten it to a sentence.***

- Limits of the data: coverage, proxies used, attribution fallbacks.
- Comparability: what changed in campaign design that affects the trend.
- What the model does not represent: consequence, reachability, privilege.
- Any deliberate bias in the scoring, stated as a bias.
- Anything the reader might reasonably infer that the data does not support.

## 7. Recommendations

*Question answered: what do we do, to whom, at what effort, and how will we
know whether it worked.*

For each recommendation:

**<n>. <Recommendation>.** Target: <units>. Effort: <low/medium/high, and what
drives it>. *Verified by:* <the specific indicator and threshold that will
settle the question at the next report>.

A recommendation without a verification criterion is an opinion. Do not ship
one.

---

## Appendix A — Method

Reference to the scoring documentation and the version of the method used.
State the weights in force for this period.

## Appendix B — Coverage

| Business unit | People measured | Person coverage | Asset coverage | Confidence |
|---------------|-----------------|-----------------|----------------|------------|

Units suppressed for small population size are listed here by name, with the
reason, rather than silently omitted.

## Appendix C — Indicator glossary

| Indicator | Definition |
|-----------|------------|
