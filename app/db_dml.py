import os
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from db.database import sessionlocal
from app.utils.logger_manager import LoggerManager

#Initializing loggers
logger = LoggerManager("logs", "load_csv_errors.log")

def insert_into_db(items, model):
    db = sessionlocal()
    try:
        db.add_all(items)
        db.commit()
        result_msg = f"[Success]: {len(items)} records inserted into {model.__tablename__} table."
        return {"result_msg": result_msg}
    except SQLAlchemyError as e:
        db.rollback()
        result_msg = f"[Error]: Database error. Details {str(e)}."
        print(result_msg)
        logger.log_error(f"{datetime.now().isoformat()} - {result_msg} - {e}\n")
        return {"result_msg": "[Error]: Database error. See details in load_csv_errors.log"}
    finally:
        db.close()