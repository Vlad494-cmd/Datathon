"""
parse_madrid_imd.py
====================
Converts Madrid IMD traffic data into clean CSVs for the feature matrix.

STEP 1 — Unzips the Madrid IMD ZIP you already downloaded
STEP 2 — Downloads + parses the DGT Peajes PDF (toll roads)
STEP 3 — Saves clean CSVs to Data/raw/traffic_imd/
STEP 4 — Prints git commands to push

HOW TO RUN:
    1. Put imd_trafico_2024.zip in the same folder as this script
    2. pip install requests beautifulsoup4 lxml pdfplumber pandas
    3. python parse_madrid_imd.py

SOURCES:
    ZIP → https://www.comunidad.madrid/media/transportes/imd_trafico_2024.zip
    PDF → https://cdn.transportes.gob.es/portal-web-transportes/carreteras/
          red_carreteras/trafico/datos_historicos_1960_aforo/
          datos_historicos_peajes_2024.pdf
"""

import os, re, sys, zipfile, requests, pandas as pd, pdfplumber
from pathlib import Path
from bs4 import BeautifulSoup

SCRIPT_DIR = Path(__file__).parent
OUT_DIR    = SCRIPT_DIR / "Data" / "raw" / "traffic_imd"
TMP_DIR    = SCRIPT_DIR / "_tmp_imd"
OUT_DIR.mkdir(parents=True, exist_ok=True)
TMP_DIR.mkdir(exist_ok=True)

ZIP_LOCAL = SCRIPT_DIR / "imd_trafico_2024.zip"
PDF_URL   = (
    "https://cdn.transportes.gob.es/portal-web-transportes/carreteras/"
    "red_carreteras/trafico/datos_historicos_1960_aforo/"
    "datos_historicos_peajes_2024.pdf"
)
PDF_LOCAL = TMP_DIR / "datos_historicos_peajes_2024.pdf"


def clean_number(s):
    s = str(s).strip()
    if "." in s and "," in s:
        s = s.replace(".", "").replace(",", ".")
    elif "," in s:
        s = s.replace(",", ".")
    s = re.sub(r"[^\d.]", "", s)
    try:    return float(s)
    except: return None


# ── STEP 1: Unzip ─────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("STEP 1 — Unzipping Madrid IMD package")
print("="*60)

if not ZIP_LOCAL.exists():
    alt = TMP_DIR / "imd_trafico_2024.zip"
    if alt.exists():
        ZIP_LOCAL = alt
    else:
        print(f"\n  ERROR: ZIP not found at {ZIP_LOCAL}")
        print("  Download from:")
        print("  https://www.comunidad.madrid/media/transportes/imd_trafico_2024.zip")
        sys.exit(1)

extract_dir = TMP_DIR / "imd_extracted"
if not extract_dir.exists():
    print(f"  Extracting {ZIP_LOCAL.name} ...")
    with zipfile.ZipFile(ZIP_LOCAL, "r") as z:
        z.extractall(extract_dir)
    print("  Done.")

html_files = list(extract_dir.rglob("*.html")) + list(extract_dir.rglob("*.htm"))
print(f"  Found {len(html_files)} HTML files")

if not html_files:
    print("  No HTML files found. ZIP contents:")
    for f in sorted(extract_dir.rglob("*"))[:20]:
        print(f"    {f.relative_to(extract_dir)}")


# ── STEP 2: Parse HTML → CSV ──────────────────────────────────────────────────
print("\n" + "="*60)
print("STEP 2 — Parsing Madrid IMD HTML files")
print("="*60)

def parse_madrid_html(filepath):
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        soup = BeautifulSoup(f.read(), "lxml")
    road_code  = filepath.stem.upper()
    road_name  = road_code
    for tag in ["title","h1","h2","h3"]:
        el = soup.find(tag)
        if el and el.get_text(strip=True):
            road_name = el.get_text(strip=True); break
    rows = []
    for table in soup.find_all("table"):
        hrow = table.find("tr")
        if not hrow: continue
        headers = [th.get_text(" ", strip=True).lower() for th in hrow.find_all(["th","td"])]
        for tr in table.find_all("tr")[1:]:
            cells = [td.get_text(" ", strip=True) for td in tr.find_all(["td","th"])]
            if not cells or all(c=="" for c in cells): continue
            row = {"road_code":road_code,"road_name":road_name,"year":2024,
                   "region":"Comunidad de Madrid","network":"Autonómica CM",
                   "source_file":filepath.name}
            for i,cell in enumerate(cells):
                row[headers[i] if i<len(headers) else f"col_{i}"] = cell
            rows.append(row)
    return pd.DataFrame(rows)

madrid_dfs = []
for html_file in sorted(html_files):
    try:
        df = parse_madrid_html(html_file)
        if not df.empty: madrid_dfs.append(df)
    except Exception as e:
        print(f"  [warn] {html_file.name}: {e}")

if madrid_dfs:
    madrid_df = pd.concat(madrid_dfs, ignore_index=True)
    col_map = {}
    for col in madrid_df.columns:
        c = col.lower()
        if re.search(r"imd|intensidad|total veh|veh.*d[ií]a", c): col_map[col]="imd_total"
        elif re.search(r"ligero|coche|light", c):                  col_map[col]="imd_ligeros"
        elif re.search(r"pesado|camion|heavy", c):                 col_map[col]="imd_pesados"
        elif re.search(r"pk.?ini|inicio|desde", c):                col_map[col]="pk_inicio"
        elif re.search(r"pk.?fin|final|hasta", c):                 col_map[col]="pk_fin"
        elif re.search(r"tramo|denominaci|segment", c):            col_map[col]="tramo"
        elif re.search(r"veloc|speed|km.?h", c):                   col_map[col]="velocidad_media_kmh"
        elif re.search(r"%.*pes|pct.*pes", c):                     col_map[col]="pct_pesados"
    madrid_df = madrid_df.rename(columns=col_map)
    for col in ["imd_total","imd_ligeros","imd_pesados","pk_inicio","pk_fin",
                "velocidad_media_kmh","pct_pesados"]:
        if col in madrid_df.columns:
            madrid_df[col] = madrid_df[col].apply(lambda x: clean_number(x) if pd.notna(x) else None)
    out = OUT_DIR / "madrid_imd_2024.csv"
    madrid_df.to_csv(out, index=False, encoding="utf-8-sig")
    print(f"  OK  {len(madrid_df):,} rows | {madrid_df['road_code'].nunique()} roads -> {out.name}")
else:
    print("  [warn] No rows parsed from HTML.")
    madrid_df = pd.DataFrame()


# ── STEP 3: Download + parse Peajes PDF ──────────────────────────────────────
print("\n" + "="*60)
print("STEP 3 — DGT Peajes PDF (toll roads)")
print("="*60)

if not PDF_LOCAL.exists():
    print(f"  Downloading {PDF_LOCAL.name} ...")
    r = requests.get(PDF_URL, headers={"User-Agent":"Mozilla/5.0"}, stream=True, timeout=120)
    if r.status_code == 200:
        with open(PDF_LOCAL,"wb") as f:
            for chunk in r.iter_content(1024*256): f.write(chunk)
        print(f"  Saved ({PDF_LOCAL.stat().st_size/1e6:.1f} MB)")
    else:
        print(f"  HTTP {r.status_code}. Download manually:")
        print(f"  {PDF_URL}")
        print(f"  Save as: {PDF_LOCAL}")

def parse_peajes_pdf(path):
    records = []
    sta_re = re.compile(r"Estaci[oó]n:\s*(\S+)")
    rd_re  = re.compile(r"Carretera:\s*(\S+)")
    pk_re  = re.compile(r"PK:\s*([\d.,]+)")
    with pdfplumber.open(path) as pdf:
        print(f"  {len(pdf.pages)} pages")
        for page in pdf.pages:
            text  = page.extract_text() or ""
            lines = text.split("\n")
            sid = road = pk = ""
            for line in lines[:20]:
                m=sta_re.search(line); 
                if m: sid=m.group(1)
                m=rd_re.search(line);  
                if m: road=m.group(1)
                m=pk_re.search(line);  
                if m: pk=m.group(1).replace(",",".")
            for line in lines:
                parts = line.strip().split()
                if not parts: continue
                if re.match(r"^(19|20)\d{2}$", parts[0]) and len(parts)>=4:
                    try:
                        records.append({
                            "station_id": sid, "road_code": road,
                            "pk_km": float(pk) if pk else None,
                            "year": int(parts[0]),
                            "imd_total":   clean_number(parts[1]),
                            "imd_ligeros": clean_number(parts[2]),
                            "imd_pesados": clean_number(parts[3]),
                            "pct_pesados": clean_number(parts[4]) if len(parts)>4 else None,
                            "network": "Autopista Peaje", "region": "España",
                            "source_file": path.name,
                        })
                    except: pass
    return pd.DataFrame(records)

if PDF_LOCAL.exists() and PDF_LOCAL.stat().st_size > 10_000:
    peajes_df = parse_peajes_pdf(PDF_LOCAL)
    if not peajes_df.empty:
        peajes_df.to_csv(OUT_DIR/"peajes_imd_historico.csv", index=False, encoding="utf-8-sig")
        df24 = peajes_df[peajes_df["year"]==2024]
        df24.to_csv(OUT_DIR/"peajes_imd_2024.csv", index=False, encoding="utf-8-sig")
        print(f"  OK  {len(df24):,} stations (2024) | roads: {sorted(df24['road_code'].unique())}")
        print(f"  OK  Historical {len(peajes_df):,} rows (2001-2024) saved")
    else:
        print("  [warn] No rows extracted from PDF")
else:
    print("  PDF not available — skipping")


# ── STEP 4: README ────────────────────────────────────────────────────────────
readme = """# traffic_imd — Spain Road Traffic Data (IMD 2024)

## Files
| File | Source | Coverage |
|---|---|---|
| `madrid_imd_2024.csv` | Comunidad de Madrid | M-roads in Madrid region |
| `peajes_imd_2024.csv` | DGT Ministerio Transportes | AP toll motorways Spain-wide (2024) |
| `peajes_imd_historico.csv` | DGT Ministerio Transportes | AP toll motorways (2001-2024) |

## Key columns
- `road_code` — Road ID (AP-7, M-30, A-1 etc.)
- `imd_total` — Average vehicles/day
- `imd_ligeros` — Light vehicles/day
- `imd_pesados` — Heavy vehicles/day
- `pct_pesados` — % heavy traffic
- `pk_km` — Kilometre point on road

## Join to feature matrix
```python
imd = pd.read_csv('Data/raw/traffic_imd/peajes_imd_2024.csv')
imd_road = imd.groupby('road_code').agg(
    imd_mean=('imd_total','mean'), imd_max=('imd_total','max'),
    pct_pesados=('pct_pesados','mean'), n_imd_stations=('station_id','nunique')
).reset_index()
fm = fm.merge(imd_road, left_on='carretera_group', right_on='road_code', how='left')
fm['imd_mean'] = fm['imd_mean'].fillna(fm['imd_mean'].median())
```

## Sources
- https://www.comunidad.madrid/media/transportes/imd_trafico_2024.zip
- https://cdn.transportes.gob.es/.../datos_historicos_peajes_2024.pdf

Generated by `parse_madrid_imd.py`
"""
(OUT_DIR / "README.md").write_text(readme, encoding="utf-8")
print(f"\n  OK  README -> {OUT_DIR}/README.md")


# ── STEP 5: Git commands ──────────────────────────────────────────────────────
print("\n" + "="*60)
print("STEP 5 — Push to GitHub")
print("="*60)
print("""
  git add Data/raw/traffic_imd/
  git add parse_madrid_imd.py
  git commit -m "feat: add DGT IMD traffic data - Madrid region + AP toll roads 2024"
  git push origin main
""")
print("="*60)
print("ALL DONE")
print("="*60)
