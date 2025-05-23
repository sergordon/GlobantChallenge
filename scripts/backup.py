import fastavro
import os
from sqlalchemy import text
from db.database import engine

def backup_table(table_name):
    conn = engine.connect()
    result = conn.execute(text(f"SELECT * FROM {table_name}"))
    records = [dict(row) for row in result]
    schema = {
        "doc": f"{table_name} schema",
        "name": table_name,
        "namespace": "backup",
        "type": "record",
        "fields": [{"name": col, "type": ["null", "string"]} for col in records[0].keys()]
    }
    os.makedirs("backup", exist_ok=True)
    with open(f"backup/{table_name}.avro", "wb") as out:
        fastavro.writer(out, schema, records)
