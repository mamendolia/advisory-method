# 04 — Mapping to NIS2 Article 20

This document exists because the most common question a security awareness
programme receives in the EU is no longer "does it work" but "does it satisfy
the obligation". Those are different questions and the method answers both,
separately.

## What the obligation actually says

NIS2 places the duty on management bodies, not on the security function.
Article 20 requires that management bodies approve the cybersecurity risk
management measures, oversee their implementation, and can be held
accountable for failures. It further requires that members of management
bodies follow training, and requires entities to offer similar training to
their employees on a regular basis.

Article 21(2)(g) then lists basic cyber hygiene practices and cybersecurity
training among the measures entities must have in place.

In Italy the transposition is D.Lgs. 138/2024, with ACN as the competent
authority.

Two consequences follow, and both are usually missed.

**The training obligation on management is separate from, and stricter than,
the one on staff.** A programme that enrols the whole workforce but not the
board has satisfied the weaker obligation and missed the stronger one.

**Oversight has to be evidenced.** Approving measures and overseeing their
implementation is not demonstrated by a completion percentage. It is
demonstrated by a decision record: what was reviewed, what was decided, on
what evidence.

## Where this method produces evidence

| Obligation | Evidence this method produces | Where |
|------------|-------------------------------|-------|
| Management approves risk measures | A ranked exposure position with declared method and stated limits, suitable for formal review | Report §1, §2 |
| Management oversees implementation | Recommendations each carrying an explicit verification criterion, re-evaluated each period | Report §7 |
| Regular training for employees | Coverage and completion by unit, with unmeasured population stated rather than omitted | Report Appendix B |
| Training for management bodies | Board and executive treated as a segment in their own right, scored like any other | Segmentation, doc 03 |
| Basic cyber hygiene, Art. 21(2)(g) | Behavioural indicators rather than attendance: phish-prone rate, reporting rate, detection latency | Report §3 |
| Risk-based approach | Prioritisation by measured exposure, with the reasoning for the ordering exposed | Doc 02 |

## What this method does not satisfy

Stating this is part of the point.

- It covers Article 21(2)(g) only in the training and hygiene limb. The other
  measures in Article 21 — incident handling, business continuity, supply
  chain, cryptography, access control — are outside its scope entirely.
- It produces no incident notification capability. Article 23 timelines are a
  separate obligation with separate machinery.
- It does not constitute a risk analysis under Article 21(2)(a). It measures
  one dimension of exposure across organisational units; that is an input to a
  risk analysis, not a substitute for one.
- Compliance is a legal determination. This method produces evidence that
  supports one, and nothing in this repository should be represented as an
  opinion on whether an entity is compliant.

## A note on the reporting incentive

There is a tension worth naming. A regime that holds management accountable
creates pressure to present favourable numbers. An awareness programme that
responds to that pressure — softening campaigns, reporting completion instead
of behaviour, excluding the worst populations from scope — will produce
excellent evidence of nothing.

The coverage confidence correction in this method exists partly as a defence
against exactly that: a unit removed from scope does not disappear from the
report, it appears with low confidence and an inflated score.
