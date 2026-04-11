# IE Sustainability Datathon - March 2026
## Intelligent Electric Mobility: Designing Tomorrow's Charging Network
**Partner:** Iberdrola | **Organizer:** IE University

---

## Challenge Overview

Design a data-driven EV charging network for Spain's interurban road system (2027 scenario).

- **Primary objective:** Propose optimal charging station locations on autopistas, autovías, and carreteras nacionales — minimizing stations while covering demand.
- **Secondary objective:** Identify "friction points" where grid capacity constraints make deployment unfeasible or risky.

---

## Repository Structure

```
├── Data/
│   ├── raw/                              # Original source data (see download instructions below)
│   │   ├── road_routes_spain/            # M1: MITMA RTIG road network (REST API download)
│   │   ├── ev_charging_points_national/  # M2: DGT DATEX2 XML — gitignored (re-downloadable)
│   │   ├── ev_fleet_projections_datosgob/  # M3: datos.gob.es EV projection parquets
│   │   ├── dgt_vehicle_registrations/    # R4: DGT monthly ZIPs — gitignored (re-downloadable)
│   │   └── ev_charging_points_local/     # R5: Local/municipal datasets (manual download)
│   ├── external/                         # Third-party grid capacity data
│   │   ├── grid_capacity_ide_iberdrola/  # R1: i-DE substations (manual download)
│   │   ├── grid_capacity_endesa/         # R2: Endesa node capacity — tracked in git
│   │   └── grid_capacity_viesgo/         # R3: Viesgo substations (manual download)
│   ├── interim/                          # Cleaned intermediate files — gitignored
│   ├── processed/                        # Model-ready outputs — gitignored
│   ├── scripts/                          # Bash scripts for automated downloads
│   └── metadata/
├── notebooks/
│   ├── Dataset_setup.ipynb               # Full dataset inventory and preprocessing guide
│   ├── M1_Road_Network_RTIG.ipynb        # Road network download and filtering
│   ├── M3_EV_Fleet_Projection_2027.ipynb # SARIMA EV fleet projection to 2027
│   └── (M2, M4, M5 — in progress)
├── references/
│   └── dataset_download_workaround.txt   # REST API workaround for MITMA portal outages
├── IE_Iberdrola_Datathon_guidelines.txt  # Official challenge guidelines
└── IE-Iberdrola Datathon Marzo 2026.pdf  # Challenge brief PDF
```

---

## Data Setup

Some datasets are excluded from git (large files, re-downloadable). See [notebooks/Dataset_setup.ipynb](notebooks/Dataset_setup.ipynb) for full instructions on what to download and where to place it.

**Quick-start checklist:**
1. Run `notebooks/M3_EV_Fleet_Projection_2027.ipynb` → downloads parquets from the [mandatory fork](https://github.com/Jvilpi/Laboratorio-de-Datos) and exports `Data/processed/m3_ev_projection.json`
2. Run `notebooks/M1_Road_Network_RTIG.ipynb` → fetches road network via MITMA REST API and exports `Data/raw/road_routes_spain/carreteras_RTIG.geojson` (see `references/dataset_download_workaround.txt` if the portal is unavailable)
3. Download i-DE capacity map → `Data/external/grid_capacity_ide_iberdrola/`
4. Download Viesgo capacity → `Data/external/grid_capacity_viesgo/`
5. Run scripts in `Data/scripts/` to refresh large re-downloadable files

---

## Challenge Deliverables

| Deliverable | Description |
|---|---|
| `File 1.csv` | Global Network KPIs (1 summary row) |
| `File 2.csv` | Proposed charging locations (1 row per station) |
| `File 3.csv` | Friction points — grid-constrained locations from File 2 |
| Colab notebook | Documented analysis with all outputs visible |
| BI map | Self-contained interactive map (colour-coded by grid status) |
| Analytical Report | 3–5 page executive summary |
| Final Pitch | 5-minute PPT/PDF presentation (finalist teams only) |
