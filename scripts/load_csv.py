import os
import pandas as pd
from sqlalchemy.exc import SQLAlchemyError
from db.database import engine
from db.models import Base
from datetime import datetime
from app.utils.logger_manager import LoggerManager

#Initializing loggers
logger_erros = LoggerManager("logs", "load_csv_errors.log")
logger_invalid_rows = LoggerManager()

# Execute models and create tables
Base.metadata.create_all(bind=engine)

DATA_DIR = "data"

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
            row_dic["error_datetime"] = {datetime.now().isoformat()}
            row_dic["tablename"] = tablename
            row_dic["error"] = error_message
            invalid_rows.append(row_dic)
    
    if valid_rows:
        try:
            pd.DataFrame(valid_rows).to_sql(tablename, engine, if_exists='append', index=False)
            result_msg = f"[Success]: {len(valid_rows)} records loaded from {path} into table {tablename}"
            print(result_msg)
        except SQLAlchemyError as e_sql:
            result_msg = f"[Error]: Failed to load {path}. See details in load_csv_errors.log"
            print(result_msg)
            logger_erros.log_error(f"{datetime.now().isoformat()} [SQL ERROR]: {result_msg} - {e_sql}\n")
            return {"result_msg": result_msg}

        except Exception as e:
            result_msg = f"[Error]: General error {e}"
            print(result_msg)
            logger_erros.log_error(f"{datetime.now().isoformat()} [GENERAL ERROR]: {result_msg}\n")
            return {"result_msg": result_msg}

        results_msg.append(result_msg)

    if invalid_rows:
        log_file = "invalid_rows.log"
        result_msg = f"[WARN]: {len(invalid_rows)} invalid records logged to {log_file}"
        print(result_msg)
        logger_invalid_rows.log_dataframe(pd.DataFrame(invalid_rows), filename=log_file)
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