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

def check_valid_rows(row):
    for key, value in row.items():
        if pd.isna(value) or str(value).strip() == '':
            return False, f"Null or empty value in column '{key}'"
    return True, ""


def load_data_to_db(path, tablename, columns):
    invalid_rows = []
    valid_rows = []
    results_msg = []
    df = pd.read_csv(path, header=None, names=columns)

    #Check for null or empty values in each row
    for row in df.itertuples(index=False):
        row_dic = row._asdict()
        is_valid_row, error_message = check_valid_rows(row_dic)
        if is_valid_row:
            valid_rows.append(row_dic)
        else:
            row_dic["error"] = error_message
            invalid_rows.append(row_dic)
            results_msg.append(error_message)
    
    if valid_rows:
        try:
            pd.DataFrame(valid_rows).to_sql(tablename, engine, if_exists='append', index=False)
            result_msg = f"[Success]: {len(valid_rows)} records loaded from {path} into table {tablename}"
            print(result_msg)
        except SQLAlchemyError as e_sql:
            result_msg = f"[Error]: Failed to load {path}: {e_sql}"            
            print(result_msg)
        except Exception as e:
            result_msg = f"[Error]: General error {e}"
            print(result_msg)
        results_msg.append(result_msg)

    if invalid_rows:
        log_file = os.path.join(LOG_DIR, f"Errors_historic_load_of_{tablename}.log")
        pd.DataFrame(invalid_rows).to_csv(log_file, index=False)
        result_msg = f"[WARN]: {len(invalid_rows)} invalid records logged to {log_file}"
        print(result_msg)
        results_msg.append(result_msg)

    return {"result_msg": results_msg}

def main():
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".csv"):
            tb_name = os.path.splitext(filename)[0].lower()
            file_path = os.path.join(DATA_DIR, filename)
            columns = TB_SCHEMAS.get(tb_name)
            load_data_to_db(file_path, tb_name, columns)

if __name__ == "__main__":
    main()