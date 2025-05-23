from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from db.database import SessionLocal

def insert_into_db(items, model):
    db = SessionLocal()

    try:
        db_obj = [model(**item) for item in items]
        db.add_all(db_obj)
        db.commit()
        return {"message": f"{len(db_obj)} records inserted into {model}."}
    except SQLAlchemyError as e:
        db.rollback()
        return {"error": "Databasee error", "details": str(e)}
    finally:
        db.close()