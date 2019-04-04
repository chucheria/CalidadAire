#!/usr/bin/python3
# encoding: utf-8

"""
aemet.py

This file implements the functions to use the AEMET's open data using his api.
(https://opendata.aemet.es/centrodedescargas/inicio)
"""

import constants as c
import apikey
import requests
import json
import pymysql
import functions
pymysql.install_as_MySQLdb()



def getRequest(url, params={}):
    """ This functions implements a simple GET request with parameters
    applied to aemet api functions. The response has a link to donwload the
    data. A second get request downloads it."""

    # Add api key to params json
    params['api_key'] = apikey.AEMET_API_KEY

    # GET with params in URL
    r = requests.get(url, params, verify=False)

    # TODO: Implement log
    print("log")

    if r.status_code == 200:
        print("Status code: 200, Successfull")

        # Transform response into a json object
        r = json.loads(r.text)

        # Request data
        data = requests.get(r['datos'], verify=False)

        # Check if there's an error
        if data.status_code == 200 and len(json.loads(data.text)) == 2:
            # Error
            print(json.loads(data.text))
            return False
        else:
            # Request successfull
            return data.text

    else:
        return False

def getWheatherStationList(cursor):
    """ This functions implements things"""

    # Wheather stations list request
    data = getRequest(c.WHEATHER_STATIONS_ENDPOINT)

    if data:
        # Upload data to database
        functions.uploadData(cursor,data,c.WHEATHER_STATIONS_TABLE)

def cleanData(data):
    """ This function implements things3"""
    data = json.loads(data)
    for d in data:
        for v in c.GEO_VARS:
            d.pop(v,None)

    return json.dumps(data)

def getConventionalObservation(cursor, province):
    """ This functions implements things2"""

    # TODO: Get stations using var province
    # Madrid stations
    stations = ["3100B","3110C","3191E","3200","3129","3194U","3196","3195",
    "3266A","2462","3338","3111D","3175","3100B","3110C","3191E","3200","3129",
    "3194U","3196","3195","3266A","2462","3338","3111D","3175","3100B","3110C",
    "3191E","3200","3129","3194U","3196","3195","3266A","2462","3338","3111D",
    "3175","3100B","3110C","3191E","3200","3129","3194U","3196","3195","3266A",
    "2462","3338","3111D","3175"]

    # Iterate by station
    for station in stations:

        # Wheather stations list request
        data = getRequest(c.WHEATHER_CONVENTIONAL_OBSERVATION + station)

        print(data)

        if data:

            # Clean data
            data = cleanData(data)
            # Upload data to database
            functions.uploadData(cursor,data,c.WHEATHER_OBSERVATION_TABLE)

# Get DB credentials
cred = json.load(open('credentials.json'))

# Open database connection
db = pymysql.connect(cred['host'],cred['user'],cred['password'],cred['database'])

# Prepare a cursor object using cursor() method
cursor = db.cursor()

# Create connector to mysql database
# getWheatherStationList(cursor)
getConventionalObservation(cursor,"MADRID")
db.commit()
db.close()
