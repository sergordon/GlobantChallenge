import fastavro
import os
from sqlalchemy import text
from db.database import engine

def restore_table(table_name):
    file_path = f"backup/{table_name}.avro"
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Backup file not found for table: {table_name}")

    with open(file_path, "rb") as f:
        reader = fastavro.reader(f)
        records = [record for record in reader]

    if not records:
        return {"result_msg": f"No records to restore for table: {table_name}"}

    columns = records[0].keys()
    values_placeholder = ", ".join([f":{col}" for col in columns])
    insert_stmt = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({values_placeholder})"

    with engine.begin() as conn:
        conn.execute(text(f"DELETE FROM {table_name}"))  # Clear table before restore
        conn.execute(text(insert_stmt), records)

    return {"result_msg": f"Table '{table_name}' restored successfully."}


def restore_all_tables():
    results = []
    for file in os.listdir("backup"):
        if file.endswith(".avro"):
            table_name = file.replace(".avro", "")
            try:
                msg = restore_table(table_name)
                results.append(msg)
            except Exception as e:
                results.append(f"Failed to restore {table_name}: {str(e)}")
    return {"results_msg": results}
