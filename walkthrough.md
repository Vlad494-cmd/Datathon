# IE Iberdrola Datathon — Project Walkthrough
# IE Iberdrola Datathon — 项目详解

> **Updated / 更新日期:** 2026-04-13  
> **Branch / 分支:** EDA  
> **Challenge / 赛题:** Intelligent Electric Mobility — Designing Spain's 2027 EV Charging Network

---

## 1. Challenge Overview / 赛题概述

**EN:** Design a data-driven public EV charging network for Spain's interurban road system (autopistas, autovías, carreteras nacionales), targeting a 2027 operational scenario. The challenge has two core objectives:
1. **Network Optimisation (Primary):** Propose the minimum number of charging stations that adequately cover interurban demand — maximising utilisation while minimising capital expenditure.
2. **Grid Viability (Secondary):** Identify "friction points" where electrical grid constraints make deployment infeasible or risky.

**ZH:** 基于数据为西班牙城际公路网络（高速公路、快速路、国道）设计一套 2027 年场景下的公共电动汽车充电网络。赛题有两个核心目标：
1. **网络优化（主要目标）：** 提出能充分覆盖城际需求、数量最少的充电站选址方案——最大化利用率，最小化资本支出。
2. **电网可行性分析（次要目标）：** 识别因电网容量限制而无法或高风险部署的"摩擦点"。

---

## 2. Required Deliverables / 必交成果

| # | Deliverable / 成果 | Description / 说明 |
|---|---|---|
| 1 | `File 1.csv` | 1 summary row — global network KPIs / 1行汇总：全网关键指标 |
| 2 | `File 2.csv` | 1 row per proposed charging station / 每个提议充电站1行 |
| 3 | `File 3.csv` | Friction points only (grid_status ≠ Sufficient) / 仅摩擦点（非充足容量） |
| 4 | Colab Notebook | All cells executed, all outputs visible / 所有单元格已运行，输出可见 |
| 5 | BI Map | Self-contained interactive map, colour-coded by grid status / 自包含交互地图，按电网状态着色 |
| 6 | Analytical Report | 3–5 page executive summary / 3–5页执行摘要 |
| 7 | Final Pitch | 5-min PPT/PDF (finalist teams only) / 5分钟PPT（决赛队伍） |

### Key Technical Constants / 关键技术常量
- **Standard charger power / 标准充电功率:** 150 kW (fixed, no exceptions / 固定，不可更改)
- **estimated_demand_kw formula:** `n_chargers_proposed × 150`
- **Coordinate system / 坐标系:** WGS84 decimal degrees
- **grid_status values:** `Sufficient` | `Moderate` | `Congested`
- **distributor_network values:** `i-DE` | `Endesa` | `Viesgo`

---

## 3. Repository Structure / 仓库结构

```
Datathon/
├── Data/
│   ├── raw/
│   │   ├── road_routes_spain/             ← M1: 道路网络 GeoJSON（已生成）
│   │   ├── ev_charging_points_national/   ← M2: DGT DATEX2 XML（需重新下载）
│   │   ├── ev_fleet_projections_datosgob/ ← M3: datos.gob.es 预测数据（parquet已下载）
│   │   ├── dgt_vehicle_registrations/     ← R4: DGT 月度注册数据 ZIP（6个月，已下载）
│   │   └── ev_charging_points_local/      ← R5: 本地充电点数据（可选，待下载）
│   ├── external/
│   │   ├── grid_capacity_ide_iberdrola/   ← R1: i-DE 变电站容量（待手动下载）
│   │   ├── grid_capacity_endesa/          ← R2: Endesa 节点容量 CSV/XLSX（已下载）
│   │   └── grid_capacity_viesgo/          ← R3: Viesgo 变电站容量（待手动下载）
│   ├── interim/                           ← 中间清洗文件（gitignored）
│   ├── processed/                         ← 模型输出文件（gitignored）
│   ├── metadata/DATASETS_SETUP.md        ← 完整数据集说明文档
│   └── scripts/                           ← bash 自动下载脚本
├── notebooks/
│   ├── Dataset_setup.ipynb                ← 数据清单与预处理指南
│   ├── M1_Road_Network_RTIG.ipynb         ← ✅ 完成：道路网络下载与过滤
│   ├── M3_EV_Fleet_Projection_2027.ipynb  ← ✅ 完成：SARIMA EV 队列预测
│   └── (M2, M4, M5 — 待完成)
├── references/
│   └── dataset_download_workaround.txt    ← MITMA REST API 绕过方法
├── IE_Iberdrola_Datathon_guidelines.txt   ← 官方赛题指南
└── walkthrough.md                         ← 本文件
```

---

## 4. Notebook Walkthroughs / 各 Notebook 详解

---

### 4.1 `Dataset_setup.ipynb` — Data Inventory & Setup Guide / 数据清单与配置指南

**EN:** This is a documentation notebook (no code execution required). It mirrors `Data/metadata/DATASETS_SETUP.md` and serves as the team's reference for:
- Which datasets are mandatory vs. recommended
- Where each dataset lives in the folder structure
- How to download datasets that are not tracked in git
- Preprocessing snippets for each format (XML, ZIP/CSV, SHP, XLSX)
- A quick-start checklist

**ZH:** 这是一个纯文档 notebook（无需执行代码）。内容与 `Data/metadata/DATASETS_SETUP.md` 完全一致，作为团队的参考手册，涵盖：
- 哪些数据集是强制的，哪些是推荐的
- 每个数据集在文件夹中的位置
- 如何下载 git 未追踪的数据集
- 各格式（XML、ZIP/CSV、SHP、XLSX）的预处理代码片段
- 快速启动清单

---

### 4.2 `M1_Road_Network_RTIG.ipynb` — Road Network Download & Filter / 道路网络下载与过滤

**Status / 状态:** ✅ Complete — output already saved to `Data/raw/road_routes_spain/carreteras_RTIG.geojson`

**EN:**

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

**ZH:**

**目的：** 从西班牙交通部（MITMA）REST API 下载城际道路网络，过滤出合规道路类型，导出 GeoJSON 供 M4 使用。

**逐步说明：**

1. **初始化** — 导入 `geopandas`、`shapely`、`requests`、`matplotlib`。定义 RTIG 数据集的 ArcGIS REST API 端点（共 1,602 条记录）。MITMA 直接下载门户正在维护中，REST API 是绕过方案（见 `references/dataset_download_workaround.txt`）。

2. **下载** — 每批500条分页请求（4批），直接请求 WGS84 坐标（`outSR=4326`）。成功下载全部 1,602 条记录。

3. **构建 GeoDataFrame** — 将 ESRI JSON 折线要素解析为 Shapely `LineString`/`MultiLineString` 对象，创建 CRS 为 EPSG:4326 的 GeoDataFrame。

4. **探索道路类型** — 检查 `Tipo_de_via` 字段，共5类：
   - `Autopista libre\Autovía`（534段）——免费高速
   - `Autopista peaje`（79段）——收费高速
   - `Multicarril`（189段）——多车道
   - `Carretera convencional`（789段）——常规道路（含N-国道）
   - `NaN`（11段）

5. **资格过滤** — 双重OR过滤：
   - `Tipo_de_via` 包含 `autopista`、`autov` 或 `multicarril` → 捕获AP-和A-类道路
   - `Carretera` 以 `N-` 开头 → 捕获国道（归类为"常规道路"）
   - 结果：**保留 1,535 段**，排除 67 段，423 个唯一道路名称

6. **网络汇总** — 合规网络总长：**约 29,050 km**。最长道路：AP-7N（849 km）、A-66（689 km）、N-630（669 km）、A-4（583 km）。

7. **可视化** — 按道路类型着色绘图，作为合理性检查。

8. **导出** — 保存至 `Data/raw/road_routes_spain/carreteras_RTIG.geojson`（约73 MB）。新增 `length_m` 列（以 EPSG:25830 计算），供 M4 布置充电站间距时使用。

9. **验证** — 从磁盘重新加载并断言：记录数>0、CRS=EPSG:4326、无空几何、坐标在西班牙范围内。

---

### 4.3 `M3_EV_Fleet_Projection_2027.ipynb` — SARIMA EV Fleet Forecast / SARIMA 电动汽车队列预测

**Status / 状态:** ✅ Complete — output saved to `Data/processed/m3_ev_projection.json`  
**Key output / 关键输出:** `total_ev_projected_2027 = 220,171`

**EN:**

**Purpose:** Project the total BEV fleet in Spain for 2027 — a mandatory input for `File 1.csv` (`total_ev_projected_2027`). Replicates and extends the SARIMA methodology from the mandatory datos.gob.es fork.

**Fork reference:** https://github.com/Jvilpi/Laboratorio-de-Datos

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
   ```
   fleet_baseline_2023  = 113,624  (cumulative historical 2015–2023)
   projected_2024–2027  = 106,547  (SARIMA sum)
   total_ev_projected_2027 = 220,171
   ```
   Assumption: fleet ≈ cumulative registrations (justified: BEV scrappage <1%/yr, most vehicles registered post-2019).

8. **Verification** — Asserts: type is `int`, value > 0, value > 100,000.

9. **Export** — Saves full metadata to `Data/processed/m3_ev_projection.json`.

**ZH:**

**目的：** 预测西班牙 2027 年 BEV 总量——`File 1.csv` 中 `total_ev_projected_2027` 的强制输入项。复现并扩展 datos.gob.es Fork 的 SARIMA 方法。

**Fork 引用：** https://github.com/Jvilpi/Laboratorio-de-Datos

**逐步说明：**

1. **初始化** — 导入 `statsmodels`、`pandas`、`numpy`、`matplotlib`、`pyarrow`。定义 Fork 的 parquet 文件原始 URL。

2. **下载历史数据** — 从 Fork 下载 108 个月度 parquet 文件（2015年1月–2023年12月），涵盖 DGT 车辆注册微观数据。原始记录共约 1,460 万条。

3. **加载与过滤** — 与 Fork 相同的过滤链：
   - `COD_TIPO == '40'` → 仅乘用车（约1040万条）
   - `CLAVE_TRAMITE` 在 `['1', '5', 'B']` → 仅正式注册（约1033万条）
   - `COD_PROPULSION_ITV == 'Electrico'`（DGT 代码 `'6'`）→ 纯 BEV（2015–2023 共 113,624 条）
   - 2023年年度 BEV 注册量：**27,928 辆**

4. **构建月度时间序列** — 按年月汇总 → 108 个月度 BEV 注册量观测值。

5. **SARIMA 模型** — 对对数变换后的月度数量拟合 `SARIMAX(1,0,2)(1,0,1)[12]`（与 Fork 规格相同）。对数变换稳定了指数增长的方差。AIC = 191.2。

6. **扩展预测** — 向前预测 48 个月（2024年1月–2027年12月），比原始 Fork 的 12 个月更长。将对数尺度预测反变换为注册量。年度预测：
   - 2024: ~32,102
   - 2025: ~28,060
   - 2026: ~24,649
   - 2027: ~21,736

7. **队列总量计算：**
   ```
   2015–2023 累计历史基数    = 113,624
   2024–2027 SARIMA预测总和 = 106,547
   total_ev_projected_2027  = 220,171
   ```
   假设：队列 ≈ 累积注册量（依据：BEV 报废率<1%/年，大多数车辆为2019年后注册）。

8. **验证** — 断言：类型为 `int`，值>0，值>100,000。

9. **导出** — 完整元数据保存至 `Data/processed/m3_ev_projection.json`。

---

## 5. Data Status Summary / 数据状态总览

| Dataset / 数据集 | Status / 状态 | Notes / 备注 |
|---|---|---|
| M1 — Road Network RTIG | ✅ Done | `carreteras_RTIG.geojson` — 1,535 segments, ~29,050 km |
| M2 — EV Charging Points XML | ⚠️ Re-download needed | `electrolineras_spain.xml` updates every 24h |
| M3 — EV Fleet Projections | ✅ Done | `total_ev_projected_2027 = 220,171` |
| R1 — i-DE Grid Capacity | ❌ Missing | Manual download from i-DE portal |
| R2 — Endesa Grid Capacity | ✅ Done | CSV + XLSX in `external/grid_capacity_endesa/` |
| R3 — Viesgo Grid Capacity | ❌ Missing | Manual download; fallback: generapp.eu |
| R4 — DGT Registrations | ✅ Done | 6 monthly ZIPs (Jun–Nov 2025) |
| R5 — Local Charging Points | ⚠️ Optional | Manual download from datos.gob.es |

---

## 6. Notebooks Still To Build / 待完成的 Notebooks

| Notebook | Purpose / 目的 | Key Inputs / 关键输入 | Key Output / 关键输出 |
|---|---|---|---|
| M2 — EV Charging Points | Parse DATEX2 XML; filter to interurban baseline | `electrolineras_spain.xml`, `carreteras_RTIG.geojson` | `total_existing_stations_baseline` (for File 1) |
| M4 — Station Placement | Place candidate stations along eligible roads; assign grid_status | `carreteras_RTIG.geojson`, grid capacity data (R1/R2/R3), EV demand weights | `File 2.csv` |
| M5 — Friction Points | Subset File 2 where grid_status ≠ Sufficient | `File 2.csv` | `File 3.csv` |
| Final — File 1 Assembly | Combine KPIs from M2, M3, M4, M5 | All outputs | `File 1.csv` |
| BI Map | Interactive map colour-coded by grid_status | `File 2.csv` | Self-contained HTML map |

---

## 7. Key Methodology Decisions (for Analytical Report) / 方法论关键决策（供分析报告引用）

**EN:**
- **EV autonomy assumption:** Must be documented (e.g., 300–400 km average range → max station spacing ~150–200 km on any given corridor).
- **Grid status thresholds:** Team must define own thresholds for `Sufficient` / `Moderate` / `Congested` based on nearest substation's available capacity (MW) vs. estimated demand. Must be justified.
- **Spatial matching methodology:** How each proposed station is matched to the nearest i-DE / Endesa / Viesgo substation — must be documented.
- **150 kW per charger:** Fixed by datathon rules. `estimated_demand_kw = n_chargers × 150`.
- **File 3 scope:** Only Moderate or Congested from File 2 — Sufficient locations excluded.

**ZH:**
- **EV 续航假设：** 必须记录（例如：平均续航 300–400 km → 任意走廊最大站间距约 150–200 km）。
- **电网状态阈值：** 团队需自定义 `Sufficient`/`Moderate`/`Congested` 阈值，基于最近变电站可用容量（MW）与预估需求的对比。须有依据。
- **空间匹配方法：** 每个提议站点如何匹配最近的 i-DE / Endesa / Viesgo 变电站——必须记录。
- **每个充电桩 150 kW：** 赛规固定。`estimated_demand_kw = n_chargers × 150`。
- **File 3 范围：** 仅包含 File 2 中的 Moderate 或 Congested 位置，Sufficient 需排除。

---

*Generated for IE Sustainability Datathon March 2026 — Iberdrola Challenge.*
