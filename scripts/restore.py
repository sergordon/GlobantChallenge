import fastavro
from sqlalchemy import create_engine
import pandas as pd
from db.database import engine

def restore_table(table_name):
    with open(f"backup/{table_name}.avro", "rb") as fo:
        reader = fastavro.reader(fo)
        records = list(reader)
        df = pd.DataFrame(records)
        df.to_sql(table_name, engine, if_exists='replace', index=False)
