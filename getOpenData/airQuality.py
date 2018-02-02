#!/usr/bin/python3
# encoding: utf-8

"""
airQuality.py

This file implements the functions to retrieve data from air Quality of the city
of Madrid. The data is retrieved from:
(http://www.mambiente.munimadrid.es/opendata/horario.txt)
"""

import constants as c
import requests
import json
import pymysql
import functions
from io import StringIO
import csv

pymysql.install_as_MySQLdb()

def getRequest(url, params={}):
    """ This functions implements a simple GET request to retrieve air quality
    data."""

    # GET with params in URL
    r = requests.get(url, params)

    # TODO: Implement log
    print("log")

    # Return data
    return r.text if r.status_code == 200 else False

def prepareData(data):
    """ This functions formats the air quality data and prepare it to be uploaded
    to the database.
    Returns the data well formated
    """

    # Transform data string to csv object
    f = StringIO(data)
    reader = csv.reader(f, delimiter=',')

    dataPrepared = []

    # Iterate by row in csv
    for row in reader:

        # STATION
        station = row[c.MAQ_STATION_COMUNITYCODE] + row[c.MAQ_STATION_TOWN] + row[c.MAQ_STATION_CODE]

        # PARAMETER
        parameter = row[c.MAQ_PARAMETER]

        # ANALITIC TECHNIQUE
        analyticTechnique = row[c.MAQ_ANALITYC_PERIOD]

        # DATE
        date = row[c.MAQ_YEAR] + '-' + row[c.MAQ_MONTH] + '-' + row[c.MAQ_DAY]

        # VALUES
        """First cast to float in order to remove zeros. Then to str to concat
        with the data confirmation character """
        values = [str(float(row[i])) for i in range(c.MAQ_FIRST_VALUE,c.MAQ_LAST_VALUE,2)]

        # Create a line well formated
        l = [station] + [parameter] + [analyticTechnique] + [date] + values

        # Append to the list of data
        dataPrepared.append(l)

    # Return data well formated
    return dataPrepared


def getAirQuality(cursor):
    """ This functions implements things"""

    # Wheather stations list request
    data = getRequest(c.AIR_QUALITY_ENDPOINT)

    if data:
        # Format data
        data = prepareData(data)

        # Upload data to database
        result = functions.uploadData(cursor,data, c.AIR_QUALITY_TABLE)
        print(result)

# Get DB credentials
cred = json.load(open('credentials.json'))

# Open database connection
db = pymysql.connect(cred['host'],cred['user'],cred['password'],cred['database'])

# Prepare a cursor object using cursor() method
cursor = db.cursor()

# # Create connector to mysql database
getAirQuality(cursor)

db.commit()
db.close()
