# 03 — Segmentation and indicators

Scoring tells you which units to look at. Segmentation tells you what to do
once you are looking, and the two questions have different answers.

## The indicator hierarchy

Not all measurements are equally close to the outcome anyone cares about.
Ordered from weakest to strongest:

| Level | Indicator | What it actually evidences |
|-------|-----------|----------------------------|
| 1 | Training completion | Attendance |
| 2 | Quiz and assessment scores | Recall, shortly after exposure |
| 3 | Phish-prone rate | Behaviour under a simulated stimulus |
| 4 | Reporting rate | Behaviour that produces operational value |
| 5 | Time to first report | Detection latency of the human sensor |
| 6 | Real-incident outcomes | The thing itself |

Programmes report level 1 because it is easy to collect and comfortable to
present. The method weights levels 3 and 4 because they are the highest levels
routinely obtainable. Level 5 is obtainable and almost always ignored: the
interval between delivery and the first report is the single best predictor of
whether the human layer would have helped in a real event.

Level 6 exists but cannot be produced on demand, and any programme claiming a
causal link between its training and a fall in real incidents is claiming more
than its data supports.

## The knowledge–behaviour gap

The reason level 2 sits so low deserves stating plainly. People who can
correctly identify a phishing email in a quiz still click phishing emails under
time pressure, in a familiar interface, on a message that arrives at a
plausible moment. Knowing is not the constraint; acting on what you know while
busy is. A programme that measures knowledge and reports behaviour change is
measuring the wrong variable and will show improvement that does not exist.

This is why the model gives the training gap a coefficient of 0.25 and
behaviour 0.55.

## Segmenting a unit once it is prioritised

Four questions, in order. Each has a different intervention attached, and
getting the order wrong wastes the budget.

**1. Is the population measured at all?**
If coverage is below roughly 0.60, stop. Any intervention deployed now cannot
be evaluated, and the next report will not be able to say whether it worked.
Fix enrolment first. This is usually an identity and provisioning problem —
shift workers, plant floor accounts, contractors — not an awareness problem.

**2. Is there a reporting path, and does using it do anything visible?**
Below roughly 10% reporting, the gap is almost never knowledge. It is that
reporting is inconvenient, or that nobody has ever seen a consequence of
reporting. A one-click button and a visible acknowledgement move this number
faster than any content.

**3. Is the failure concentrated or diffuse?**
Concentrated failure — a small group accounting for most clicks — is a
targeted-coaching problem. Diffuse failure across the unit is a process
problem: something about how work arrives in that unit makes the lure
plausible. Finance approving invoices by email is not a population weakness,
it is a workflow that a lure can imitate.

**4. Does the lure family match the unit's real threat?**
A unit that never handles payments does not need invoice-fraud simulations.
Matching the pretext family to the unit's actual exposure is what separates a
programme from a compliance exercise.

## From segmentation to measurement

Segmenting correctly is what makes the next period's comparison meaningful. If
the intervention was matched to the unit and the lure family was matched to the
unit's real work, a change can be attributed to something specific. If a
generic programme was deployed uniformly, any change that appears is
uninterpretable, because there is nothing to attribute it to. The method for
testing attribution is in `docs/06-measuring-change.md`.

## Comparability rules

Period-over-period movement is meaningless unless campaign difficulty is held
constant. Three rules, all routinely broken:

- **Language must match the population.** An English-language template sent to
  an Italian-speaking site measures reading comprehension as much as
  susceptibility, and the result cannot be compared with a localised campaign
  the following quarter.
- **Pretext family must be declared and held.** Credential harvest, invoice
  fraud, internal authority and delivery notification produce systematically
  different rates. Changing family between periods changes the instrument.
- **Send timing must be stable.** Rates shift with day of week and hour. Monday
  at nine and Friday at four are different experiments.

Where any of these changed, the report says so and declines to draw a trend.
Declining to draw a trend is a finding, and it is more credible than a
confident line through incomparable points.

## The ceiling of awareness as a control

Some lures cannot be trained against. A credential-harvest message that
displays a legitimate-looking domain, arrives from an expected internal
function and asks for an action the recipient performs routinely will succeed
against a well-trained population at a rate that no amount of additional
content will meaningfully reduce.

When the data shows this, the honest recommendation is procedural and
technical, not educational: a declared policy that certain operations never
arrive by email link, and phishing-resistant authentication that makes a
harvested credential worthless. Saying so in a client report costs nothing and
buys the credibility to be believed on everything else.
