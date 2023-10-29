from sqlalchemy import create_engine
from flask import g

# Replace 'username', 'password', 'hostname', and 'database_name' with your MySQL credentials
username = 'root'
password = 'MySQLRoot23'
hostname = 'localhost'  # Typically 'localhost' for local MySQL server
database_name = 'ptori_app_db'

def  get_db_connection():
# Create a connection string
    connection_string = f'mysql+mysqlconnector://' + username + ':' + password + '@' + hostname + '/' + database_name
    # create engine
    engine = create_engine(connection_string)

    if 'db_connection' not in g:
        # create connection
        g.db_connection = engine.connect()

    # return the connection
    return g.db_connection

def close_db_connection(e=None):
    db_connection = g.pop('db_connection', None)

    if db_connection is not None:
        db_connection.close()

'''        
# Test the connection
try:
    with engine.connect() as connection:
        print("Connected to the database")
except Exception as e:
    print(f"Connection error: {e}")

from sqlalchemy import text

# SQL SELECT query
query = text("SELECT * FROM BRANCH")

with engine.connect() as connection:
    result = connection.execute(query)
    for row in result:
        print(row)
'''