# IE Sustainability Datathon — March 2026
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
│   │   ├── road_routes_spain/            # M1: Ministry of Transport road network (manual download)
│   │   ├── ev_charging_points_national/  # M2: DGT DATEX2 XML — gitignored (re-downloadable)
│   │   ├── ev_fleet_projections_datosgob/  # M3: datos.gob.es EV projection notebook
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
├── Dataset_setup.ipynb                   # Full dataset inventory and preprocessing guide
├── IE_Iberdrola_Datathon_guidelines.txt  # Official challenge guidelines
└── IE-Iberdrola Datathon Marzo 2026.pdf  # Challenge brief PDF
```

---

## Data Setup

Some datasets are excluded from git (large files, re-downloadable). See [Dataset_setup.ipynb](Dataset_setup.ipynb) for full instructions on what to download and where to place it.

**Quick-start checklist:**
1. Fork the [datos.gob.es repository](https://github.com/Admindatosgobes/Laboratorio-de-Datos) and run Exercise 3 → get `total_ev_projected_2027`
2. Download the road network SHP from [CNIG](https://centrodedescargas.cnig.es/CentroDescargas/redes-transporte) → `Data/raw/road_routes_spain/`
3. Download i-DE capacity map → `Data/external/grid_capacity_ide_iberdrola/`
4. Download Viesgo capacity → `Data/external/grid_capacity_viesgo/`
5. Run scripts in `Data/scripts/` to refresh large re-downloadable files

---

## Challenge Deliverables (to be produced)

The following outputs must be submitted as part of the datathon final submission:

| Deliverable | Description |
|---|---|
| `File 1.csv` | Global Network KPIs (1 summary row) |
| `File 2.csv` | Proposed charging locations (1 row per station) |
| `File 3.csv` | Friction points — grid-constrained locations from File 2 |
| Colab notebook | Documented analysis with all outputs visible |
| BI map | Self-contained interactive map (colour-coded by grid status) |
| Analytical Report | 3–5 page executive summary |
| Final Pitch | 5-minute PPT/PDF presentation (finalist teams only) |
