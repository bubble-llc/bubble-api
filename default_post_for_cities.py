import json
from app.util.db_connection import DbConnection
from datetime import datetime, timezone
from decimal import Decimal
from app.queries_new_schema import QUERY_CHECK_CONNECTION, QUERY_INSERT_POST_TO_CATEGORY

with open('major_city_coordinates.json') as json_file:
    cities = json.load(json_file)
print(cities)

dbconnection = DbConnection('db_credentials.yaml')
dbconnection.init_db_connection()
con = dbconnection.connection
for city in cities:
    print(city["latitude"])
    print(city["longitude"])
    cursor = con.cursor()
    cursor.execute(QUERY_INSERT_POST_TO_CATEGORY, (
        1,
        1,
        "Welcome to Bubble",
        "Hello",
        Decimal(city["latitude"]),
        Decimal(city["longitude"]),
        datetime.now(tz=timezone.utc),
        Decimal(city["longitude"]),
        Decimal(city["latitude"]),
        )
    )
con.commit()
cursor.close()