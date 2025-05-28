from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, ValidationError
from typing import List
from app import db_dml
from db.models import Jobs, Departments, Hired_Employees
from db.database import engine
from datetime import datetime
from typing import Any
from sqlalchemy import text
from app.utils.logger_manager import LoggerManager

#Config logger
logger = LoggerManager("logs", "json_columns_type_error.log")

router = APIRouter()

#Models/Tables
class JobSchema(BaseModel):
    id: int
    job: str

class DepartmentSchema(BaseModel):
    id: int
    department: str

class HiredEmployeeSchema(BaseModel):
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
            logger.log_error(f"{datetime.now().isoformat()} {e} -  Column {item}")
            return {"result_msg": f"{e} -  Column {item}"}

    if not valid_items:
        raise HTTPException(status_code=400, detail="There is no valid rows to insert")

    return db_dml.insert_into_db(valid_items, model_class)

@router.get("/report/quarterly-hiring")
def quarterly_hiring(datefrom: str = Query(...), dateto: str = Query(...)):
    query = text("""
        SELECT department Department, job Job, 
            SUM(CASE WHEN CAST((strftime('%m', datetime) + 2) / 3 AS INTEGER) = 1 THEN 1 ELSE 0 END) AS Q1,
            SUM(CASE WHEN CAST((strftime('%m', datetime) + 2) / 3 AS INTEGER) = 2 THEN 1 ELSE 0 END) AS Q2,
            SUM(CASE WHEN CAST((strftime('%m', datetime) + 2) / 3 AS INTEGER) = 3 THEN 1 ELSE 0 END) AS Q3,
            SUM(CASE WHEN CAST((strftime('%m', datetime) + 2) / 3 AS INTEGER) = 4 THEN 1 ELSE 0 END) AS Q4
        FROM hired_employees e
        LEFT JOIN jobs j ON e.job_id = j.id
        LEFT JOIN departments d ON e.department_id = d.id
        WHERE datetime >= :datefrom AND datetime <= :dateto
        GROUP BY department, job
        ORDER BY department, job
    """)
    with engine.connect() as conn:
        result = conn.execute(query, {"datefrom": datefrom, "dateto": dateto})
        return [dict(row._mapping) for row in result]

@router.get("/report/above-average-hiring")
def above_average_hiring(datefrom: str = Query(...), dateto: str = Query(...)):
    query = text("""
        SELECT d.department Department, COUNT(*) Hired
        FROM hired_employees e
        INNER JOIN (
            SELECT department_id
            FROM (
                SELECT department_id, COUNT(*) hires_dep,
                       AVG(COUNT(*)) OVER () AS avg_hires
                FROM hired_employees
                WHERE datetime >= :datefrom AND datetime <= :dateto
                GROUP BY department_id
            ) q
            WHERE hires_dep > avg_hires
        ) deps_hire_over_mean ON deps_hire_over_mean.department_id = e.department_id
        LEFT JOIN departments d ON d.id = e.department_id
        GROUP BY e.department_id, d.department
        ORDER BY Hired DESC
    """)
    with engine.connect() as conn:
        result = conn.execute(query, {"datefrom": datefrom, "dateto": dateto})
        return [dict(row._mapping) for row in result]
