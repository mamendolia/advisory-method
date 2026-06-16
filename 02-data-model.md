# 02 — Data Model

The method needs exactly **two numbers per business unit**: a human-risk score
and a technical-risk score. Everything in this file exists to produce the raw
inputs for those two numbers cleanly and reproducibly.

## Unit of analysis: the business unit (BU)

The matrix is read at the **business-unit** level — not per user, not per asset.
A BU is whatever organizational slice the customer makes decisions about
(a store cluster, a department, a subsidiary, a function). Users and assets are
the raw material; the BU is where prioritization happens and where budget is
allocated.

This means every record we pull must be resolvable to a BU. That resolution is
the **mapping layer** (last section) — and it is the single biggest determinant
of how much work the method is in a given environment.

---

## Vector A — Human risk (KnowBe4)

KnowBe4 already computes a per-user and per-group **Risk Score (0–100, higher =
riskier)**, so most of the human side is solved at the source. We pull, not
recompute.

**User-level fields** (KMSAT / Reporting API):

| Field                 | Use                                              | Note |
|-----------------------|--------------------------------------------------|------|
| `user_id`             | join key                                         | internal id, not PII |
| `email` / `name`      | mapping to BU only                               | **PII — minimize, hash if exported** |
| `groups[]`            | BU resolution                                    | the link to the mapping layer |
| `current_risk_score`  | human-risk input (0–100)                         | the core signal |
| `phish_prone`         | tail / context                                   | recent failure flag |
| `training_status`     | context for recommendations                      | completed / overdue |

**Group-level fields** (already aggregated by KnowBe4):

| Field                       | Use                                  |
|-----------------------------|--------------------------------------|
| `group_name`                | BU resolution                        |
| `member_count`              | weighting when re-aggregating        |
| `group_risk_score` (0–100)  | human-risk input if group == BU      |
| `phish_prone_percentage`    | tail metric at group level           |

> **PII handling:** email/name leave the platform only to resolve BU membership,
> then are dropped. No example or committed artifact in this repo ever contains
> real identities (see README → data handling).

---

## Vector B — Technical risk (Qualys VMDR / TruRisk)

Qualys also pre-aggregates: it scores vulnerabilities, rolls them up to assets,
and can roll assets up to tags. The method rides that hierarchy.

> Ranges below reflect the TruRisk model; **confirm the exact ranges/field
> names in your own tenant and VMDR version**, as they shift between releases.

| Level          | Field                              | Typical range | Use |
|----------------|------------------------------------|---------------|-----|
| Vulnerability  | `QDS` (Qualys Detection Score)     | 1–100         | severity + threat intel (exploit, malware) |
| Asset          | `ACS` (Asset Criticality Score)    | 1–5           | business criticality of the asset |
| Asset          | `TruRisk` asset score              | ~0–1000       | per-asset roll-up of its vulns × criticality |
| Tag / group    | `TruRisk` tag score                | ~0–1000       | per-tag roll-up — **this is the BU score if assets are tagged by BU** |

**The key consequence:** if assets are tagged by business unit in Qualys, the
per-BU technical input already exists as the tag-level TruRisk score — one API
call. If not, we aggregate asset TruRisk scores to BU ourselves (see
`03-scoring.md`). The QDS-per-vulnerability detail is kept for the *narrative*
("the exposure on this BU is driven by N internet-facing assets with actively
exploited CVEs"), not for the score itself.

---

## The mapping layer (groups / tags → business unit)

Both vectors must land on the same BU labels. Three cases, in increasing order
of effort:

1. **Identity** — KnowBe4 groups *are* the BUs and Qualys assets are tagged with
   the same BUs. The mapping is a no-op. *(Goal state.)*
2. **Rename** — the slices exist on both sides but under different names. A
   static lookup table (`group_name` → `BU`, `tag` → `BU`) resolves it.
3. **Reconstruct** — one side has no BU concept (e.g. assets untagged, or
   KnowBe4 groups are functional not organizational). Here the mapping must be
   built once, with the customer, and maintained. This is real work and should
   be surfaced as a finding in itself ("you cannot currently see risk by
   business unit — that is a gap").

The mapping layer is intentionally explicit and version-controlled, because a
silent mismatch here invalidates the whole matrix.

**Output of this stage:** one tidy table, one row per BU, carrying the raw
human inputs (user/group risk scores) and raw technical inputs (asset/tag
TruRisk, ACS). `03-scoring.md` turns that into `(H, T, C)`.

---

### Environment checklist (fill in per engagement)

- [ ] Do KnowBe4 groups correspond to business units? *(identity / rename / reconstruct)*
- [ ] Are Qualys assets tagged by business unit? *(yes → tag TruRisk; no → asset roll-up)*
- [ ] Is `ACS` set deliberately per asset, or left at default? *(affects weighting trust)*
- [ ] Confirm TruRisk score ranges and field names in this tenant/version.
