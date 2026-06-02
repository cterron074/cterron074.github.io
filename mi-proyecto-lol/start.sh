#!/usr/bin/env bash
# Detener el proceso si alguno de los scripts da error
set -e

echo "Ejecutando preparación del ETL..."
python src/preparar_etl.py

echo "Ejecutando el pipeline ETL..."
python src/etl.py

echo "Iniciando Gunicorn..."
gunicorn --chdir src app:app -b 0.0.0.0:$PORT
