import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from db.database import engine
from db.models import Base
from datetime import datetime


# Execute models and create tables
Base.metadata.create_all(bind=engine)

DATA_DIR = "data"
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

TB_SCHEMAS = {
    "jobs": ['id', 'job'],
    'departments': ['id', 'department'],
    'hired_employees': ['id', 'name', 'datetime', 'department_id', 'job_id']
}

def check_rows_with_nulls(row):
    for key, value in row.items():
        if pd.isna(value) or str(value).strip() == '':
            return False, f"Null value in column '{key}'"
    return True, ""


def load_data_to_db(path, tablename, columns):
    rows_with_nulls = []
    rows_without_nulls = []
    df = pd.read_csv(path, header=None, names=columns)

    #Check for null or empty values in each row
    for row in df.itertuples(index=False):
        row_dic = row._asdict()
        is_not_null_row, error_message = check_rows_with_nulls(row_dic)
        if is_not_null_row:
            rows_without_nulls.append(row_dic)
        else:
            row_dic["error"] = error_message
            rows_with_nulls.append(row_dic)
    
    if rows_without_nulls:
        try:
            pd.DataFrame(rows_without_nulls).to_sql(tablename, engine, if_exists='append', index=False)
            print(f"[Success]: {len(rows_without_nulls)} records loaded from {path} into table {tablename}")
        except SQLAlchemyError as e_sql:
            print(f"[Error]: Failed to load {path}: {e_sql}")
        except Exception as e:
            print(f"[Error]: General error {e}")

    if rows_with_nulls:
        log_file = os.path.join(LOG_DIR, f"Errors_historic_load_of_{tablename}.log")
        pd.DataFrame(rows_with_nulls).to_csv(log_file, index=False)
        print(f"[WARN]: {len(rows_with_nulls)} invalid records logged to {log_file}")


def main():
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".csv"):
            tb_name = os.path.splitext(filename)[0].lower()
            file_path = os.path.join(DATA_DIR, filename)
            columns = TB_SCHEMAS.get(tb_name)
            load_data_to_db(file_path, tb_name, columns)

if __name__ == "__main__":
    main()