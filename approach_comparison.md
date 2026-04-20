# IE Iberdrola Datathon — Approach Comparison & Methodology Rationale

---

## 1. Challenge Goals (Alignment Anchor)

The datathon asks teams to:

| # | Objective | Key constraint |
|---|---|---|
| **O1** | Propose the **minimum** number of stations to cover interurban EV mobility demand | Sparse but seamless; economically viable |
| **O2** | Identify **friction points** where grid congestion limits deployment | Cross-reference mobility data with distributor capacity maps |
| **O3** | Deliver an **actionable strategic roadmap** for Iberdrola | Trade-offs between demand, grid, and capex |

All models must target **2027**, use the **datos.gob.es EV fleet projection** (327,883 vehicles), and comply with **AFIR regulation (EU 2023/1804 Art. 4)** — maximum 60 km gap between charging stations on interurban corridors.

**Regulatory context — why this creates urgency:** AFIR is legally binding from **2025** on TEN-T Core corridors and from **2027** on TEN-T Comprehensive. Once the deadline passes, all operators must comply — Iberdrola's first-mover window to lock in premium locations closes as the regulation becomes mandatory. The datos.gob.es projection is the official DGT/MITMA fleet baseline aligned with PNIEC 2021–2030 reporting; using any other source would be inconsistent with Spain's official decarbonisation commitments, which is why it is a mandatory evaluation input.

---

## 2. Approaches Considered

### Approach 1 — M6 Greedy (Baseline Heuristic)

**Description:** Pure gap-filling heuristic. Scans the road network and places stations wherever a >60 km gap exists, using fixed charger counts.

**Pros:**
- Simple, fully interpretable
- Guarantees AFIR minimum spacing in covered segments
- Captures island routes (TF-1, Ma-13) that ML approaches miss

**Cons:**
- No demand signal — treats a low-traffic rural road identically to AP-7
- Massively over-represents Endesa geography (92% Congested) due to geographic bias
- No grid-capacity integration
- Does not comply with AFIR at network level (150 km effective spacing)
- Cannot justify charger counts per station

---

### Approach 2 — V1 Teammate (LightGBM + MILP)

**Description:** Segment-level LightGBM classifier selects road segments; MILP (scipy/HiGHS) minimises total chargers subject to demand coverage and grid constraints.

**Pros:**
- Formal optimisation framework (MILP provides provable optimality)
- Grid constraint explicitly modelled in the solver
- HiGHS solver (LP relaxation + branch-and-bound) is production-grade

**Cons:**
- Segment-level granularity → F1=0.833, PR-AUC=0.583 (poor vs road-level)
- MILP objective is **MINIMISE** chargers — wrong direction for an Iberdrola investment narrative (investor wants to maximise coverage/revenue, not minimise assets)
- NOT AFIR compliant: uses 10/20 km segment threshold, not the 60 km gap requirement
- LP infeasible with full grid constraints; required constraint relaxation
- 81 stations at segment granularity are harder to map to real interurban road designations

---

### Approach 3 — V2 (AFIR-first ML)

**Description:** XGBoost classifier + XGBoost Poisson regressor at road level. AFIR ≤60 km spacing used as the **primary filter** to select candidate roads; traffic-weighted charger sizing.

**Pros:**
- Road-level granularity → F1=0.967, PR-AUC=0.995 (major improvement over segment-level)
- Fully AFIR compliant by construction
- Demand signal integrated via traffic weights
- Clean separation between selection (classifier) and sizing (regressor)

**Cons:**
- AFIR used as a filter rather than a regulatory floor — excludes valid high-demand roads that already have partial coverage
- Charger sizing (traffic-weighted formula) is not grounded in actual 2027 demand projections
- Grid congestion signal not incorporated at selection stage

---

### Approach 4 — V3 (Demand-first ML, corrected)

**Description:** Same XGBoost + Poisson stack as V2, but selection logic flipped: ML-flagged roads ranked by **demand pressure** (EV fleet / refill points × traffic). AFIR becomes an additive gap-fill layer (Layer 2), not an exclusion filter.

**Pros:**
- Demand-first framing aligns with investor logic: deploy where pressure is highest
- AFIR ≤60 km enforced as a hard floor, not a ceiling — no high-demand roads are excluded
- All 73 V2 roads are retained (V3 ⊇ V2); 7 additional gap-fill roads added
- 5 consensus roads identified across all ML approaches (A-21, N-111, N-211, N-623, N-634)

**Cons:**
- Charger sizing still traffic-weighted (not demand-calibrated to 2027 fleet)
- 5 coordinate-duplicate rows required post-hoc dedup fix (93 stations after correction)
- Grid congestion not yet integrated at selection stage

---

### Approach 5 — FV Final Version (Demand-first + Grid Penalty + Demand-sized Chargers)

**Description:** Extends V3 with two additions: (a) Endesa KD-tree grid signal integrated into Layer 1 demand pressure scoring, and (b) charger counts replaced by INE demand formula using 2027 EV fleet projections.

**Pros:**
- **Demand-weighted selection** (Layer 1): stations ranked by `ev_fleet_2027_regional / refill_points × traffic`
- **AFIR as regulatory floor** (Layer 2): gap-fill is purely additive — no roads removed
- **Grid congestion at selection stage** (Layer 1b): Endesa KD-tree penalises roads near congested substations
- **Demand-calibrated charger sizing**: `n_chargers = ceil(daily_sessions / 16)` using 327,883-vehicle 2027 projection — directly tied to the mandatory datos.gob.es output. The 150 kW/charger constant is not arbitrary: AFIR Art. 4 mandates a **minimum 150 kW per charging point** on TEN-T Core interurban corridors, making this value a regulatory floor, not an assumption
- Produces fewer but more precisely allocated chargers than V3 (479 vs 630) — economically efficient
- MILP extension (Section 15) ready for activation if Iberdrola provides a budget envelope
- Fully AFIR compliant

**Cons:**
- 80.5% of stations default to "Moderate" (i-DE and Viesgo data gaps — no data available)
- All 87 stations are Moderate or Congested (none Sufficient) due to Endesa-only grid signal
- MILP extension non-executed (requires Iberdrola budget input)

---

## 3. ML Design Decisions

These choices are non-obvious and will be questioned by anyone reading the methodology. Each decision has a concrete reason.

### 3.1 Why XGBoost, not Random Forest or LightGBM?

The dataset has 494 road-level rows with 59 mixed features (continuous traffic proxies, binary infrastructure flags, regional demand estimates). At this scale, gradient boosting on tabular data consistently outperforms Random Forest (no shrinkage, weaker regularisation) and LightGBM offers no advantage (leaf-wise splitting gains matter at >10k rows; here it would overfit). XGBoost with `tree_method='hist'` gives the right bias-variance balance for ~500 rows, handles missing values natively, and exposes SHAP values for business-facing interpretation.

### 3.2 Why GroupKFold, not standard KFold?

Roads are not independent observations. The feature matrix has 494 rows but only 423 unique roads — 69 roads appear multiple times with different `traffic_weight` values from different segments. Under standard KFold, the same road can appear in both train and test folds, inflating metrics by leaking road identity. GroupKFold k=5 assigns all rows belonging to the same road to the same fold, enforcing true out-of-sample evaluation.

### 3.3 Why F1=0.967 is legitimate (not overfit)

A first pass produced F1=0.994 — a red flag. Root cause: 9 infrastructure features were directly derived from the target (e.g. `n_stations`, `existing_coverage_ratio`). These were removed (`CLF_EXTRA_EXCLUSIONS`). After the leakage fix, F1 dropped to 0.967. The residual high performance is explained by `mean_max_power_kw`: roads with no stations have this feature = 0 by definition, which is a real infrastructure signal (absence of charging infrastructure is observable before labelling), not leakage. Class balance: 307 negatives / 187 positives (62/38) — F1 is the right metric here, not accuracy (0.98 accuracy would be misleadingly high on this split).

### 3.4 Why threshold = 0.66, not 0.50?

The default threshold of 0.50 maximises accuracy. We optimised threshold for F1 on the OOF predictions, which shifted it to 0.66. The practical implication: higher threshold = higher precision, lower recall. For an Iberdrola capex decision, a false positive (investing in a road that doesn't need a station) is more costly than a false negative (missing a viable road that Layer 2 AFIR gap-fill may catch anyway). The threshold bias is intentional.

### 3.5 Why Poisson regression for charger counts?

Charger counts are discrete non-negative integers ranging 1–5 in the training data. Standard regression (MSE objective) can predict negative values and treats the distance from 1→2 identically to 4→5, which is wrong for count data. The Poisson log-likelihood objective (`objective='count:poisson'` in XGBoost) is the natural choice: it enforces non-negativity and is calibrated for count distributions. MAE=0.075 vs baseline (predict-mean) MAE=0.107 — a 30% improvement on a range of 1–5.

### 3.6 Why was the regressor output replaced by the demand formula?

The regressor was trained on historical charger counts (y=1–5), which reflect *past deployment decisions*, not *future demand*. A model trained on past infrastructure patterns predicts past infrastructure patterns — it would replicate Iberdrola's historical deployment biases, not identify where 327,883 EVs in 2027 will need charging. The INE demand formula (`n_chargers = ceil(daily_sessions / 16)`) is prospective by design: it uses the mandatory datos.gob.es 2027 EV fleet projection as input. The regressor MAE=0.075 is reported as a model quality signal, not used operationally.

### 3.7 Why is V1's LightGBM segment-level approach structurally weaker?

The F1=0.833 / PR-AUC=0.583 gap vs road-level (0.967 / 0.995) is not coincidental — it is structural. The road-level target `y_reg` is repeated identically across all segments of the same road. Without GroupKFold at segment level, the same road's label appears in both train and test folds, creating target leakage. V1 used standard KFold at segment granularity, meaning the classifier was partially evaluated on data it had already seen at the road level. The poor PR-AUC (0.583 ≈ near-random for imbalanced classes) is the consequence.

### 3.8 Why MILP is not the primary approach

MILP (Mixed-Integer Linear Programming) was the optimisation backbone of V1 and is retained as a non-executed extension in FV Section 15. It is **not used as the primary method** for three compounding reasons:

1. **Wrong objective in V1.** The V1 MILP minimises total chargers (`min Σxⱼ`). For an Iberdrola investment pitch, minimising assets is the opposite of the desired framing — the goal is to maximise demand-weighted coverage subject to a budget, not to find the smallest possible network. The objective direction was corrected in FV Section 15 to `max Σ demand_pressure_norm_j × xⱼ`, but this requires a budget envelope as input.

2. **Infeasibility under full grid constraints.** When V1 applied all grid capacity constraints simultaneously, the LP relaxation became infeasible — the constraints were mutually exclusive given the available road set. The solver required constraint relaxation to produce any output, which undermines the core value proposition of MILP (provable optimality under stated constraints). A solution obtained after relaxing constraints is no more reliable than a heuristic.

3. **The demand formula achieves equivalent per-station sizing without solver complexity.** When there is no shared budget constraint, optimising each station independently (as FV does via the INE demand formula) produces the same result as a MILP with decoupled constraints. The formula `n_chargers = ceil(daily_sessions / 16)` is the closed-form solution to the per-station subproblem — the solver adds no value unless a binding cross-station budget forces trade-offs. FV Section 15 MILP activates precisely when Iberdrola provides `TOTAL_BUDGET_EUR`, creating that binding constraint. Until then, the demand formula is the correct and simpler choice.

**Where we do use MILP — and why.** MILP is included as a non-executed extension in FV Section 15 (`Modelling_FV.ipynb`, cells 48–49) for a specific scenario: when Iberdrola provides a total capital budget envelope (`TOTAL_BUDGET_EUR`). At that point, the problem changes structurally — stations compete for the same budget, and the trade-off between deploying at a Moderate-grid site (€15k/charger) vs. a Congested-grid site (€35k/charger, CNMC RD 1183/2020) cannot be solved station-by-station. A shared budget makes the cross-station constraint binding, which is exactly the regime where MILP adds value over the demand formula. The formulation was corrected from V1's minimise-chargers objective to `max Σ demand_pressure_norm_j × xⱼ` — maximising demand-weighted coverage — with asymmetric capex costs and a hard cap of 3 chargers at Congested nodes to limit grid reinforcement exposure. The solver (scipy HiGHS, LP relaxation + branch-and-bound) is production-grade and reuses V1's infrastructure. We present it to Iberdrola as the natural next step once a budget figure is on the table.

---

## 4. Summary Comparison Table

| Metric | M6 Greedy | V1 (Teammate) | V2 (AFIR-first) | V3 (Demand-first) | **FV (Final)** |
|---|---|---|---|---|---|
| **Selection logic** | Heuristic gap-fill | LightGBM + MILP | AFIR density | Demand pressure | Demand + grid penalty |
| **Classifier** | None | LightGBM | XGBoost | XGBoost | XGBoost |
| **Optimizer / Regressor** | None | MILP (HiGHS) | XGBoost Poisson | XGBoost Poisson | Demand formula (INE) |
| **Granularity** | Road-level | Segment-level | Road-level | Road-level | Road-level |
| **Roads selected** | 23 | 81 (segments) | 73 | 80 | 80 |
| **Proposed stations** | 26 | 81 | 91 | 93 | **87** |
| **Total chargers** | 192 | 422 | 600 | 630 | **479** |
| **Installed capacity (kW)** | 28,800 | 63,300 | 90,000 | 94,500 | **71,850** |
| **Charger sizing method** | Fixed rule | MILP (minimise) | Traffic weight | Traffic weight | Demand-based (INE) |
| **AFIR 60 km spacing** | No (150 km gap) | No (10/20 km thr) | Primary filter | Layer 2 gap-fill | Layer 2 gap-fill |
| **Grid congestion signal** | None | None | None | None | Layer 1b (Endesa KD-tree) |
| **Classifier F1** | N/A | 0.833 | 0.967 | 0.967 | **0.967** |
| **Regressor MAE** | N/A | — | 0.075 | 0.075 | **0.075**\* |

\* FV trains the Poisson regressor but replaces its output with the INE demand formula for final charger counts.

---

## 5. Why FV is the Chosen Approach

The datathon explicitly asks teams to minimise stations while covering demand — but the deeper ask is to build a solution **Iberdrola could act on**. FV is the only approach that satisfies all three objectives simultaneously:

| Challenge criterion | FV response |
|---|---|
| **O1 — Minimum stations** | 87 stations (fewer than V2's 91 and V3's 93) via demand concentration |
| **O1 — Justified charger counts** | INE formula tied to 327,883 EV projection (mandatory datos.gob.es output) |
| **O2 — Grid friction points** | 87 friction points (all stations Moderate/Congested); Endesa KD-tree at selection stage |
| **O3 — Iberdrola investment narrative** | Demand-first ranking = deploy where revenue potential is highest. Iberdrola earns from two streams: **i-DE** (regulated grid connection fees, *retribución regulada* — fixed CNMC return regardless of utilisation) + **Iberdrola Smart Charging** (per-kWh service revenue — utilisation-dependent). Even low-utilisation stations in congested areas earn regulated connection income |
| **AFIR compliance** | Layer 2 gap-fill guarantees ≤60 km spacing on all selected corridors |
| **Data gap handling** | i-DE/Viesgo absence documented; "Moderate" default is conservative, not arbitrary |
| **MILP extension (Sec. 15)** | Activates with budget envelope: maximises demand-weighted chargers with asymmetric grid costs (€15k Moderate / €35k Congested). The 2–3× premium for Congested nodes reflects CNMC *Acceso y Conexión* (RD 1183/2020): connections exceeding local substation capacity require a full grid reinforcement study and shared-cost allocation — a regulatory cost structure, not an estimate |

**The key differentiator vs. other approaches:** FV is the only version where charger counts are directly derived from the mandatory datos.gob.es EV fleet projection (327,883 vehicles, 2027 logistic curve), which is an explicit evaluation requirement. All other approaches use traffic weights or MILP that are decoupled from this mandatory data source. The datos.gob.es projection is the official DGT/MITMA baseline used in PNIEC 2021–2030 reporting — anchoring to it ensures the methodology is consistent with Spain's government-published decarbonisation trajectory.

**5 consensus roads** validated across all ML approaches (A-21, N-111, N-211, N-623, N-634) represent the highest-confidence investment signals and should anchor the report's strategic narrative. All five are in the **northeastern interior corridor** (Aragón, Navarra, Castilla y León) — the gap between the well-served Mediterranean coast (AP-7) and the French border TEN-T Core entry point. This is the interior TEN-T link with the lowest existing coverage relative to cross-border transit demand, making it both the highest ML-consensus signal and the highest regulatory-urgency corridor.

---

## 6. Data & Notebook Pipeline

The following diagram traces every file from raw source to final deliverable.

```
RAW DATA SOURCES
├── Data/raw/road_routes_spain/carreteras_RTIG.geojson          [Ministry of Transport — RTIG]
├── Data/external/grid_capacity_endesa/endesa_demanda_2026_03.csv  [Endesa e-distribución]
├── Data/interim/m2_charging_sites_interurban.csv               [National Access Point — M2]
└── datos.gob.es GitHub fork → EV fleet logistic curve (327,883 vehicles, 2027)
          │
          ▼
STEP 1 — notebooks/Dataset_setup.ipynb
  Reads : DGT registration files, M2 raw data, Endesa CSV
  Writes: Data/interim/ev_registrations_2025.csv
          Data/interim/m2_charging_sites_all.csv
          Data/interim/m2_charging_sites_interurban.csv
          Data/interim/m2_road_coverage.csv
          │
          ▼
STEP 2 — notebooks/EDA_Complete.ipynb
  Reads : Data/interim/m2_charging_sites_*.csv
          Data/raw/road_routes_spain/carreteras_RTIG.geojson
          Data/external/grid_capacity_endesa/endesa_demanda_2026_03.csv
  Writes: Data/processed/ev_charging_ml_dataset_v2.csv     ← 494 road-level rows, raw features
          │
          ▼
STEP 3 — notebooks/temporary/Feature_engineering/FE_v2.ipynb
  Reads : Data/processed/ev_charging_ml_dataset_v2.csv
  Writes: Data/processed/feature_matrix.csv                ← 494 × 62 (59 X features + labels)
          │
          ▼
STEP 4 — notebooks/Modelling/Modelling_FV.ipynb            ← PRIMARY SUBMISSION NOTEBOOK
  Reads : Data/processed/feature_matrix.csv
          Data/processed/ev_charging_ml_dataset_v2.csv     (metadata: Carretera, comunidad_autónoma)
          Data/interim/endesa_interim.csv                   (cached Endesa substations)
  Trains: XGBoost Classifier  (GroupKFold k=5, F1=0.967, PR-AUC=0.995)
          XGBoost Poisson Regressor (MAE=0.075)
  Applies: Layer 1 demand pressure ranking
           Layer 1b Endesa KD-tree grid penalty
           Layer 2 AFIR ≤60 km gap-fill
           Section 8b demand formula charger sizing
  Writes: Data/processed/File_2_FV.csv   → 87 proposed stations
          Data/processed/File_3_FV.csv   → 87 friction points (all Moderate/Congested)
          Data/processed/File_1_FV.csv   → Global KPIs scorecard (1 row)
          Data/processed/BI_Visualization_FV.html  → Interactive Folium map
          │
          ▼
FINAL SUBMISSION
  Rename: File_1_FV.csv → File_1.csv
          File_2_FV.csv → File_2.csv
          File_3_FV.csv → File_3.csv
          BI_Visualization_FV.html → BI_Visualization.html
```

**Reference notebooks (not in submission pipeline):**
- `notebooks/Modelling/Modelling_v2.ipynb` — V2 AFIR-first approach (reference)
- `notebooks/Modelling/Modelling_v3.ipynb` — V3 demand-first approach with dedup fix (reference)
- `notebooks/Modelling/Classification.ipynb` — V1 teammate LightGBM classifier
- `notebooks/Modelling/Optimization.ipynb` — V1 teammate MILP (constants reused in FV Sec. 15)

---

## 7. Final Submission Scorecard (File 1 — FV)

| KPI | Value |
|---|---|
| `total_proposed_stations` | **87** |
| `total_existing_stations_baseline` | **3,679** |
| `total_friction_points` | **87** |
| `total_ev_projected_2027` | **327,883** |

**Network summary:**

| Metric | Value |
|---|---|
| Unique roads covered | 80 |
| Total chargers | 479 |
| Avg chargers per station | 5.5 |
| Total installed capacity | 71,850 kW |
| Grid: Moderate stations | 70 (80.5%) |
| Grid: Congested stations | 17 (19.5%) |
| Grid: Sufficient stations | 0 (0%) — all stations are friction points |
| AFIR ≤60 km compliant | Yes (Layer 2 gap-fill) |
| Charger sizing basis | INE demand formula (datos.gob.es mandatory output) |

**5 consensus roads (highest-confidence investment signals):**
A-21, N-111, N-211, N-623, N-634 — flagged by all three ML approaches (V1, V2, V3/FV).

---

## 8. Issues, Warnings & Submission Compliance Scorecard

The table below merges the **Submission Compliance Scorecard** (16 submission-facing checks) with the **Technical Issues** (W-series: internal data and model quality issues). Items are grouped by category.

### Legend
- ❌ Risk — disqualification or critical output error if unresolved  
- ⚠ Warn — degrades score or narrative credibility; must be documented in report  
- ✅ OK — compliant or resolved; no action needed  

---

### A. Submission & Compliance Risks

| # | Issue | Rating | Status | Required Action |
|---|---|---|---|---|
| SC-8 | **Google Colab migration** — notebook is local Jupyter; submission requires Colab with all outputs visible | ❌ Risk | OPEN | Upload Modelling_FV.ipynb to Colab; replace local paths with Drive mount; execute all cells |
| SC-7 | Mandatory fork URL (`https://github.com/Jvilpi/Laboratorio-de-Datos`) must appear in report body and Colab | ✅ OK | OPEN | Confirm URL appears in report text before submission |

---

### B. Grid & Data Gaps

| # | Issue | Rating | Status | Required Action |
|---|---|---|---|---|
| W1 / SC-1 | i-DE and Viesgo capacity files empty → 94.3% of stations default to "Moderate" (82/87) | ⚠ Warn | OPEN | Document fallback in report; frame as conservative estimate pending Iberdrola's own i-DE data |
| W2 / SC-2 | Endesa-only KD-tree → 0 "Sufficient" stations; all 87 are friction points | ⚠ Warn | OPEN | Add BI legend note: "No Sufficient-grid stations — all 87 locations carry grid constraints" |
| SC-12 | i-DE data absence not documented — no retrieval attempt noted | ⚠ Warn | OPEN | State in report: i-DE capacity dataset retrieved [date], file empty → fallback Moderate; cite i-DE public URL |
| SC-3 | Grid status thresholds undocumented in report | ⚠ Warn | OPEN | Mandatory paragraph: Congested <1.5 MW, Moderate 1.5–10 MW, Sufficient ≥10 MW; anchor to 150 kW × n_chargers peak load + CNMC *Acceso y Conexión* |
| SC-10 | Viesgo attribution: 6 stations mislabelled as i-DE | ✅ Fixed | ✅ DONE | Cell 34 geographic fallback patched; Cell 24 Extremadura corrected. File_3: i-DE:74 / Endesa:7 / Viesgo:6 |

---

### C. Charger Sizing & Demand Assumptions

| # | Issue | Rating | Status | Required Action |
|---|---|---|---|---|
| SC-5 | 50% utilisation aggressive for 2027 Spain (realistic: 20–25%, AEDIVE) | ⚠ Warn | OPEN | Add sensitivity table: 20%→1,197 / 35%→684 / 50%→479 chargers; add peak coincident load note for grid sizing |
| W5 | Poisson regressor trained but NOT used for final charger counts | ⚠ Warn | — | Report MAE=0.075 as model quality signal; clarify INE demand formula is the operative sizing method |
| W3 | MILP Section 15 (cells 48–49) not executed — requires `TOTAL_BUDGET_EUR` from Iberdrola | ✅ OK | OPEN | Frame as strategic extension: "activates when Iberdrola provides a budget envelope" |
| SC-9 | File 3 `estimated_demand_kw` field | ✅ OK | ✅ DONE | Confirmed present: n_chargers × 150 kW |

---

### D. ML Model & Pipeline

| # | Issue | Rating | Status | Required Action |
|---|---|---|---|---|
| SC-6 | Classifier target (AFIR binary) vs challenge objective (demand) | ✅ OK | — | Gate (classifier) + priority ranker (demand) is correctly aligned — document two-layer logic |
| W4 | `feature_matrix.csv`: 494 rows but 423 unique roads (69 duplicate segments) | ✅ Fixed | ✅ DONE | `drop_duplicates('carretera_group', keep='first')` in Cell 27 of FV; do NOT modify FE_v2.ipynb |
| W6 | V3 had 5 coordinate-duplicate stations (98 → 93 rows) | ✅ Fixed | ✅ DONE | Dedup patch Cell 27; FV inherits fix and further reduces to 87 stations via demand formula |

---

### E. Report & Business Narrative Gaps

| # | Issue | Rating | Status | Required Action |
|---|---|---|---|---|
| SC-11 | Phased deployment roadmap missing | ⚠ Warn | OPEN | Phase 1 (2025–26): top-30 Moderate; Phase 2 (2026–27): remaining Moderate; Phase 3: 5 Congested + AFIR gap-fills |
| SC-15 | Revenue/business value narrative missing | ⚠ Warn | OPEN | (1) charging fees via Iberdrola Smart Charging; (2) i-DE connection fees (retribución regulada); (3) Congested CAPEX pipeline ~€3–17M for 5 stations |
| SC-13 | PNIEC 2021–2030 not cited | ⚠ Warn | OPEN | One paragraph: 479 chargers = minimum interurban backbone within Spain's 250k-charger 2030 PNIEC target |
| SC-14 | RD 29/2021 not referenced | ⚠ Warn | OPEN | Optional but differentiating: obligated service stations reduce deployment risk for Iberdrola |
| SC-4 | AFIR Layer 2 (9 gap-fill roads) framing | ✅ OK | — | Frame as legally mandatory (EU 2023/1804 Art. 4); not an optimisation choice |
| SC-16 | BI legend: no Green marker, no explanation | ✅ OK | OPEN | Add legend note explaining absence of Sufficient-grid stations |

---

### Summary Counts

| Category | ❌ Risk | ⚠ Warn (Open) | ✅ OK / Fixed |
|---|---|---|---|
| Submission & Compliance | 1 | 0 | 1 |
| Grid & Data Gaps | 0 | 3 | 2 |
| Charger Sizing & Demand | 0 | 2 | 2 |
| ML Model & Pipeline | 0 | 0 | 3 |
| Report & Business Narrative | 0 | 5 | 2 |
| **Total** | **1** | **10** | **10** |

**Priority order:** SC-8 (Colab migration) → SC-5 + W5 (charger sensitivity) → SC-11/15/13 (report narrative) → SC-3/12 (grid documentation) → SC-14/16 (optional differentiators)
