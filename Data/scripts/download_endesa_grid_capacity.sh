#!/bin/bash
# =============================================================================
# Script: download_endesa_grid_capacity.sh
# Purpose: Download Endesa e-distribución grid access capacity data
# Source: https://www.edistribucion.com/es/red-electrica/nodos-capacidad-red/capacidad-demanda.html
# Format: CSV + XLSX (updated monthly)
# Output: data/external/grid_capacity_endesa/
# =============================================================================
# NOTE: Update YEAR_MONTH and DATE_TAG when new monthly files are published.
# Pattern: https://www.edistribucion.com/content/dam/edistribucion/
#          conexion-a-la-red/descargables/nodos/demanda/YYYYMM/YYYY_MM_DD_R1299_demanda.csv
# =============================================================================

OUTPUT_DIR="$(dirname "$0")/../external/grid_capacity_endesa"
mkdir -p "$OUTPUT_DIR"

BASE_URL="https://www.edistribucion.com/content/dam/edistribucion/conexion-a-la-red/descargables/nodos/demanda"

# === Operator: e-distribución (R1299) ===
YEAR_MONTH="202603"
DATE_TAG="2026_03_04"
OPERATOR="R1299"

for EXT in csv xlsx; do
  FILENAME="${DATE_TAG}_${OPERATOR}_demanda.${EXT}"
  URL="${BASE_URL}/${YEAR_MONTH}/${FILENAME}"
  OUTFILE="$OUTPUT_DIR/${FILENAME}"

  if [ -f "$OUTFILE" ] && [ -s "$OUTFILE" ]; then
    echo "SKIP (exists): $FILENAME"
    continue
  fi

  echo "Downloading $FILENAME..."
  curl -L --max-time 60 --retry 2 \
    -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
    -o "$OUTFILE" "$URL"

  if [ -f "$OUTFILE" ] && [ -s "$OUTFILE" ]; then
    SIZE=$(wc -c < "$OUTFILE")
    echo "OK: $FILENAME ($SIZE bytes)"
  else
    echo "FAILED: $FILENAME"
  fi
done

# === Operator: EASA (R1026) — subsidiary in certain areas ===
OPERATOR="R1026"

for EXT in csv xlsx; do
  FILENAME="${DATE_TAG}_${OPERATOR}_demanda.${EXT}"
  URL="${BASE_URL}/${YEAR_MONTH}/${FILENAME}"
  OUTFILE="$OUTPUT_DIR/${FILENAME}"

  if [ -f "$OUTFILE" ] && [ -s "$OUTFILE" ]; then
    echo "SKIP (exists): $FILENAME"
    continue
  fi

  echo "Downloading $FILENAME..."
  curl -L --max-time 60 --retry 2 \
    -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
    -o "$OUTFILE" "$URL"

  if [ -f "$OUTFILE" ] && [ -s "$OUTFILE" ]; then
    SIZE=$(wc -c < "$OUTFILE")
    echo "OK: $FILENAME ($SIZE bytes)"
  else
    echo "FAILED or not available: $FILENAME"
  fi
done

echo ""
echo "=== Endesa capacity download complete ==="
ls -lh "$OUTPUT_DIR/"
