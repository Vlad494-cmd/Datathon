# IE Iberdrola Datathon — Project Walkthrough

> **Updated:** 2026-04-14
> **Branch:** EDA
> **Challenge:** Intelligent Electric Mobility — Designing Spain's 2027 EV Charging Network

---

## 1. Challenge Overview

Design a data-driven public EV charging network for Spain's interurban road system (autopistas, autovías, carreteras nacionales), targeting a 2027 operational scenario. The challenge has two core objectives:

1. **Network Optimisation (Primary):** Propose the minimum number of charging stations that adequately cover interurban demand — maximising utilisation while minimising capital expenditure.
2. **Grid Viability (Secondary):** Identify "friction points" where electrical grid constraints make deployment infeasible or risky.

---

## 2. Required Deliverables

| # | Deliverable | Description |
|---|---|---|
| 1 | `File 1.csv` | 1 summary row — global network KPIs |
| 2 | `File 2.csv` | 1 row per proposed charging station |
| 3 | `File 3.csv` | Friction points only (grid_status ≠ Sufficient) |
| 4 | Colab Notebook | All cells executed, all outputs visible |
| 5 | BI Map | Self-contained interactive map, colour-coded by grid status |
| 6 | Analytical Report | 3–5 page executive summary |
| 7 | Final Pitch | 5-min PPT/PDF (finalist teams only) |

### Key Technical Constants

- **Standard charger power:** 150 kW (fixed, no exceptions)
- **estimated_demand_kw formula:** `n_chargers_proposed × 150`
- **Coordinate system:** WGS84 decimal degrees (EPSG:4326)
- **grid_status values:** `Sufficient` | `Moderate` | `Congested`
- **distributor_network values:** `i-DE` | `Endesa` | `Viesgo`

---

## 3. Repository Structure

```
Datathon/
├── Data/
│   ├── raw/
│   │   ├── road_routes_spain/             ← M1: Road network GeoJSON (generated)
│   │   ├── ev_charging_points_national/   ← M2: DGT DATEX2 XML (snapshot downloaded)
│   │   ├── ev_fleet_projections_datosgob/ ← M3: datos.gob.es parquet files (downloaded)
│   │   ├── dgt_vehicle_registrations/     ← R4: DGT monthly registration ZIPs (6 months, downloaded)
│   │   └── ev_charging_points_local/      ← R5: Local charging data (optional, pending)
│   ├── external/
│   │   ├── grid_capacity_ide_iberdrola/   ← R1: i-DE substation capacity (manual download needed)
│   │   ├── grid_capacity_endesa/          ← R2: Endesa node capacity CSV/XLSX (downloaded)
│   │   └── grid_capacity_viesgo/          ← R3: Viesgo substation capacity (manual download needed)
│   ├── interim/                           ← Intermediate cleaned files (gitignored)
│   ├── processed/                         ← Model output files (gitignored)
│   ├── metadata/DATASETS_SETUP.md        ← Full dataset documentation
│   └── scripts/                           ← Bash auto-download scripts
├── notebooks/
│   ├── Dataset_setup.ipynb                ← Data inventory & preprocessing guide
│   ├── M1_Road_Network_RTIG.ipynb         ← ✅ Complete: Road network download & filter
│   ├── M2_EV_Charging_Points_Baseline.ipynb ← ✅ Complete: EV charging baseline (3,679 sites)
│   ├── M3_EV_Fleet_Projection_2027.ipynb  ← ✅ Complete: SARIMA EV fleet forecast
│   └── (M4, M5, Final Assembly — pending)
├── references/
│   └── dataset_download_workaround.txt    ← MITMA REST API workaround guide
├── IE_Iberdrola_Datathon_guidelines.txt   ← Official challenge guidelines
└── walkthrough.md                         ← This file
```

---

## 4. Notebook Walkthroughs

---

### 4.1 `Dataset_setup.ipynb` — Data Inventory & Setup Guide

This is a documentation notebook (no code execution required). It mirrors `Data/metadata/DATASETS_SETUP.md` and serves as the team's reference for:
- Which datasets are mandatory vs. recommended
- Where each dataset lives in the folder structure
- How to download datasets that are not tracked in git
- Preprocessing snippets for each format (XML, ZIP/CSV, SHP, XLSX)
- A quick-start checklist

---

### 4.2 `M1_Road_Network_RTIG.ipynb` — Road Network Download & Filter

**Status:** ✅ Complete — output saved to `Data/raw/road_routes_spain/carreteras_RTIG.geojson`

**Purpose:** Download Spain's interurban road network from the Ministry of Transport (MITMA) REST API, filter to eligible road types, and export as GeoJSON for downstream use by M4.

**Step-by-step:**

1. **Setup** — Imports `geopandas`, `shapely`, `requests`, `matplotlib`. Defines the ArcGIS REST API endpoint for the RTIG dataset (1,602 records total). The MITMA direct download portal is under maintenance; the REST API is the workaround documented in `references/dataset_download_workaround.txt`.

2. **Download** — Paginates through the API in batches of 500 records (4 batches), requesting WGS84 coordinates directly (`outSR=4326`). Downloads all 1,602 records successfully.

3. **Build GeoDataFrame** — Parses ESRI JSON polyline features into Shapely `LineString`/`MultiLineString` objects. Creates a `GeoDataFrame` with CRS EPSG:4326 (WGS84).

4. **Explore road types** — Inspects the `Tipo_de_via` field. Finds 5 categories:
   - `Autopista libre\Autovía` (534 segments) — free motorways
   - `Autopista peaje` (79 segments) — toll motorways
   - `Multicarril` (189 segments) — multi-lane roads
   - `Carretera convencional` (789 segments) — conventional roads (includes N- national roads)
   - `NaN` (11 segments)

5. **Eligibility filter** — Two-criterion OR filter:
   - `Tipo_de_via` contains `autopista`, `autov`, or `multicarril` → captures AP- and A- roads
   - `Carretera` starts with `N-` → captures national roads (which appear as `Carretera convencional`)
   - Result: **1,535 segments kept**, 67 excluded. 423 unique road designations.

6. **Network summary** — Total eligible network: **~29,050 km**. Longest roads: AP-7N (849 km), A-66 (689 km), N-630 (669 km), A-4 (583 km).

7. **Visualisation** — Plots the filtered network colour-coded by road type as a sanity check.

8. **Export** — Saves to `Data/raw/road_routes_spain/carreteras_RTIG.geojson` (~73 MB). Adds `length_m` column (computed in EPSG:25830) for M4 to use when spacing charging stations.

9. **Verification** — Reloads file from disk and asserts: record count > 0, CRS = EPSG:4326, no null geometries, coordinates within Spain's bounding box.

---

### 4.3 `M3_EV_Fleet_Projection_2027.ipynb` — SARIMA EV Fleet Forecast

**Status:** ✅ Complete — output saved to `Data/processed/m3_ev_projection.json`
**Key output:** `total_ev_projected_2027 = 220,171`

**Purpose:** Project the total BEV fleet in Spain for 2027 — a mandatory input for `File 1.csv` (`total_ev_projected_2027`). Replicates and extends the SARIMA methodology from the mandatory datos.gob.es fork.

**Fork reference:** [NOSIEMPRE/Laboratorio-de-Datos](https://github.com/NOSIEMPRE/Laboratorio-de-Datos)

**Step-by-step:**

1. **Setup** — Imports `statsmodels`, `pandas`, `numpy`, `matplotlib`, `pyarrow`. Defines the fork's raw parquet base URL.

2. **Download historical data** — Downloads 108 monthly parquet files from the fork (Jan 2015 – Dec 2023), covering DGT vehicle registration microdata. Total raw records: ~14.6 million.

3. **Load & Filter** — Applies the same filter chain as the fork:
   - `COD_TIPO == '40'` → passenger cars only (~10.4M records)
   - `CLAVE_TRAMITE` in `['1', '5', 'B']` → firm registrations only (~10.3M records)
   - `COD_PROPULSION_ITV == 'Electrico'` (DGT code `'6'`) → pure BEV only (113,624 records across 2015–2023)
   - 2023 annual BEV registrations: **27,928**

4. **Build monthly time series** — Aggregates by year-month → 108 monthly observations of BEV registration counts.

5. **SARIMA model** — Fits `SARIMAX(1,0,2)(1,0,1)[12]` on log-transformed monthly counts (same specification as fork). Log-transform stabilises exponential growth variance. AIC = 191.2.

6. **Extended forecast** — Forecasts 48 months ahead (Jan 2024 – Dec 2027), vs. only 12 months in the original fork. Back-transforms log-scale forecast to registration counts. Annual projections:
   - 2024: ~32,102
   - 2025: ~28,060
   - 2026: ~24,649
   - 2027: ~21,736

7. **Fleet total calculation:**

   ```text
   fleet_baseline_2023  = 113,624  (cumulative historical 2015–2023)
   projected_2024–2027  = 106,547  (SARIMA sum)
   total_ev_projected_2027 = 220,171
   ```

   Assumption: fleet ≈ cumulative registrations (justified: BEV scrappage <1%/yr, most vehicles registered post-2019).

8. **Verification** — Asserts: type is `int`, value > 0, value > 100,000.

9. **Export** — Saves full metadata to `Data/processed/m3_ev_projection.json`.

---

### 4.4 `M2_EV_Charging_Points_Baseline.ipynb` — EV Charging Points Baseline

**Status:** ✅ Complete

| Output file | Contents |
| --- | --- |
| `m2_charging_sites_interurban.csv` | 3,679 rows × 11 cols (incl. `Carretera`, `Tipo_de_via`) |
| `m2_road_coverage.csv` | 1,535 rows — per-segment nearest station distance + gap flag |
| `m2_baseline.json` | `{"total_existing_stations_baseline": 3679}` |

**Purpose:** Parse Spain's national EV charging network from the DGT DATEX2 XML feed (83.3 MB), filter to interurban sites only (within 500 m of the RTIG road network), run a road-level coverage gap analysis, and produce the baseline KPIs required for `File 1.csv` and M4.

**Step-by-step:**

1. **Setup** — Imports `xml.etree.ElementTree`, `geopandas`, `shapely`, `pandas`. Defines the DATEX2 v3 XML namespace map.

2. **Parse XML** — Iterates over all `energyInfrastructureSite` elements. Zero null coordinates across 12,074 sites — no imputation needed. Extracts: `site_id`, `name`, `lat/lon`, `operator`, `n_refill_points`, `max_power_kw` (W→kW), `connector_types`, `type_of_site`.

3. **National EDA** — Power distribution: mean 49.9 kW, median 22.2 kW, 75th percentile 50.0 kW. The median charger is AC-only — adequate for overnight parking, not for highway pit-stops. 44.2% (5,338 sites) reach DC fast ≥50 kW; only 8.8% (1,065 sites) reach HPC ≥150 kW.

4. **Interurban spatial filter** — Projects both layers to EPSG:25830. Buffers each road segment by 500 m, uses `gpd.sjoin(..., predicate='within')` with STRtree index. Sites matching multiple road buffers are deduplicated by nearest road centreline distance, and the matched road name (`Carretera`, `Tipo_de_via`) is retained for M4.
   - **Result: 3,679 interurban sites (30.5%), across 281 unique roads**

5. **Interurban power profile:**

   | Tier | Interurban | National |
   | --- | --- | --- |
   | Sub-50 kW (AC) | 38.4% | 55.8% |
   | DC fast 50–150 kW | 45.6% | 35.4% |
   | HPC ≥150 kW | **16.0% (590 sites)** | 8.8% |

   The interurban network is more advanced than the national average, but **84% of interurban sites still fall below 150 kW HPC** — the standard expected by long-distance EV drivers in 2026–2027.

6. **Road coverage gap analysis** — For each of the 1,535 RTIG road segments, finds the nearest existing station using `gpd.sjoin_nearest` (STRtree). Flags segments with no station within 50 km as gaps. Saves `m2_road_coverage.csv`.

   **Key finding: 99.6% of Spain's interurban road network is already covered.**

   | Metric | Value |
   | --- | --- |
   | Total eligible network | 29,050 km |
   | Covered (nearest station ≤50 km) | 28,920 km (99.6%) |
   | Gap (nearest station >50 km) | **130 km (0.4%)** |
   | Gap segments | **2 — N-502 (51.9 km gap) and N-502A (50.7 km gap)** |

   Next-largest near-gap corridors: N-322 (48.5 km), N-211 (45.6 km), N-111 (37.8 km).

7. **Export** — Three output files (see table above). `m2_road_coverage.csv` contains `nearest_station_m` and `has_gap` per road segment — the primary input for M4 placement logic.

**Core findings for the Analytical Report:**

> **The coverage problem is almost solved. The quality problem is not.**
>
> Spain's interurban road network is 99.6% covered by existing stations within 50 km. Only two road segments (N-502 and N-502A, ~130 km total) are true dark corridors requiring mandatory new placements. M4's primary brief is therefore **quality upgrade and densification**, not coverage expansion.
>
> **Demand sizing:** 3,679 interurban stations vs. 220,171 projected EVs in 2027 = ~60 EVs/station. Industry benchmark is 20–30:1. Implied station deficit: 3,700–7,300 additional stations.
>
> **Iberdrola's position:** Leads the interurban segment with ~22% market share (ahead of Endesa ~20% and Repsol ~17%). Existing grid connections on Iberdrola-operated corridors are a structural advantage for rapid HPC deployment.

---

## 5. Data Status Summary

| Dataset | Status | Notes |
| --- | --- | --- |
| M1 — Road Network RTIG | ✅ Done | `carreteras_RTIG.geojson` — 1,535 segments, ~29,050 km |
| M2 — EV Charging Points XML | ✅ Done | Baseline snapshot: 3,679 interurban sites. XML refreshes daily but notebook is a one-time run. |
| M3 — EV Fleet Projections | ✅ Done | `total_ev_projected_2027 = 220,171` |
| R1 — i-DE Grid Capacity | ❌ Missing | Manual download from i-DE portal required before M4 |
| R2 — Endesa Grid Capacity | ✅ Done | CSV + XLSX in `external/grid_capacity_endesa/` |
| R3 — Viesgo Grid Capacity | ❌ Missing | Manual download; fallback: generapp.eu |
| R4 — DGT Registrations | ✅ Done | 6 monthly ZIPs (Jun–Nov 2025) |
| R5 — Local Charging Points | ⚠️ Optional | Manual download from datos.gob.es |

---

## 6. Notebooks Still To Build

| Notebook | Purpose | Key Inputs | Key Output |
| --- | --- | --- | --- |
| M4 — Station Placement | Place candidate stations along eligible roads; assign grid_status | `carreteras_RTIG.geojson`, grid capacity data (R1/R2/R3), EV demand weights | `File 2.csv` |
| M5 — Friction Points | Subset File 2 where grid_status ≠ Sufficient | `File 2.csv` | `File 3.csv` |
| Final — File 1 Assembly | Combine KPIs from M2, M3, M4, M5 into single row | All notebook outputs | `File 1.csv` |
| BI Map | Interactive map colour-coded by grid_status | `File 2.csv` | Self-contained HTML map |

### Dependency chain

```text
M1 (road network)
    └─► M2 (interurban filter)  ──────────────────────────────────┐
    └─► M4 (station placement)  ◄── R1/R2/R3 (grid capacity)      │
            └─► M5 (friction points)                               │
M3 (EV fleet forecast)          ──────────────────────────────────┤
                                                                   ▼
                                                        Final Assembly → File 1.csv
                                                        (M2 + M3 + M4 + M5 KPIs)
```

**Blocking dependency:** M4 cannot start until R1 (i-DE) and R3 (Viesgo) grid data are downloaded. R2 (Endesa) is already available.

---

## 7. Key Methodology Decisions (for Analytical Report)

- **Coverage vs. quality framing:** M2 found 99.6% road coverage — M4's placement logic should be framed as capacity upgrade and densification, not gap-filling. Only N-502 and N-502A are mandatory new placements for coverage. All other proposed stations are justified on demand and quality grounds.
- **Gap threshold (50 km):** Chosen based on 300–400 km average EV range and 2–3 charging stops per long trip. Must be stated and defended in the report. Next sensitivity check: run at 30 km to capture near-gap corridors.
- **EV autonomy assumption:** Must be documented (e.g., 300–400 km average range → max station spacing ~150–200 km on any given corridor).
- **Grid status thresholds:** Team must define own thresholds for `Sufficient` / `Moderate` / `Congested` based on nearest substation's available capacity (MW) vs. estimated demand. Must be justified in the report.
- **Spatial matching methodology:** How each proposed station is matched to the nearest i-DE / Endesa / Viesgo substation — must be documented.
- **150 kW per charger:** Fixed by datathon rules. `estimated_demand_kw = n_chargers × 150`.
- **File 3 scope:** Only Moderate or Congested rows from File 2 — Sufficient locations excluded.
- **Interurban definition:** 500 m buffer around RTIG-eligible segments (AP-, A-, N- roads) in EPSG:25830.

---

*Generated for IE Sustainability Datathon March 2026 — Iberdrola Challenge.*
