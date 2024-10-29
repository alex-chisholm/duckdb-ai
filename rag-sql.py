from sqlalchemy import create_engine

engine = create_engine("duckdb:///dc.duckdb")
with engine.connect() as connection:
    cursor = connection.exec_driver_sql("SELECT * FROM bank LIMIT 3")
    print(cursor.fetchall())


from llama_index.core import SQLDatabase
sql_database = SQLDatabase(engine, include_tables=["bank"])


from llama_index.core.query_engine import NLSQLTableQueryEngine
query_engine = NLSQLTableQueryEngine(sql_database)



# fails: https://www.datacamp.com/tutorial/building-ai-projects-with-duckdb --? Loading the DuckDB database


