import json
import types

def createSQLTemplate(d, table, dataType):
    # Prepare the placeholders with the number of items in station
    placeholders = ['%s'] * len(d)

    # Aemet Data
    if dataType == 'json':
        # Prepare insert template with bind parameters
        sql_template = """
        REPLACE INTO {table} ({columns}) VALUES ({placeholders})
        """
        # Add bind parameters
        sql = sql_template.format(
            table=table,
            columns=','.join(d.keys()),
            placeholders=','.join(placeholders)
        )

    # Air Quality Data
    elif dataType == 'list':
        # Prepare insert template with bind parameters
        sql_template = """
        REPLACE INTO {table} VALUES ({placeholders})
        """

        # Add bind parameters
        sql = sql_template.format(
            table=table,
            placeholders=','.join(placeholders)
        )

    return sql

def uploadData(cursor, data, table):
    """ This function implements a insert into sql sentence. The column names
    are the key names of the data object.
    """

    if type(data).__name__ == 'str':
        # Parse json object
        data = json.loads(data)
        dataType = 'json'

    elif type(data).__name__ == 'list':
        dataType = 'list'

    else:
        # Return false (error)
        return False

    # Iterate by all the objects
    for d in data:

        # Prepare template depending on dataType
        sql = createSQLTemplate(d,table,dataType)

        # TODO: Group insert in 1 (max 10.000 lines)

        # Execute query
        if dataType == 'json':
            cursor.execute(sql, list(d.values()))
        elif dataType == 'list':
            cursor.execute(sql,d)

    # Upload completed
    return True;
