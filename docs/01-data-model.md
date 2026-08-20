# 01 — Data model

The method joins two independent measurement systems onto a shared unit of
analysis. Everything else in the repository depends on this join being honest,
so it is documented before the scoring.

## The unit of analysis is the business unit

Not the person, not the asset. Three reasons.

Person-level exposure scores create a disciplinary artefact. Once a per-employee
risk number exists, someone eventually asks for the list of the worst
employees, and the awareness programme becomes a performance-management tool.
That destroys the reporting culture the programme is supposed to build: people
do not report incidents to a system that scores them.

Asset-level scores are already produced by the vulnerability platform and add
nothing.

The business unit is also the level at which someone can actually act. A unit
has a manager, a budget, a shift pattern and a technology estate. An
intervention can be assigned to it.

## Vector one — human risk

Source: an awareness platform of the KnowBe4 family. The fields the method
needs are deliberately few, because a method that needs twenty fields cannot be
reproduced on a different platform.

| Field | Type | Meaning |
|-------|------|---------|
| `person_id` | string | Pseudonymous identifier, never an email address |
| `unit_id` | string | Business unit the person belongs to |
| `in_scope` | 0/1 | Whether the person is enrolled in the platform at all |
| `phish_sent` | int | Simulated messages delivered in the period |
| `phish_clicked` | int | Messages where the link was followed |
| `phish_reported` | int | Messages reported through the declared channel |
| `credential_submitted` | int | Clicks that proceeded to submit credentials |
| `training_assigned` | int | Training modules assigned in the period |
| `training_completed` | int | Assigned modules completed in the period |

`in_scope` is the field most implementations forget. A person who was never
enrolled is not a person with a clean record — they are a person about whom
nothing is known. Collapsing those two states is the single most common way an
awareness dashboard lies.

## Vector two — technical risk

Source: a vulnerability management platform of the Qualys VMDR family.

| Field | Type | Meaning |
|-------|------|---------|
| `asset_id` | string | Pseudonymous asset identifier |
| `unit_id` | string | Business unit the asset is attributed to |
| `in_scope` | 0/1 | Whether the asset is actually scanned |
| `asset_criticality` | 1–5 | Business criticality of the asset |
| `qds_max` | 0–100 | Highest detection score currently open on the asset |
| `oldest_critical_age_days` | int | Age of the oldest open critical finding |
| `kev_count` | int | Open findings on the known-exploited catalogue |

## The mapping layer

Joining the two vectors requires attributing every person and every asset to a
unit. In practice this is where the method breaks, and there are only three
cases.

**Case 1 — clean attribution.** Identity provider group maps to a unit, asset
tag maps to the same unit. Roughly the estate that was built after someone
thought about this. Use it directly.

**Case 2 — partial attribution.** People map cleanly, assets do not, typically
because tagging follows network segments or acquisition history rather than
organisation. Attribute by primary user where the platform records one; fall
back to network segment ownership; record the fallback in the coverage
appendix. Never silently distribute unattributed assets pro rata — that
manufactures a technical vector out of nothing.

**Case 3 — no attribution.** Common in operational technology and in recently
acquired entities. Do not score the unit. Report it as unmeasured. An honest
gap is worth more than a fabricated number, and it is also the finding most
likely to get budget approved.

## Personal data

The method never needs to identify a person, so it never receives the means to.

- Identifiers are pseudonymised at export, before the data reaches any tool in
  this repository. The mapping table stays with the data controller.
- No free-text fields are ingested. Job titles, departments as typed by users
  and manager names are all dropped.
- Outputs are aggregated to unit level. Any unit with fewer than ten measured
  people is suppressed rather than reported, because at that size an aggregate
  is a description of individuals.
- Retention follows the client's awareness platform retention, and the derived
  scores are not kept longer than the source.

This is not only a GDPR position. A programme that is visibly incapable of
identifying individual clickers is a programme people will report incidents
to.

## Files produced

    data/synthetic/units.csv    unit_id, unit_name, headcount, business_criticality
    data/synthetic/people.csv   human vector, one row per person
    data/synthetic/assets.csv   technical vector, one row per asset
    data/scores.json            computed output, one record per unit
