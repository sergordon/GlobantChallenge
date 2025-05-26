# import sys
# import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, model_validator, ValidationError
from typing import List
from app import db_dml
from db.models import Jobs, Departments, Hired_Employees
import os
import logging
from typing import Any

#Config logger
LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(level=logging.INFO, 
                    filename="Api_invalid_rows.log",
                    filemode="a")

router = APIRouter()

# Global validator
class ModelValidator(BaseModel):
    @model_validator(mode='after')
    def no_null_or_empty_fields(model):
        for field, value in model.__dict__.items():
            if value is None or (isinstance(value, str) and value.strip() == ""):
                raise ValueError(f"Field '{field}' must not be null or empty")
        return model


#Models/Tables
class JobSchema(ModelValidator):
    id: int
    job: str

class DepartmentSchema(ModelValidator):
    id: int
    department: str

class HiredEmployeeSchema(ModelValidator):
    id: int
    name: str
    datetime:str
    department_id: int
    job_id: int

#Mapping
model_mapping = {
    "jobs": (JobSchema, Jobs),
    "departments": (DepartmentSchema, Departments),
    "hired_employees": (HiredEmployeeSchema, Hired_Employees)
}

#Endpoint
@router.post("/insert/{table}")

def insertFromBatch(table: str, data: list[dict[str, Any]]):
    if not (1 <= len(data) <= 1000):
        raise HTTPException(status_code=400, detail=f"Batch must be between 1 and 1000")
    
    if table not in model_mapping:
        raise HTTPException(status_code=404, detail=f"Table '{table}' not found")
    
    schema_class, model_class = model_mapping[table]

    valid_items = []
    for item in data:
        try:
            validated = schema_class(**item)
            model_instance = model_class(**validated.model_dump())
            valid_items.append(model_instance)
        except ValidationError as e:
            logging.warning(f"[{table}] Null value in column {item} | Error: {e}")

    if not valid_items:
        raise HTTPException(status_code=400, detail="There is no valid rows to insert")

    return db_dml.insert_into_db(valid_items, model_class)


# def main():
#     results = insertFromBatch("jobs", c)
#     return print(results.items)

# if __name__ == "__main__":
#     main()