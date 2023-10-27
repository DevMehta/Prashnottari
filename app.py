#!/bin/env python

from pranshnottriApp import create_app, socketio
from sqlalchemy.sql import text
from sqlalchemy import create_engine
'''Database connectivity'''
password = 'mysql'
hostname = 'localhost'  
database_name = 'quiz_db'

connection_string = f'mysql+mysqlconnector://root:mysql@localhost/quiz_db'

# Create an SQLAlchemy engine
engine = create_engine(connection_string)

# Test the connection
try:
    with engine.connect() as connection:
        print("Connected to the database")
except Exception as e:
    print(f"Connection error: {e}")


# SQL SELECT query
query = text("SELECT * FROM quiz")

with engine.connect() as connection:
    result = connection.execute(query)
    for row in result:
        print(row)

app = create_app(debug=True)

if __name__ == '__main__':
    socketio.run(app)