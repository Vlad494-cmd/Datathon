#!/bin/bash
# =============================================================================
# Script: download_dgt_registrations.sh
# Purpose: Download DGT monthly vehicle registration microdata (2025)
# Source: https://www.dgt.es/microdatos/
# Output: data/raw/dgt_vehicle_registrations/
# =============================================================================

OUTPUT_DIR="$(dirname "$0")/../raw/dgt_vehicle_registrations"
mkdir -p "$OUTPUT_DIR"

MONTHS=(6 7 8 9 10 11)
YEAR=2025

for MONTH in "${MONTHS[@]}"; do
  FILENAME="export_mensual_mat_${YEAR}$(printf '%02d' $MONTH).zip"
  URL="https://www.dgt.es/microdatos/salida/${YEAR}/${MONTH}/vehiculos/matriculaciones/${FILENAME}"
  OUTFILE="$OUTPUT_DIR/$FILENAME"

  if [ -f "$OUTFILE" ] && [ -s "$OUTFILE" ]; then
    echo "SKIP (exists): $FILENAME"
    continue
  fi

  echo "Downloading $FILENAME..."
  curl -L --max-time 120 --retry 3 -o "$OUTFILE" "$URL"

  if [ -f "$OUTFILE" ] && [ -s "$OUTFILE" ]; then
    SIZE=$(wc -c < "$OUTFILE")
    echo "OK: $FILENAME ($SIZE bytes)"
  else
    echo "FAILED: $FILENAME"
  fi
done

echo ""
echo "=== Download complete ==="
ls -lh "$OUTPUT_DIR/"
