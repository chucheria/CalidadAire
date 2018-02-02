#!/usr/bin/env python
# encoding: utf-8
"""
Constants.py
"""
# ==== AEMET ====

# AEMET API ENDPOINTS
WHEATHER_STATIONS_ENDPOINT = "https://opendata.aemet.es/opendata/api/valores/climatologicos/inventarioestaciones/todasestaciones"
WHEATHER_CONVENTIONAL_OBSERVATION = "https://opendata.aemet.es/opendata/api/observacion/convencional/datos/estacion/"

# AEMET TABLES
WHEATHER_STATIONS_TABLE = "stationAEMET"
WHEATHER_OBSERVATION_TABLE = "observation"

# VARIABLES TO CLEAN

GEO_VARS = ['geo700','geo850','geo925']

# ==== AIR QUALITY ====

# MADRID AIR QUALITY (HOULY)
AIR_QUALITY_ENDPOINT = "http://www.mambiente.munimadrid.es/opendata/horario.txt"

# AIR QUALITY TABLES
AIR_QUALITY_TABLE = "airQuality"

# MADRID AIR QUALITY FIELDS
MAQ_STATION_COMUNITYCODE = 0
MAQ_STATION_TOWN = 1
MAQ_STATION_CODE = 2
MAQ_PARAMETER = 3
MAQ_ANALITYC_TECHNIQUE = 4
MAQ_ANALITYC_PERIOD = 5
MAQ_YEAR = 6
MAQ_MONTH = 7
MAQ_DAY = 8
MAQ_FIRST_VALUE = 9
MAQ_LAST_VALUE = 57
