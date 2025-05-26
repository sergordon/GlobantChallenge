import fastavro
import os
from sqlalchemy import text, inspect
from db.database import engine

# Map SQLAlchemy types to AVRO types
def sqlalchemy_to_avro_type(col_type):
    col_type = str(col_type).lower()
    if "int" in col_type:
        return ["null", "int"]
    elif "char" in col_type or "text" in col_type:
        return ["null", "string"]
    elif "bool" in col_type:
        return ["null", "boolean"]
    elif "float" in col_type or "real" in col_type or "numeric" in col_type or "double" in col_type:
        return ["null", "float"]
    elif "date" in col_type or "time" in col_type:
        return ["null", "string"]  
    else:
        return ["null", "string"]

def backup_table(table_name):
    conn = engine.connect()
    result = conn.execute(text(f"SELECT * FROM {table_name}"))
    records = [dict(row) for row in result.mappings()]

    if not records:
        return {"results_msg": f"There is no data to backup in table {table_name}"}
    
    inspector = inspect(engine)
    columns = inspector.get_columns(table_name)

    schema = {
        "doc": f"{table_name} schema",
        "name": table_name,
        "namespace": "backup",
        "type": "record",
        "fields": [{"name": col["name"], "type": sqlalchemy_to_avro_type(col["type"])} for col in columns]
    }
    os.makedirs("backup", exist_ok=True)
    with open(f"backup/{table_name}.avro", "wb") as out:
        fastavro.writer(out, schema, records)
    return {"result_msg": f"Backup completed for table: {table_name}"}

def backup_all_tables():
    result = []
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    for table in tables:
        msg = backup_table(table)
        result.append(msg)
    result.append("Full database backup completed")
    return {"results_msg": result}