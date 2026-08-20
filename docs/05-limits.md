# 05 — Known limits of the model

A method document that only argues for its own design is marketing. These are
the failure modes I know about, including the ones I have not solved.

## 1. Blast radius is not modelled

The model ranks units by their own exposure, never by what an attacker gains
from reaching them. In the reference run, IT & Infrastructure ranks last: it
clicks rarely, reports heavily, and patches fast. It is also the unit whose
compromise would end the discussion for the entire organisation.

The ranking is therefore correct about susceptibility and silent about
consequence. Any reader who treats the table as a priority list without
overlaying privilege and reachability will systematically underinvest in the
places that matter most.

I have not solved this because doing it properly requires attack-path data
that a two-vector method does not have. Multiplying by business criticality
was tried and rejected: it double-counts, since criticality already weights
the technical vector, and it produces a number that looks like consequence
modelling while being nothing of the kind.

## 2. Organisational units are not network topology

The compound score assumes the human and technical vectors interact because
they sit in the same box on an org chart. Real lateral movement follows trust
relationships, shared credentials and flat network segments, none of which
respect reporting lines. A unit can be compromised through a vector attributed
to a different unit entirely, and the model will never see it.

## 3. Simulated phishing is a proxy of unverified strength

The correlation between response to a simulation and response to a real
targeted attack is assumed here, not demonstrated. Simulations are
undifferentiated by design and lack the reconnaissance that makes real
spear-phishing effective. The direction of the bias is unknown: simulations
may overstate susceptibility, by training people to expect tests, or
understate it, by being less convincing than the real thing.

## 4. The confidence correction is a deliberate bias

It never lowers a score. A well-run unit that is simply not enrolled will be
overstated, possibly badly. The justification is behavioural rather than
statistical — it makes exclusion from scope unattractive — but it is a thumb
on the scale and it should be disclosed to any client, not buried in a
methodology appendix.

## 5. Weights are argued, not fitted

Every coefficient in this model was chosen by reasoning about what the
indicators mean, not derived from outcome data. There is no training set. The
0.55 on susceptibility and resilience could defensibly be 0.5 or 0.6, and the
ranking would shift slightly. Anyone presenting this as an empirically
calibrated model is misrepresenting it.

Calibrating properly would require linking scores to real incident outcomes
across many organisations over several periods. That dataset does not exist in
any form I have access to.

## 6. Small units are unstable

Below roughly fifty measured people, a handful of clicks moves the phish-prone
rate by several points and the unit jumps bands between periods for reasons
that are pure sampling noise. The suppression floor of ten people protects
privacy; it does not make units of thirty statistically meaningful.

## 7. The score invites false precision

CES* is reported to one decimal place, which is one decimal place more than
the model deserves. It is retained only so that ordering is deterministic. Any
reader who distinguishes 52.6 from 54.1 has been misled by the formatting, and
the report says so in §2 for that reason.
