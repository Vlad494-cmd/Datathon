# EcoSpark Executive Summary — Report Feedback & Recommendations

Review conducted 2026-04-21 against IE-Iberdrola_Datathon_Marzo_2026.md.
Canonical FV figures: **87 stations · 502 chargers · 75,300 kW · 327,883 EVs**.

---

## 1. Disqualification Risks — Fix First

### 1.1 Missing BEV fleet number
Executive Summary para 1 reads "projected BEV fleet of [blank]" — the number is missing or corrupted.

**Recommend:** Insert **327,883** (datos.gob.es 2027 logistic curve). Ensure this matches `total_ev_projected_2027` in File 1. Do not use the rounded ~328,000 figure from EDA; evaluators will cross-check against the mandatory data source.

---

### 1.2 Grid status MW thresholds never defined
The report assigns Sufficient / Moderate / Congested labels but never states the MW cutoffs. Challenge Rules 1 and T4 require explicit thresholds.

**Recommend:** Add a small table in the methodology section:

| Classification | Available capacity | Basis |
|---|---|---|
| Sufficient | ≥ 10 MW | Endesa substation data |
| Moderate | 1.5 – 10 MW | Endesa substation data |
| Congested | < 1.5 MW | Endesa substation data |

Anchor to the 150 kW per-charger AFIR floor and note that i-DE / Viesgo substations default to Moderate due to missing data.

---

### 1.3 Viesgo absent from Appendix A
Viesgo is a required distributor source in the challenge spec and is not cited anywhere in the report. File 3 assigns 6 stations to Viesgo territory.

**Recommend:** Add Viesgo to Appendix A with a one-line description: distributor covering northern Spain (Cantabria, Asturias, eastern Galicia). Note that capacity data was unavailable and these stations default to Moderate grid status.

---

### 1.4 Sections 3.0 (Recommendations) and 4.0 (Conclusions) are empty
Only headings exist. These sections cover scoring criteria B2 (~10%) and B3 (~10%).

**Recommend:** Section 3 should present a three-phase deployment roadmap. **Phase 1 (2025–2027):** the 82 Moderate-grid stations — no reinforcement needed, shovel-ready. This is the only phase realistically achievable by 2027; explicitly acknowledge this. **Phase 2 (2027–2029):** reinforcement studies already in queue; stations deployable as CNMC approvals complete. **Phase 3 (2029+):** the 5 Congested stations requiring full *Acceso y Conexión* studies and grid upgrades (3–5 year lead time from today). Section 4 (Conclusions) should state Iberdrola's dual revenue logic clearly: regulated distribution income (i-DE, *retribución regulada* — fixed CNMC return regardless of charger utilisation) + merchant charging revenue (Iberdrola Smart Charging, per-kWh). This means even a low-utilisation rural N-* corridor generates regulated income from the grid connection itself — a structurally different ROI from a pure charging operator such as Repsol or BP Pulse, and a reason Iberdrola can justify corridors competitors would not.

---

### 1.5 Distributor zone assignment method not explained
File 3 includes `distributor_network` per station (i-DE: 74, Endesa: 7, Viesgo: 6) but the report never explains how this field is assigned.

**Recommend:** Add a short paragraph explaining the spatial matching methodology: Endesa stations are identified via KD-tree nearest-substation join on the Endesa capacity dataset; i-DE and Viesgo zones are assigned by geographic boundary fallback (i-DE covers most of Spain; Viesgo covers Cantabria / Asturias / eastern Galicia). Where no substation data is available, the station defaults to Moderate capacity.

---

## 2. High-Value Additions — Competitive Differentiation

### 2.1 "Zero capacity" = queue saturation, not physical impossibility
The report states 94% of Endesa substations have zero available capacity, which currently reads like a modelling artifact.

**Recommend:** Reframe as: *"94% of substations show zero unallocated firm capacity under current cola de acceso (CNMC RD 1183/2020) queue conditions — meaning they are queue-saturated, not physically excluded from new connections."* This is a real regulatory insight that shows domain knowledge and directly addresses T4.

---

### 2.2 AFIR 2025 TEN-T Core deadline is already breached
The report frames AFIR compliance as a 2027 target, but the TEN-T Core 60 km spacing requirement was mandatory from **31 December 2025** — already passed.

**Recommend:** Add one sentence: *"Spain is already in breach of AFIR Art. 4 TEN-T Core requirements as of 31 December 2025; the 5 priority consensus roads (A-21, N-111, N-211, N-623, N-634) address an active regulatory non-compliance, not a future obligation."* This sharpens urgency for the Iberdrola investment case.

---

### 2.3 Grid reinforcement lead times make some 2027 targets infeasible
Substation upgrades under *retribución regulada* take 3–5 years from CNMC approval to energization.

**Recommend:** In Section 3.0 roadmap, explicitly state that the 5 Congested stations cannot realistically be energized by 2027 unless reinforcement studies are initiated immediately. This positions Iberdrola as needing to act now, not at the 2027 deadline.

---

### 2.4 i-DE data gap = Iberdrola's own network advantage
The 74-station i-DE data gap (94.3% of Moderate stations) falls under Iberdrola's own distribution subsidiary.

**Recommend:** Frame as competitive advantage: *"In real deployment, Iberdrola has privileged access to i-DE internal capacity data unavailable to competitors. The conservative Moderate default used here would be replaced by precise substation readings, significantly improving site selection accuracy in the highest-priority corridors."*

---

### 2.6 Business context for model selection not explained (B1 — first tie-breaker)
The report describes XGBoost and the demand formula in technical terms but never states the *business rationale* for these choices. B1 (Integration between technical and strategic analysis) is the **first tie-breaking criterion** in the guidelines. The gap needs closing.

**Recommend:** Add a short paragraph in the methodology section with this framing: *"The XGBoost classifier was trained to identify roads where the combination of traffic volume, existing infrastructure density, and regional EV pressure matches the pattern of commercially successful charging deployments — it is a demand-readiness signal, not a rule-based filter. The Poisson regressor (MAE=0.075) was validated but intentionally replaced by the INE demand formula for final charger sizing: past deployment patterns reflect historical underinvestment biases and would predict where chargers were built, not where Spain's 327,883-vehicle 2027 fleet will need them. The formula is prospective by design."* This connects T3 to B1 and directly answers what the judges will ask.

---

### 2.7 PNIEC 2030 context missing (B2/B3 differentiation)
Spain's PNIEC 2021–2030 commits to 250,000 public chargers by 2030. The report does not reference this.

**Recommend:** Add one paragraph positioning FV's output within PNIEC: *"The 502 chargers proposed across 87 interurban stations represent the high-priority backbone layer of Spain's 250,000-charger PNIEC 2021–2030 target. Iberdrola deploying on these corridors now secures both AFIR compliance and first-mover position on the routes that will carry the majority of Spain's 2030 EV traffic — at a point where premium locations are still available."* No competitor is likely to quantify this framing. It is also a clean answer to B3 (business value for Iberdrola).

---

### 2.5 Simultaneity factor not acknowledged
150 kW × n_chargers implies 100% concurrent utilisation. Industry standard is 65–80% simultaneity.

**Recommend:** Add a brief note: *"Grid demand estimates apply a 100% simultaneity factor as required by the challenge formula; real peak load would be approximately 25–35% lower under standard industry simultaneity assumptions (65–80%). Congested / Moderate classifications are therefore conservative."* This demonstrates technical credibility without breaking the required formula.

---

## 3. Minor Fixes

| # | Issue | Fix |
|---|---|---|
| M1 | REE §1.5 paragraph ends mid-sentence | Complete the sentence |
| M2 | "Carrreteras" triple-r typo in §1.1 | → "Carreteras" |
| M3 | "autopista de paeje" in §1.1 | → "autopista de peaje" |
| M4 | Charger count cited as 479 in body text | → Update to **502** (post-Section 8c seasonal adjustment) |
| M5 | Capacity cited as 71,850 kW in body text | → Update to **75,300 kW** |
| M6 | Seasonal IMD flagged as limitation | → Now resolved: Section 8c applies DGT-based seasonal multipliers (AP-* ×1.25, A-* ×1.15). Update §2.2.6 narrative accordingly |
| M7 | Poisson regressor described as unused | → Reframe as deliberate validation step: MAE=0.075 confirms model quality; INE demand formula used operationally for prospective 2027 sizing |
| M8 | datos.gob.es GitHub fork URL not explicitly cited in report body | → Guidelines §4 Source 3 requires the fork URL to appear in BOTH the Colab notebook AND the Analytical Report. Verify it is present as a numbered citation in Appendix A |
| M9 | Key assumptions not documented using the guidelines §6 three-part structure | → For each major assumption (50% utilisation, seasonal multipliers AP-* ×1.25 / A-* ×1.15, Moderate default for i-DE/Viesgo), the report must include: **(1) Document Your Logic** — state the value; **(2) Show Your Research** — cite the source (AEDIVE, ICCT, DGT IMD, CNMC); **(3) The Expert Perspective** — explain why it is appropriate for real infrastructure planning. Missing this structure is explicitly listed as a T1 penalty |

---

## 4. Priority Checklist

| # | Item | Risk if skipped |
|---|---|---|
| 1 | Fix missing BEV fleet number → 327,883 | Disqualification |
| 2 | Add MW threshold table | Disqualification (T4) |
| 3 | Write Sections 3.0 and 4.0 | ~20% of grade (B2 + B3) |
| 4 | Add Viesgo to Appendix A | Disqualification risk |
| 5 | Explain distributor zone assignment | T4 compliance |
| 6 | Update 479 → 502 chargers, 71,850 → 75,300 kW | Inconsistency with deliverables |
| 7 | Reframe zero-capacity as cola de acceso queue saturation | T1/B3 score quality |
| 8 | Add AFIR 2025 breach sentence | B2/B3 differentiation |
| 9 | Add phased roadmap with grid lead times | B2 coherence |
| 10 | Frame i-DE gap as Iberdrola advantage | B3 business value |
| 11 | Add business context for model selection (2.6) | B1 tie-breaker |
| 12 | Add PNIEC 2030 positioning paragraph (2.7) | B2/B3 differentiation |
| 13 | Add simultaneity factor caveat | Technical credibility |
| 14 | Apply §6 three-part structure to key assumptions (M9) | T1 — explicit penalty if missing |
| 15 | Verify datos.gob.es fork URL in report body (M8) | B6 / disqualification risk |
| 16 | Fix typos M2, M3; complete M1 mid-sentence | Basic quality |
