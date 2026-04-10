#!/bin/bash
# =============================================================================
# Script: download_ev_charging_national.sh
# Purpose: Download national EV charging points (DATEX2 XML) from DGT/MITERD
# Source: https://nap.dgt.es/dataset/puntos-de-recarga-electrica-para-vehiculos
# Format: DATEX2 v3 XML (updated every 24 hours)
# Output: data/raw/ev_charging_points_national/
# =============================================================================

OUTPUT_DIR="$(dirname "$0")/../raw/ev_charging_points_national"
mkdir -p "$OUTPUT_DIR"

URL="https://infocar.dgt.es/datex2/v3/miterd/EnergyInfrastructureTablePublication/electrolineras.xml"
OUTFILE="$OUTPUT_DIR/electrolineras_spain.xml"

echo "Downloading national EV charging points XML..."
echo "Source: $URL"
curl -L --max-time 180 --retry 2 -o "$OUTFILE" "$URL"

if [ -f "$OUTFILE" ] && [ -s "$OUTFILE" ]; then
  SIZE=$(wc -c < "$OUTFILE")
  echo "OK: electrolineras_spain.xml ($SIZE bytes)"
else
  echo "FAILED: electrolineras_spain.xml"
  exit 1
fi

echo ""
echo "NOTE: This file is updated every 24 hours."
echo "Re-run this script to refresh the data."
