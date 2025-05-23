from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DB_URL = "sqlite:///./poc.db"

# Able to use same connection from differente threads,
# it needs because  FastAPI handle multiple request in parallel threads
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})

sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Instance base class
Base = declarative_base()