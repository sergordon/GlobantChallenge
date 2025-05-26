from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from db.database import sessionlocal

def insert_into_db(items, model):
    db = sessionlocal()
    try:
        db.add_all(items)
        db.commit()
        result_msg = f"[Success]: {len(items)} records inserted into {model}."
        return {"result_msg": result_msg}
    except SQLAlchemyError as e:
        db.rollback()
        result_msg = f"[Error]: Database error. Details {str(e)}."
        return {"result_msg": result_msg}
    finally:
        db.close()