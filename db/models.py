from sqlalchemy import Column, Integer, String, ForeignKey
from db.database import Base

class Jobs(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    job = Column(String, nullable=False)

class Departments(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, index=True)
    department = Column(String, nullable=False)

class Hired_Employees(Base):
    __tablename__ = "hired_employees"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    datetime = Column(String, nullable=False)
    department_id = Column(Integer, ForeignKey(Departments.id), nullable=False)
    job_id = Column(Integer, ForeignKey(Jobs.id), nullable=False)