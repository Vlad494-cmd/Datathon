# DATASETS SETUP — IE Iberdrola Datathon March 2026
## Intelligent Electric Mobility: Designing Tomorrow's Charging Network

> **Last updated:** March 10, 2026
> **Project:** IE Sustainability Datathon — Iberdrola Challenge
> **Target year:** 2027 operational scenario
> **Geography:** Interurban road network of Spain (autopistas, autovías, carreteras nacionales)

---

## Table of Contents

1. [Dataset Inventory](#1-dataset-inventory)
2. [Folder Structure](#2-folder-structure)
3. [Automated Downloads Summary](#3-automated-downloads-summary)
4. [Manual Download Instructions](#4-manual-download-instructions)
5. [Data Formats and Notes](#5-data-formats-and-notes)
6. [Preprocessing Requirements](#6-preprocessing-requirements)
7. [Additional Recommended Datasets](#7-additional-recommended-datasets)

---

## 1. Dataset Inventory

### Mandatory Datasets

| # | Dataset Name | Type | Provider | Access | Format | Status | Purpose |
|---|---|---|---|---|---|---|---|
| M1 | Road Routes — Spanish Interurban Network | Geospatial / Transport | Ministry of Transport (MITMA) via CNIG/IGN | Manual download | SHP / GeoPackage | ⚠️ Manual required | Map autopistas, autovías, carreteras nacionales; structural backbone of proposed network |
| M2 | EV Charging Points — National | EV Infrastructure | DGT / MITERD via NAP | Direct download ✅ | DATEX2 XML | ✅ Downloaded | Existing infrastructure baseline; identify coverage gaps; avoid redundancy |
| M3 | EV Fleet Projections — datos.gob.es | EV Demand / Forecasting | datos.gob.es / Admindatosgobes | GitHub fork | Jupyter Notebook | ⚠️ Fork required | **Mandatory foundational input** — projected total EV fleet in Spain for 2027 (Exercise 3 output) |

### Recommended / Additional Official Datasets

| # | Dataset Name | Type | Provider | Access | Format | Status | Purpose |
|---|---|---|---|---|---|---|---|
| R1 | Grid Capacity — i-DE / Iberdrola | Electrical Grid | i-DE (Iberdrola Group) | Manual (interactive map + download) | XLSX / CSV / Interactive map | ⚠️ Manual required | Substation-level available capacity (MW) + coordinates for Iberdrola's distribution zone |
| R2 | Grid Capacity — Endesa (e-distribución) | Electrical Grid | Endesa e-distribución | Direct download ✅ | XLSX + CSV | ✅ Downloaded | Node-level access capacity for Endesa's distribution zone; CSV + XLSX available |
| R3 | Grid Capacity — Viesgo | Electrical Grid | Viesgo Distribución | Manual (interactive map) | Interactive / PDF | ⚠️ Manual required | Substation-level capacity for northern Spain (Viesgo distribution zone) |
| R4 | DGT Vehicle Registrations (monthly) | Vehicle Registration | DGT (Dirección General de Tráfico) | Direct download ✅ | ZIP (CSV inside) | ✅ Downloaded (6 months) | Monthly EV registration trends by province for geographic demand weighting |
| R5 | Local EV Charging Points — datos.gob.es | EV Infrastructure (local) | datos.gob.es (various municipalities) | Direct download | CSV / GeoJSON / SHP | ⚠️ Optional manual | Local/municipal datasets to validate national figures and find unregistered regional chargers |

---

## 2. Folder Structure

```
data/
├── raw/                              ← Original files, never modified
│   ├── road_routes_spain/            ← M1: Ministry of Transport road network SHP
│   ├── ev_charging_points_national/  ← M2: DGT DATEX2 XML (national charging points)
│   ├── ev_fleet_projections_datosgob/← M3: datos.gob.es EV projection repository
│   ├── dgt_vehicle_registrations/    ← R4: DGT monthly registration ZIPs
│   └── ev_charging_points_local/     ← R5: Local/municipal charging point datasets
│
├── external/                         ← Third-party datasets not generated internally
│   ├── grid_capacity_ide_iberdrola/  ← R1: i-DE substation capacity data
│   ├── grid_capacity_endesa/         ← R2: Endesa node-level capacity CSV/XLSX
│   └── grid_capacity_viesgo/         ← R3: Viesgo substation capacity data
│
├── interim/                          ← Cleaned/intermediate data (temporary)
├── processed/                        ← Model-ready datasets (final outputs)
│
├── metadata/
│   └── DATASETS_SETUP.md             ← This file
│
└── scripts/
    ├── download_dgt_registrations.sh
    ├── download_ev_charging_national.sh
    ├── download_endesa_grid_capacity.sh
    └── clone_datosgob_ev_repo.sh
```

---

## 3. Automated Downloads Summary

### ✅ Successfully Downloaded

| File | Location | Size | Notes |
|---|---|---|---|
| `electrolineras_spain.xml` | `raw/ev_charging_points_national/` | ~80 MB | DATEX2 v3 XML, updated every 24 hours |
| `export_mensual_mat_202506.zip` | `raw/dgt_vehicle_registrations/` | ~17 MB | Jun 2025 registrations |
| `export_mensual_mat_202507.zip` | `raw/dgt_vehicle_registrations/` | ~17 MB | Jul 2025 registrations |
| `export_mensual_mat_202508.zip` | `raw/dgt_vehicle_registrations/` | ~11 MB | Aug 2025 registrations |
| `export_mensual_mat_202509.zip` | `raw/dgt_vehicle_registrations/` | ~14 MB | Sep 2025 registrations |
| `export_mensual_mat_202510.zip` | `raw/dgt_vehicle_registrations/` | ~16 MB | Oct 2025 registrations |
| `export_mensual_mat_202511.zip` | `raw/dgt_vehicle_registrations/` | ~15 MB | Nov 2025 registrations |
| `2026_03_04_R1299_demanda.csv` | `external/grid_capacity_endesa/` | ~226 KB | Endesa e-distribución demand capacity (Mar 2026) |
| `2026_03_04_R1299_demanda.xlsx` | `external/grid_capacity_endesa/` | ~193 KB | Endesa e-distribución demand capacity (Mar 2026) |

**Re-download scripts:** See `data/scripts/` for bash scripts to refresh any of the above.

---

## 4. Manual Download Instructions

### M1 — Road Routes | CNIG / Ministry of Transport

**Purpose:** Spatial backbone of the charging network. Required to identify autopistas, autovías, and carreteras nacionales, map route segments, and geolocate proposed stations.

**Provider:** Instituto Geográfico Nacional (IGN) / Centro Nacional de Información Geográfica (CNIG)
**Official page:** https://centrodedescargas.cnig.es/CentroDescargas/redes-transporte
**Alternative (datos.gob.es):** https://datos.gob.es/en/catalogo/e00125901-transporte
**Ministry catalog:** https://www.transportes.gob.es/carreteras/catalogo-y-evolucion-de-la-red-de-carreteras

**Steps to download:**

1. Go to: https://centrodedescargas.cnig.es/CentroDescargas/redes-transporte
2. Select **"Red de Transporte de España"** (Spain Transport Networks)
3. Choose download coverage:
   - **Option A:** National coverage (4 thematic files — recommended)
     - Interurban road network
     - Kilometer points
     - Road network infrastructure
     - Highway catalog
   - **Option B:** By province (52 files)
4. Select **format:** SHP (Shapefile) or GeoPackage
5. Accept the terms and download
6. Place all files in: `data/raw/road_routes_spain/`

**Key layers to use:**
- `red_vial_interurbana` — Interurban road network (contains `autopistas`, `autovías`, `carreteras nacionales`)
- Road classification field to filter: road type attribute

**Latest version:** May 2025 (includes updates to autopistas A-7, highway reclassifications)
**License:** Free, IGN Open Data License
**Format:** SHP or GeoPackage (with .shp, .dbf, .shx, .prj files)

---

### M3 — EV Fleet Projections | datos.gob.es Mandatory Repository

**Purpose:** Provides the **projected total EV fleet in Spain for 2027** — mandatory foundational input for all demand models. Teams MUST fork this repository.

**Repository:** https://github.com/Admindatosgobes/Laboratorio-de-Datos
**Direct notebook path:** `Data Science/Ruta a la electrificación de la Movilidad/Codigo/Notebook.ipynb`
**Open in Colab:** https://colab.research.google.com/github/Admindatosgobes/Laboratorio-de-Datos/blob/main/Data%20Science/Ruta%20a%20la%20electrificaci%C3%B3n%20de%20la%20Movilidad/Codigo/Notebook.ipynb
**Article:** https://datos.gob.es/en/conocimiento/road-electrification-deciphering-electric-vehicle-growth-spain-through-data-analytics

**Steps to fork and use:**

1. Go to: https://github.com/Admindatosgobes/Laboratorio-de-Datos
2. Click **"Fork"** (top-right corner) — create a fork under your own GitHub account
3. Clone YOUR fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Laboratorio-de-Datos.git \
     data/raw/ev_fleet_projections_datosgob/Laboratorio-de-Datos
   ```
4. Open the notebook:
   `Data Science/Ruta a la electrificación de la Movilidad/Codigo/Notebook.ipynb`
5. Run **Exercise 3 (Open Data)** — the output is the projected EV fleet growth figure for 2027
6. Use this output as `total_ev_projected_2027` in File 1.csv

**CRITICAL:** Reference YOUR fork URL (not the original) in both the Colab notebook and Analytical Report.

---

### R1 — Grid Capacity | i-DE (Iberdrola Distribution)

**Purpose:** Substation-level available consumption capacity (MW) with geographic coordinates for Iberdrola's distribution zone (central and eastern Spain).

**Official page:** https://www.i-de.es/conexion-red-electrica/suministro-electrico/mapa-capacidad-consumo
**English version:** https://www.i-de.es/grid-connection/energy-generation/capacity-map

**Steps to access data:**

1. Go to: https://www.i-de.es/conexion-red-electrica/suministro-electrico/mapa-capacidad-consumo
2. The page displays an interactive map of substation capacity
3. Look for a **"Descargar datos"** (Download data) or **"Fichero"** button
4. If a downloadable file is available (XLSX/CSV), download it
5. **If no direct download:** Use the interactive map to manually note capacity values for substations nearest to your proposed charging locations
6. Alternatively, check CNMC's unified capacity platform: https://www.generapp.eu/mapa-de-capacidades/
7. Place any downloaded files in: `data/external/grid_capacity_ide_iberdrola/`

**Key field needed:**
`Capacidad disponible / Available capacity (MW)` per substation
Used for `grid_status` classification in File 2 and File 3

**Notes:**
- i-DE is obligated by CNMC Circular 1/2024 to publish this data
- If the download portal is temporarily unavailable (HTTP 503), retry later
- The map may only allow per-substation queries by clicking on the map

---

### R3 — Grid Capacity | Viesgo Distribución

**Purpose:** Substation-level capacity for Viesgo's distribution zone (northern Spain: Cantabria, Asturias, parts of Castilla y León).

**Official page:** https://www.viesgodistribucion.com/mapa-interactivo-de-la-red
**Alternative (customer):** https://www.viesgodistribucion.com/soy-cliente/mapa-interactivo-de-la-red
**Installer access:** https://www.viesgodistribucion.com/soy-instalador/mapa-interactivo-de-la-red

> **⚠️ Important:** Viesgo was acquired by **E.ON España**. The distribution entity may now operate under **E.ON Distribución** or **Edistribución Norte**. If the Viesgo URLs above are unavailable, search for "E.ON distribución mapa capacidad acceso" or check the unified CNMC platform below.

**Steps to access data:**

1. Try: https://www.viesgodistribucion.com/mapa-interactivo-de-la-red
2. If redirected, search "E.ON distribución capacidad acceso" to find the new URL
3. Use the interactive map to explore substations for northern interurban routes (A-8 Autovía del Cantábrico, A-67, N-621, N-634)
4. Download capacity data file if available (CSV/XLSX/PDF)
5. **Best fallback:** Use the unified CNMC capacity platform (aggregates ALL 29 distributors including Viesgo/E.ON):
   - https://www.generapp.eu/mapa-de-capacidades/
   - Filter by operator "Viesgo" or by geographic zone (northern Spain)
   - Reference date: December 1, 2025 data available (97% of customers covered)
6. Place downloaded files in: `data/external/grid_capacity_viesgo/`

**Coverage:** Cantabria, Asturias, northern Castilla y León
**Distributor code:** Used for `distributor_network = "Viesgo"` in File 3.csv

---

### R5 — Local EV Charging Points | datos.gob.es

**Purpose:** Validate national charging point figures against local/municipal datasets. Identify unregistered or locally-documented chargers.

**Portal:** https://datos.gob.es
**Search URL:** https://datos.gob.es/es/catalogo?q=puntos+recarga+electrico

**Relevant datasets found:**

| Dataset | Publisher | Format | URL |
|---|---|---|---|
| Puntos de recarga de vehículos eléctricos | Comunidad Foral de Navarra | SHP | https://datos.gob.es/es/catalogo/a15002917-puntos-de-recarga-de-vehiculos-electricos1 |
| Electrolineras | Diputación Provincial de Castelló | JSON, CSV, ZIP | https://datos.gob.es/es/catalogo/l02000012-electrolineras |
| Registro de Instalaciones de Recarga (La Rioja) | Gobierno de La Rioja | XLS, CSV, JSON | https://datos.gob.es/es/catalogo/a17002943-puntos-de-recarga-de-coches-electricos |
| Red de recarga de Vehículos Eléctricos (La Palma) | Cabildo de La Palma | GeoJSON, CSV, SHP | https://datos.gob.es/es/catalogo/l03380010-red-de-recarga-de-vehiculos-electricos |

**Steps:**
1. Visit each dataset page above
2. Click the desired format (CSV or GeoJSON preferred)
3. Place files in: `data/raw/ev_charging_points_local/`

---

## 5. Data Formats and Notes

### M2 — EV Charging Points XML (DATEX2)

- **Format:** DATEX2 v3 XML (~80 MB)
- **Standard:** European DATEX2 standard for traffic/mobility data
- **Parsing:** Use Python `lxml` or `xml.etree.ElementTree` to parse
- **Key elements:** `energyInfrastructureSite`, `location` (coordinates), `chargerType`, `powerRating`
- **Update frequency:** Every 24 hours — re-download before final analysis
- **Filter for interurban only:** Cross-reference coordinates with road routes shapefile to keep only stations on autopistas/autovías/carreteras nacionales

### R4 — DGT Vehicle Registrations

- **Format:** ZIP files containing semicolon-delimited CSV
- **Encoding:** ISO-8859-1 (Latin-1) — use `encoding='latin1'` in pandas
- **Key fields:** `TIPO_VEHICULO`, `COMBUSTIBLE`, `PROVINCIA_MATRICULACION`, `FECHA_MATRICULACION`
- **EV filter:** Filter on `COMBUSTIBLE` = 'ELECTRICO' or 'HIBRIDO ENCHUFABLE'
- **Purpose:** Count EV registrations by province to weight spatial demand forecasts

### R2 — Endesa Grid Capacity

- **Format:** CSV + XLSX (monthly updates)
- **Key fields:** Node ID, substation name, municipality, latitude, longitude, available capacity (MW), voltage level
- **Coverage:** Endesa distribution zone (Andalucía, Extremadura, Cataluña, Canarias, Baleares, parts of Aragón and Castilla-La Mancha)
- **Spatial matching:** Use lat/lon fields to find nearest substation to each proposed charging location

### M1 — Road Routes SHP

- **Format:** Shapefile (.shp + .dbf + .shx + .prj)
- **CRS:** ETRS89 (EPSG:25830) — reproject to WGS84 (EPSG:4326) for this project
- **Key attribute:** Road type / classification to filter: autopistas (AP-), autovías (A-), carreteras nacionales (N-)
- **Suggested tool:** GeoPandas (`gpd.read_file()`)

---

## 6. Preprocessing Requirements

### Step 1 — Parse EV Charging XML → CSV

```python
import xml.etree.ElementTree as ET
import pandas as pd

# Parse DATEX2 XML
tree = ET.parse('data/raw/ev_charging_points_national/electrolineras_spain.xml')
root = tree.getroot()
# Extract sites with coordinates and charger attributes
# Filter: keep only interurban stations (cross-reference with road SHP)
```

### Step 2 — Unzip and Filter DGT Registrations

```python
import zipfile, pandas as pd, glob

records = []
for zf in glob.glob('data/raw/dgt_vehicle_registrations/*.zip'):
    with zipfile.ZipFile(zf) as z:
        for fname in z.namelist():
            if fname.endswith('.txt') or fname.endswith('.csv'):
                with z.open(fname) as f:
                    df = pd.read_csv(f, sep=';', encoding='latin1', low_memory=False)
                    ev = df[df['COMBUSTIBLE'].isin(['ELECTRICO', 'HIBRIDO ENCHUFABLE'])]
                    records.append(ev)
ev_registrations = pd.concat(records)
ev_registrations.to_csv('data/interim/ev_registrations_2025.csv', index=False)
```

### Step 3 — Load Road Network (Shapefile)

```python
import geopandas as gpd

roads = gpd.read_file('data/raw/road_routes_spain/red_vial_interurbana.shp')
roads = roads.to_crs('EPSG:4326')  # Reproject to WGS84
# Filter interurban: autopistas (AP-), autovias (A-), carreteras nacionales (N-)
interurban = roads[roads['road_type'].isin(['autopista', 'autovia', 'carretera_nacional'])]
```

### Step 4 — Load Grid Capacity (Endesa)

```python
import pandas as pd

endesa = pd.read_csv(
    'data/external/grid_capacity_endesa/2026_03_04_R1299_demanda.csv',
    encoding='utf-8', sep=';'
)
# Key columns: coordinates, available_capacity_mw
# Use to assign grid_status to each proposed charging location
```

### Step 5 — Run datos.gob.es EV Projection Notebook

1. Open the Colab notebook (see M3 instructions above)
2. Run all cells through Exercise 3
3. Extract the `total_ev_projected_2027` value
4. Use this directly in `File 1.csv`

---

## 7. Additional Recommended Datasets

The following public datasets can strengthen the model and are positively scored:

| # | Dataset | Provider | URL | Type | Coverage | Why Useful |
|---|---|---|---|---|---|---|
| A1 | PMUS / Traffic Intensity (IMD) — Estado | MITMA | https://www.transportes.gob.es/carreteras/nuestra-red/movilidad/mapas-trafico | Traffic flow | Spain (state roads) | Annual average daily traffic per road segment; directly informs demand weighting per corridor |
| A2 | AEMET Open Data — Climate/Weather | AEMET | https://opendata.aemet.es/opendata/api/ | Climate | All Spain | Seasonal temperature and weather affect EV battery range; important for seasonal demand modeling |
| A3 | ESIOS — Red Eléctrica de España (REE) | REE | https://www.esios.ree.es/es/descargas | Grid / Energy | Spain | Transmission network data, demand curves, and grid topology complement distribution-level capacity from i-DE/Endesa/Viesgo |
| A4 | OpenStreetMap — Spain Road Network | OpenStreetMap | https://download.geofabrik.de/europe/spain.html | Geospatial | Spain | Free, detailed road network with POI data; useful cross-reference for road classification and nearby services |
| A5 | ACEA — European EV Market Data | ACEA | https://www.acea.auto/stats/share-of-electric-cars-in-new-registrations/ | EV Market | Europe | European EV adoption benchmarks for modeling Spain's 2027 EV penetration scenarios |
| A6 | Catastro Inmobiliario (Building Footprints) | Dirección General del Catastro | https://www.sedecatastro.gob.es/ | Geospatial | Spain | Identify highway service areas, rest stops, and commercial zones suitable for charging stations |
| A7 | EMT/Interurban Bus Stop Locations | MITMA / Regional | https://datos.gob.es | Transport Nodes | Spain | Identify high-traffic transit nodes where EV charging co-location maximises utilisation |
| A8 | Observatorio del Vehículo (ANFAC) | ANFAC | https://www.anfac.com/estadisticas/ | EV Fleet | Spain | Detailed EV fleet statistics by region and vehicle category; validates datos.gob.es projections |
| A9 | CNMC Capacity Unified Platform | CNMC / Third-party | https://www.generapp.eu/mapa-de-capacidades/ | Electrical Grid | Spain | Aggregates ALL 29 distributors' capacity maps in one place — excellent for quick spatial queries |
| A10 | Eurostat — Electric Road Vehicles | Eurostat | https://ec.europa.eu/eurostat/statistics-explained/index.php/Electric_vehicles | EV Statistics | EU | EU-level EV statistics for contextualising Spain's trajectory and validating 2027 projections |

---

## Quick-Start Checklist

```
[ ] 1. Run: data/scripts/clone_datosgob_ev_repo.sh (or fork manually)
[ ] 2. Run Exercise 3 in the datos.gob.es Colab notebook → get total_ev_projected_2027
[ ] 3. Download road network from CNIG → data/raw/road_routes_spain/
[ ] 4. Verify: data/raw/ev_charging_points_national/electrolineras_spain.xml exists
[ ] 5. Verify: data/raw/dgt_vehicle_registrations/ has 6 ZIP files
[ ] 6. Download i-DE capacity map → data/external/grid_capacity_ide_iberdrola/
[ ] 7. Verify: data/external/grid_capacity_endesa/ has CSV + XLSX files
[ ] 8. Download Viesgo capacity → data/external/grid_capacity_viesgo/
[ ] 9. (Optional) Download local EV charging datasets → data/raw/ev_charging_points_local/
[ ] 10. Run preprocessing scripts to convert raw data to interim/processed formats
```

---

*Documentation generated for IE Sustainability Datathon March 2026 — Iberdrola Challenge.*
