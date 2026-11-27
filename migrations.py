import psycopg
from dotenv import load_dotenv
import os
puti = "migrations"

load_dotenv()
table = os.getenv('TABLE')
if table is None:
    os._exit(1)
    
with psycopg.connect(table, autocommit=True) as connection: 
    connection.execute("""CREATE TABLE IF NOT EXISTS schema_migrations(name TEXT PRIMARY KEY, applied_at TIMESTAMPTZ DEFAULT NOW())""")
    for i in os.listdir(puti):
        connection.execute("""INSERT INTO schema_migrations(name) VALUES(%s)""", (i,))
        sql_query = open(i).read()
        connection.execute(sql_query)