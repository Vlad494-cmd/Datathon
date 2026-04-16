# IE Sustainability Datathon March 2026 — Iberdrola Challenge
## EDA Notebooks: README

> **Team Context:** Intelligent Electric Mobility — Designing Tomorrow's Charging Network  
> **Target:** Optimal placement of public EV charging stations on Spain's interurban road network for a 2027 operational scenario.

---

## Overview

This repository contains three exploratory data analysis (EDA) notebooks that form the analytical foundation of the datathon pipeline. Each notebook is self-contained but produces outputs consumed by downstream modules. They must be run **in order (M1 → M2 → M3)** before proceeding to the network optimisation model.

| Notebook | Role | Key Output |
|---|---|---|
| `M1_Road_Network_RTIG.ipynb` | Download & filter Spain's interurban road network | `carreteras_RTIG.geojson` |
| `M2_EV_Charging_Points_Baseline.ipynb` | Parse & filter national EV charging point registry | `m2_charging_sites_interurban.csv` |
| `M3_EV_Fleet_Projection_2027.ipynb` | SARIMA forecast of Spain's BEV fleet to 2027 | `m3_ev_projection.json` |

---

## Repository Structure

```
.
├── Data/
│   ├── raw/
│   │   ├── road_routes_spain/            ← M1 output
│   │   │   └── carreteras_RTIG.geojson
│   │   ├── ev_charging_points_national/  ← M2 input (download separately)
│   │   │   └── electrolineras_spain.xml
│   │   └── ev_fleet_projections_datosgob/
│   │       └── parquet/                  ← M3 downloads here
│   ├── interim/
│   │   ├── m2_charging_sites_all.csv
│   │   └── m2_charging_sites_interurban.csv
│   └── processed/
│       └── m3_ev_projection.json
│
├── M1_Road_Network_RTIG.ipynb
├── M2_EV_Charging_Points_Baseline.ipynb
├── M3_EV_Fleet_Projection_2027.ipynb
└── README.md
```

---

## Notebook Details

### M1 — Road Network RTIG

**Purpose:** Downloads Spain's RTIG (Red de Transporte de Interés General) road network from the MITMA ArcGIS REST API and filters it to only the road types eligible under datathon rules.

**Data Source:** Ministry of Transport and Sustainable Mobility (MITMA) REST API  
`https://mapas.fomento.gob.es/arcgis2/rest/services/Hermes/0_CARRETERAS/MapServer/19/query`

**Eligible road types (per datathon scope):**
- Autopistas (`AP-` roads) — toll motorways
- Autovías (`A-` roads) — free dual carriageways
- Carreteras Nacionales (`N-` roads) — national roads

**Method:**
1. Downloads the full RTIG dataset via paginated API calls (500 records/batch, ~1,602 total features)
2. Parses ESRI JSON polyline geometries into Shapely `LineString` / `MultiLineString` objects
3. Applies a two-criterion eligibility filter: `Tipo_de_via` keyword match (autopista / autovía / multicarril) OR `N-` road name prefix
4. Projects to ETRS89 UTM Zone 30N (EPSG:25830) to compute segment lengths in metres
5. Exports the filtered network in WGS84 (EPSG:4326) GeoJSON with a `length_m` column for downstream spacing logic

**Output:** `Data/raw/road_routes_spain/carreteras_RTIG.geojson`  
- ~29,050 km of eligible interurban road network
- Fields: `Carretera`, `Tipo_de_via`, `Longitud`, `length_m`, `geometry`
- CRS: EPSG:4326 (WGS84)

**Dependencies:** `geopandas`, `shapely`, `requests`, `pandas`, `numpy`, `matplotlib`

---

### M2 — EV Charging Points Baseline

**Purpose:** Parses the national EV charging point registry (DATEX2 XML format), performs exploratory analysis, and filters the full dataset to only interurban stations. Produces `total_existing_stations_baseline` for File 1.csv.

**Data Source:** DGT / MITERD via National Access Point (NAP)  
File: `Data/raw/ev_charging_points_national/electrolineras_spain.xml`  
> **Note:** This file (~80 MB, updated every 24 hours) must be downloaded separately before running M2. Run `Data/scripts/download_ev_charging_points.py` or download manually from the [NAP portal](https://nap.mitma.es/).

**Depends on:** M1 output (`carreteras_RTIG.geojson`)

**Method:**
1. Parses DATEX2 v3 XML, extracting site ID, name, coordinates, operator, refill point count, max power (kW), and connector types from each `energyInfrastructureSite` element
2. Validates coordinates within Spain's bounding box and drops nulls
3. Applies exploratory analysis: power band distribution (AC slow → ultra-fast DC), operator market share, connector type breakdown
4. Filters to interurban sites via a 500 m spatial buffer around the RTIG road network (using EPSG:25830 for metric accuracy)
5. Computes `total_existing_stations_baseline` as the unique site count within the buffer

**Key Findings:**
| Metric | Value |
|---|---|
| Total national registered sites | 12,074 |
| Interurban baseline (`total_existing_stations_baseline`) | **3,679** |
| Interurban share | 30.5% |
| DC fast (≥50 kW) interurban sites | 2,268 (61.6%) |
| HPC (≥150 kW) interurban sites | 590 (16.0%) |
| Iberdrola market share (interurban) | 22.2% (#1) |

**Outputs:**
- `Data/interim/m2_charging_sites_all.csv` — full parsed national dataset
- `Data/interim/m2_charging_sites_interurban.csv` — interurban-filtered sites with columns: `site_id`, `name`, `latitude`, `longitude`, `operator`, `n_refill_points`, `max_power_kw`, `connector_types`, `type_of_site`

**Dependencies:** `geopandas`, `shapely`, `pandas`, `numpy`, `matplotlib`, `xml.etree.ElementTree`

---

### M3 — EV Fleet Projection 2027

**Purpose:** Projects Spain's total BEV passenger car fleet to 2027 using a SARIMA model. Produces `total_ev_projected_2027`, a mandatory input for File 1.csv per datathon requirements.

**Mandatory Fork Reference:** [https://github.com/NOSIEMPRE/Laboratorio-de-Datos](https://github.com/NOSIEMPRE/Laboratorio-de-Datos)  
Original notebook: `Data Science/Ruta a la electrificación de la Movilidad/Codigo/Notebook.ipynb`  
This notebook replicates the fork's SARIMA specification and extends the forecast horizon from 12 to 48 months.

**Data Source:** DGT vehicle registration parquet files (2015–2023), downloaded directly from the fork repository.

**Method:**
1. Downloads 108 monthly parquet files (Jan 2015 – Dec 2023) from the fork's raw GitHub URL
2. Filters to: passenger cars (`COD_TIPO == '40'`), firm registrations (`CLAVE_TRAMITE` in `['1','5','B']`), pure BEV propulsion (`COD_PROPULSION_ITV == '6'` → `'Electrico'`)
3. Constructs a monthly registration time series and applies a log transform to stabilise exponential variance
4. Fits `SARIMAX(1,0,2)(1,0,1)[12]` — identical to the fork specification
5. Extends the forecast to 48 months (Jan 2024 – Dec 2027) and back-transforms from log scale
6. Computes total fleet as: `fleet_baseline_2023 (cumulative 2015–2023) + Σ projected_registrations(2024–2027)`

**Fleet assumption:** Active fleet ≈ cumulative registrations. Justified by the youth of Spain's BEV fleet (mostly post-2019), a 12–15 year average vehicle lifetime, and sub-1% BEV scrappage rate (ANFAC 2024). Resulting overestimation is <2%.

**Key Output:**

| Field | Value |
|---|---|
| `fleet_baseline_2023` (cumulative 2015–2023) | ~62,000 |
| `projected_registrations_2024_2027` | ~158,000 |
| **`total_ev_projected_2027`** | **~220,171** |

**Output:** `Data/processed/m3_ev_projection.json`  
Fields: `total_ev_projected_2027`, `fleet_baseline_2023`, `projected_registrations_2024_2027`, `annual_forecast` (year-by-year), `model`, `train_range`, `fork`, `generated_at`

**Dependencies:** `statsmodels`, `pandas`, `numpy`, `matplotlib`, `requests`

---

## Execution Order & Dependencies

```
M1_Road_Network_RTIG.ipynb
        │
        └──► carreteras_RTIG.geojson
                    │
                    └──► M2_EV_Charging_Points_Baseline.ipynb
                                    │
                                    └──► m2_charging_sites_interurban.csv
                                                        │
                                         (used by downstream optimisation)

M3_EV_Fleet_Projection_2027.ipynb  (independent, no M1/M2 dependency)
        │
        └──► m3_ev_projection.json
                    │
                    └──► File 1.csv  (total_ev_projected_2027)
```

> M3 can be run in parallel with M1/M2. All three must complete before running the network optimisation notebook (M4).

---

## Environment Setup

All notebooks are designed for **Google Colab**. Install dependencies by uncommenting the `!pip install` cell at the top of each notebook.

```bash
# M1 / M2
pip install geopandas shapely requests matplotlib

# M3
pip install statsmodels pandas numpy matplotlib pyarrow
```

---

## Datathon Compliance Notes

- All notebooks follow evaluation criterion **T5** (code quality & reproducibility): cells alternate between code and explanatory markdown, and all outputs include a printed verification block confirming file structure, row counts, column names, and data types.
- The 500 m interurban buffer methodology (M2) and fleet approximation assumption (M3) are both documented inline per criterion **T1** (assumptions & justification).
- M3 explicitly references the mandatory datos.gob.es fork URL in both code and markdown cells per datathon requirements.
- All geometries use **WGS84 (EPSG:4326)** as the output CRS; metric projections (EPSG:25830) are used only for intermediate distance/area calculations.
