import duckdb
import polars as pl
import pandas as pd

# make new local db
con = duckdb.connect("dc.duckdb")

bank_df = pl.read_csv("bank.csv")


con.execute("""
    CREATE TABLE IF NOT EXISTS bank AS 
    SELECT * FROM read_csv('bank.csv')
""")

con.execute("SHOW ALL TABLES").fetchdf()

con.execute("SELECT * FROM bank WHERE duration < 100 LIMIT 5").fetchdf()

# duckdb relations

bank_duck = duckdb.read_csv("bank.csv")
bank_duck.filter("duration < 100").limit(3).df()



rel = con.table("bank")
rel.columns
rel.filter("duration < 100").project("job,education,loan").order("job").limit(3).df()



res = duckdb.query("""SELECT 
                            job,
                            COUNT(*) AS total_clients_contacted,
                            AVG(duration) AS avg_campaign_duration,
                        FROM 
                            'bank.csv'
                        WHERE 
                            age > 30
                        GROUP BY 
                            job
                        ORDER BY 
                            total_clients_contacted DESC;""")
res.df()
con.close()

