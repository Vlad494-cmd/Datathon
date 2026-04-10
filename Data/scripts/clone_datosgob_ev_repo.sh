#!/bin/bash
# =============================================================================
# Script: clone_datosgob_ev_repo.sh
# Purpose: Clone the mandatory datos.gob.es EV electrification repository
# Source: https://github.com/Admindatosgobes/Laboratorio-de-Datos
# Article: https://datos.gob.es/en/conocimiento/road-electrification-deciphering-electric-vehicle-growth-spain-through-data-analytics
# Output: data/raw/ev_fleet_projections_datosgob/
# =============================================================================
# IMPORTANT: Teams MUST fork this repository (not just clone).
# Fork instructions:
#   1. Go to: https://github.com/Admindatosgobes/Laboratorio-de-Datos
#   2. Click "Fork" (top-right)
#   3. Clone YOUR fork, not the original
#   4. Reference YOUR fork URL in the Colab notebook and Analytical Report
# =============================================================================

OUTPUT_DIR="$(dirname "$0")/../raw/ev_fleet_projections_datosgob"
REPO_URL="https://github.com/Admindatosgobes/Laboratorio-de-Datos.git"

# The EV notebook is at:
NOTEBOOK_PATH="Data Science/Ruta a la electrificación de la Movilidad/Codigo/Notebook.ipynb"
COLAB_URL="https://colab.research.google.com/github/Admindatosgobes/Laboratorio-de-Datos/blob/main/Data%20Science/Ruta%20a%20la%20electrificaci%C3%B3n%20de%20la%20Movilidad/Codigo/Notebook.ipynb"

if [ -d "$OUTPUT_DIR/Laboratorio-de-Datos/.git" ]; then
  echo "Repo already cloned. Pulling latest..."
  git -C "$OUTPUT_DIR/Laboratorio-de-Datos" pull
else
  echo "Cloning datos.gob.es Laboratorio-de-Datos..."
  mkdir -p "$OUTPUT_DIR"
  git clone --depth=1 "$REPO_URL" "$OUTPUT_DIR/Laboratorio-de-Datos"
fi

echo ""
echo "Colab notebook URL:"
echo "$COLAB_URL"
echo ""
echo "IMPORTANT: Use Exercise 3 output (projected EV fleet 2027) as"
echo "the foundational input for all demand models."
